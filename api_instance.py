import configparser
from uuid import uuid4
import tweepy
from datetime import datetime
from colorama import init, Fore, Back

class API_custom:

    # API instance has been used to authenticate at least once
    __valid = False

    # API instance with config details from file
    __api: tweepy.API = None

    # Each API is passed different details and given a corresponding number/uuid
    __number = None

    # When used, a timestamp will be assigned to an API instance
    __last_used: datetime = None

    # Initialize API instance
    def __init__(self, path) -> None:
        self.__login(path)


    def get_number(self):
        return self.__number


    def get_api(self) -> tweepy.API:
        return self.__api


    def is_valid(self) -> bool:
        return self.__valid

    # (Not implemented yet.)
    def get_timestamp(self):
        return self.__last_used


    def set_timestamp(self, new_time: datetime):
        self.__last_used = new_time
    

    # Login using config file details
    def __login(self, path) -> None:
        # read the config file
        config = configparser.ConfigParser()
        try:
            config.read(path)

            # Pass the config file details
            api_key = config['twitter']['API_KEY']
            api_key_secret = config['twitter']['SECRET_KEY']

            access_token = config['twitter']['ACCESS_TOKEN']
            access_token_secret = config['twitter']['SECRET_ACCESS_TOKEN']

            #bearer_token = config['twitter']['BEARER_TOKEN']

            # This is optional and has no bearing on operation
            #self.__number = config['twitter']['NUMBER']

            # Authenticate Node details
            try:
                auth = tweepy.OAuthHandler(api_key, api_key_secret)
                auth.set_access_token(access_token, access_token_secret)
                
                self.__api = tweepy.API(auth, wait_on_rate_limit = True)

                self.__valid = True
                self.__number = uuid4()

                # Print Node status
                #print(">> Authenticated: API instance {0} Running.\n".format(self.__number))
            
            except Exception as e:
                print("\t└ ERROR: Please check authentication details for API instance {0}.\n\t\t└ ".format(self.__number), e)
                self.__valid = False

        except Exception as e:
            print("\t└ ERROR: Please check authentication details for API instances")
            self.valid = False

