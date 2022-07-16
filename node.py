import configparser
import tweepy
from dbinit import cnx
from dbservices import insert_user, get_next_poi, calc_map_score, indexed_followers, assign_map_score,assign_zoo_score, get_map_score, get_zoo_score
from colorama import init, Fore, Back

class Node:

    __authenticated = False
    # API instance with config details from file
    __api = None
    __consecuetive_errors = 0
    # Each Node is passed different details and given a corresponding number
    __number = None



    # Initialize Node instance
    def __init__(self, path) -> None:
        self.__login(path)



    # Authenticate Node Instance
    def is_authenticated(self):
        authenticated = self.__authenticated
        return authenticated



    # Get the node number to match with details
    def get_number(self):
        return self.__number



    # Login using config file details
    def __login(self, path):
        # read the config file
        config = configparser.ConfigParser()
        try:
            config.read(path)

            # Pass the config file details
            api_key = config['twitter']['API_KEY']
            api_key_secret = config['twitter']['SECRET_KEY']

            access_token = config['twitter']['ACCESS_TOKEN']
            access_token_secret = config['twitter']['SECRET_ACCESS_TOKEN']

            bearer_token = config['twitter']['BEARER_TOKEN']

            self.__number = config['twitter']['NUMBER']

            # Authenticate Node details
            try:
                auth = tweepy.OAuthHandler(api_key, api_key_secret)
                auth.set_access_token(access_token, access_token_secret)
                
                self.__api = tweepy.API(auth, wait_on_rate_limit = True)

                self.__authenticated = True

                # Print Node status
                print(">> Authenticated: Node {0} Running..\n".format(self.__number))
            
            except Exception as e:
                print("\t└ ERROR: Please check authentication details for node {0}.\n\t\t└ ".format(self.__number), e)
        except Exception as e:
            print("\t└ ERROR: Please check authentication details for nodes")



    # pull follower information for full follower list
    def __get_followers(self, followed_user_id):

        # Get the scores for the poi by id

        # Pull follower information
        for user in tweepy.Cursor(self.__api.get_followers, user_id = followed_user_id, count = 300).items():
            id = user.id
            name = user.name
            user_at = user.screen_name
            is_private = user.protected
            AVI_path = user.profile_image_url
            description = user.description
            created = user.created_at


            # Insert user records
            # For some reason, the true protected status of users gotten here is unknown and simply defaults to None.
            # While this is inconvenient, it doesnt not largely affect operation.
            inserted = insert_user(followed_user_id, id, user_at, is_private, AVI_path, description, created)
            #print(inserted)
            # Calculate user scores
            prev_map_score = get_map_score(followed_user_id)
            prev_zoo_score = get_zoo_score(followed_user_id)
            map_score, zoo_score = calc_map_score(name, user_at, description, prev_map_score, prev_zoo_score)
                
            if inserted == 0:
                self.__consecuetive_errors = 0
                
                """
                New scores only calculated if succesful insertion of user.
                """
                assign_zoo_score(id, zoo_score)
                assign_map_score(id, map_score)
            else:
                self.__consecuetive_errors +=1
                print("\t└", inserted)


                #print("inserted \n")
            #--------------------------------#
            # ADD A LOG FILE FOR SQL CRASHES #
            #--------------------------------#
            #---------------------------------------------------------------#
            # A NODE SHOULD CHECK THE STATE OF SOME OUTSIDE VARIABLE, LIKE  #
            # A BUTTON TO TELL IT TO STOP ITERATING, THEN IT RETURNS 1      #
            #---------------------------------------------------------------#



    def __get_exsiting_poi(self):
        # Get person of interest by scrren_name
        init_user_at = input("\nPerson of interest: @")
        poi = self.__api.get_user(screen_name = init_user_at)
        """
        Check if the user exists 
        """
        while poi is None or poi.protected:
            if poi is None:
                init_user_at = input("\nUser {0} does not exist, give new User: @".format(poi.name))
            elif poi.protected:
                init_user_at = input("\nUser {0} is private, give new User: @".format(poi.name))
            poi = self.__api.get_user(screen_name = init_user_at)

        return poi
                 


    def __get_valid_poi(self):
        while True:
            poi = self.__get_exsiting_poi()
            """
            Check if given user has been scraped
            """ 
            followers = indexed_followers(poi.id_str)

            """
            If the number of followers in the db is within 5% of the number currently
            then count the poi as fully scraped.

            This works for slow, gradual changes in followers. If a mass influx or decrease in followers for one user happens, a full wiping and redoing of the map region would be needed.
            For our purposes however, this is fine.
            """

            if followers != 0:
                print("\n>> Given user alrady scraped, checking variance..")
                current_follower_count = poi.followers_count
                upper = 1.20 * current_follower_count
                lower = 0.80 * current_follower_count

                #print(f"Upper: {upper}\t|\tIndexed: {followers}\t|\tLower: {lower}")

                if (lower<= followers <= upper):
                    print("\t└ Followers within variance range, cannot scrape.\n")
                    continue
                else:
                    print("\t└ Followers not within variance range, valid for scraping.\n")
                    return poi
            else:
                print("\n>> Initial user {0} Valid for scraping\n".format(poi.name))
                return poi



    def scrape_user(self):

        poi = self.__get_valid_poi()
        insert_user(poi.id_str, poi.id_str, poi.screen_name, poi.protected, poi.profile_image_url_https, poi.description, poi.created_at)
        map_score = 1.000
        zoo_score = 1.000
        assign_zoo_score(poi.id_str, zoo_score)
        assign_map_score(poi.id_str, map_score)

        while True:
            
            # When the first user is inserted, they will be inserted as following themself 
            # We can find the next person of interest by doing a query for followers of this person of interest.

            print(f"> Currently scraping: {poi.name}\nMAP Score: {map_score}\t |\tZOO Score: {zoo_score}")
            
            self.__get_followers(poi.id_str)

            poi_tup = get_next_poi(poi, self.__api)

            
            if poi_tup == 0:
                print("\t└ Dead end. Insular account reached")
                break

            new_poi_id, map_score, zoo_score = poi_tup
            
            poi = self.__api.get_user(user_id = new_poi_id)
            # FIND ANOTHER WAY TO DO THIS, THIS IS VERY BAD

        print("done crawling.")

