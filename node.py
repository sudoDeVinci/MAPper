import configparser
from uuid import uuid4
import tweepy
from db import cnx
from dbservices import insert_user, get_next_poi


class Node:

    __authenticated = False
    __api = None
    __client = None
    __batch = []
    __batch_size = 500
    __consecuetive_errors = 0
    __session_id = None


    # Initialize 
    def __init__(self, path) -> None:
        self.__login(path)


    # Authenticate Node
    def is_authenticated(self):
        authenticated = self.__authenticated
        return authenticated

    def get_id(self):
        return self.__session_id


    def __login(self, path):
        # read the config file
        config = configparser.ConfigParser()
        config.read(path)

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
            self.__session_id = uuid4()
            print("..Authenticated..\nNode One Up.")
        
        except Exception as e:
            print("Please check authentication details")


    # pull follower information for full follower list
    def __get_followers(self, followed_user_name, followed_user_id):
        # Pull follower information
        for response in tweepy.Paginator(self.__client.get_users_following,
                                            id = followed_user_id,
                                            max_results=1000, 
                                            limit=10):
            for user in response.data:
                id = user.id
                user_name = user.name
                user_at = user.username
                is_private = user.protected
                AVI_path = user.profile_image_url_https
                created = user.created_at
                
                # Add these user details to batch
                self.__batch.append((id, user_name, user_at, is_private, AVI_path, created))

                # Check if batch size has been met
                if (len(self.__batch) >= self.__batch_size):
                    # Insert leftover records
                    inserted = insert_user(followed_user_id, id, user_at, is_private, AVI_path, created)

                    if type(inserted) is str:
                        self.__consecuetive_errors +=1
                    elif type(inserted) is int:
                        self.__consecuetive_errors = 0
                        print("inserted \n")
                #--------------------------------#
                # ADD A LOG FILE FOR SQL CRASHES #
                #--------------------------------#

        # If all followers pulled but not full batch, insert anyway.
        if len(self.__batch) >=1 :
            for id, user_name, user_at, is_private, AVI_path, created in self.__batch:
                    # Insert leftover records
                    inserted = insert_user(followed_user_id, id, user_at, is_private, AVI_path, created)

                    if type(inserted) is str:
                        self.__consecuetive_errors +=1
                    elif type(inserted) is int:
                        self.__consecuetive_errors = 0
                        print("inserted \n")
            #---------------------------------------------------------------#
            # A NODE SHOULD CHECK THE STATE OF SOME OUTSIDE VARIABLE, LIKE  #
            # A BUTTON TO TELL IT TO STOP ITERATING, THEN IT RETURNS 1      #
            #---------------------------------------------------------------#
            self._batch = []


    def scrape_user(self, init_user_at):

        poi = self.__api.get_user(screen_name = init_user_at)
        poi_is_private = poi.protected
        poi_AVI_path = poi.profile_image_url_https
        poi_created = poi.created_at

        self.__batch.append((poi.id_str, poi.name, poi.screen_name, poi_is_private, poi_AVI_path, poi_created))

        while True:
            
            # When the first user is inserted, they will be inserted as following themself
            
            # We can find the next person of interest by doing a query for followers of this person of interest.

            # We should check if any follower records exist for this person of interest (LIMIT 1 for speed).
            print(f"Currently scraping : {poi.name}\r")
            self.__get_followers(poi.screen_name, poi.id_str)
            poi = self.__api.get_user(user_id = get_next_poi(poi.id_str))
            break

        print("done crawling.")


