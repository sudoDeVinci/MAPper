from array import array
import configparser
import tweepy
from api_instance import API_custom
from dbinit import cnx
from dbservices import insert_user, get_next_poi, calc_map_score, indexed_followers, assign_map_score,assign_zoo_score, get_map_score, get_zoo_score
from colorama import init, Fore, Back

class Worker:

    # general use API instance with config details from file
    __api:tweepy.API = None

    __consecutive_errors = 0

    # Each Node is passed different details and given a corresponding number/uuid
    __number = None
     
    # Batch of user accounts currently being processed
    __batches = []


    def __init__(self, api: tweepy.API) -> None:
        self.__api = api


    # pull follower information for full follower list
    def __get_followers(self, followed_user_id):

        # Get the scores for the poi by id
        prev_map_score = get_map_score(followed_user_id)
        prev_zoo_score = get_zoo_score(followed_user_id)

        """
        TODO:
            Separate each page of followers into possible 
        """

        # Pull follower information
        for user in tweepy.Cursor(self.__api.get_followers, user_id = followed_user_id, count = 200).items():
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
            # Calculate user scores
            map_score, zoo_score = calc_map_score(name, user_at, description, prev_map_score, prev_zoo_score)
                
            if inserted == 0:
                self.__consecutive_errors = 0
                
                """
                New scores only calculated if succesful insertion of user.
                """
                assign_zoo_score(id, zoo_score)
                assign_map_score(id, map_score)
            else:
                self.__consecutive_errors +=1
                print("\t└", inserted)

            #--------------------------------#
            # ADD A LOG FILE FOR SQL CRASHES #
            #--------------------------------#
            #---------------------------------------------------------------#
            # A NODE SHOULD CHECK THE STATE OF SOME OUTSIDE VARIABLE, LIKE  #
            # A BUTTON TO TELL IT TO STOP ITERATING, THEN IT RETURNS 1      #
            #---------------------------------------------------------------#


    def __set_initial_poi(self) -> tweepy.User:
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


    def __get_valid_poi(self) -> tweepy.User:
        while True:
            poi = self.__set_initial_poi()
            """
            Check if given user has been scraped
            """ 
            followers = indexed_followers(poi.id_str)

            """
            If the number of followers in the db is within 20% of the number currently
            then count the poi as fully scraped.

            This works for slow, gradual changes in followers, and for accounts that cannot be indexed for one reason or another.
            If a mass influx or decrease in followers for one user happens, a full wiping and redoing of the map region 
            would be needed, but this will be handled preferably by simply doing a full scrape again.
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


    """
    Manually point to a user as the first poi, then scrape followers using an array of api keys.
    Once done, find a follwoer that hasnt been indexed and give them a map and zoo score. If either score is at least 0.5
    then continue
    """
    def scrape_user(self, api_list: array[API_custom]) -> None:

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

            # We pass the general operation api instance for this 
            poi_tup = get_next_poi(poi, self.__api)

            
            if poi_tup == 0:
                print("\t└ Dead end. Insular account reached")
                break

            new_poi_id, map_score, zoo_score = poi_tup
            
            poi = self.__api.get_user(user_id = new_poi_id)
            # FIND ANOTHER WAY TO DO THIS, THIS IS VERY BAD

        print("done crawling.")

