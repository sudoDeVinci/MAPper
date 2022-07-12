import configparser
import tweepy
from dbinit import cnx
from dbservices import insert_user, get_next_poi, calc_map_score, indexed_followers, assign_map_score,assign_zoo_score


class Node:

    __authenticated = False
    # API instance with config details from file
    __api = None
    __client = None
    __consecuetive_errors = 0
    # Each Node is passed different details and given a corresponding number
    __number = 0

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
        config.read(path)

        # Pass the config file details
        api_key = config['twitter']['API_KEY']
        api_key_secret = config['twitter']['SECRET_KEY']

        access_token = config['twitter']['ACCESS_TOKEN']
        access_token_secret = config['twitter']['SECRET_ACCESS_TOKEN']

        bearer_token = config['twitter']['BEARER_TOKEN']

        # Authenticate Node details
        try:
            auth = tweepy.OAuthHandler(api_key, api_key_secret)
            auth.set_access_token(access_token, access_token_secret)
            
            self.__api = tweepy.API(auth, wait_on_rate_limit = True)

            self.__client = tweepy.Client(
                    bearer_token = bearer_token,
                    access_token = access_token, access_token_secret = access_token_secret,
                    wait_on_rate_limit = True
                )

            self.__authenticated = True

            # Assign session ID
            print("..Authenticated..\nNode Up.")
        
        except Exception as e:
            print("Please check authentication details")

    


    # pull follower information for full follower list
    def __get_followers(self, followed_user_id):

        # Get the scores for the poi by id

        # Pull follower information
        for response in tweepy.Paginator(self.__client.get_users_following,
                                            id = followed_user_id,
                                            max_results=1000, 
                                            limit=10):
            for user in response.data:
                id = user.id
                user_at = user.username
                is_private = user.protected
                AVI_path = user.profile_image_url_https
                description = user.description
                created = user.created_at
                
                # Calculate user scores
                map_score, zoo_score = calc_map_score()
                # Insert user records
                inserted = insert_user(followed_user_id, id, user_at, is_private, AVI_path, description, created)

                if type(inserted) is str:
                    self.__consecuetive_errors +=1
                elif type(inserted) is int:
                    self.__consecuetive_errors = 0
                    """
                    New scores only calculated if succesful insertion of user.
                    """
                    assign_zoo_score(id, zoo_score)
                    assign_map_score(id, map_score)
                    print("inserted \n")
                #--------------------------------#
                # ADD A LOG FILE FOR SQL CRASHES #
                #--------------------------------#
                #---------------------------------------------------------------#
                # A NODE SHOULD CHECK THE STATE OF SOME OUTSIDE VARIABLE, LIKE  #
                # A BUTTON TO TELL IT TO STOP ITERATING, THEN IT RETURNS 1      #
                #---------------------------------------------------------------#
    
    def __get_exsiting_poi(self):
        # Get person of interest by scrren_name
        init_user_at = input("Person of interest: @")
        poi = self.__api.get_user(screen_name = init_user_at)
        """
        Check if the user exists 
        """
        while poi is None:
            init_user_at = input("Inital User: @")
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
                print("Given user alrady scraped, checking variance..")
                current_follower_count = poi.followers_count
                upper = 1.05 * current_follower_count
                lower = 0.95 * current_follower_count

                if (lower<= followers <= upper):
                    print("\t└ Followers within variance range, cannot scrape.\n")
                    continue
                else:
                    return poi
            else:
                return poi

                
            

    def scrape_user(self, init_user_at):

        poi = self.__get_valid_poi()
        assign_zoo_score(poi.id_str, 1.000)
        assign_map_score(poi.id_str, 1.000)

        while True:
            
            # When the first user is inserted, they will be inserted as following themself 
            # We can find the next person of interest by doing a query for followers of this person of interest.

            print(f"Currently scraping : {poi.name}\r")
            
            self.__get_followers(poi.id_str)
            poi = self.__api.get_user(user_id = get_next_poi(poi))
            if poi is None:
                print("Dead end. Insular account reached")
                break

        print("done crawling.")


