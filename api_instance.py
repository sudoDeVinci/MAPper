import configparser
from uuid import uuid4, UUID
import tweepy
from datetime import datetime
from colorama import init, Fore, Back

class API_custom:
    """
    Wrapper around Tweepy API object.
    """

    __slots__ = ('_valid', '_api', '_number','_last_used','_init_poi')

    # API instance has been used to authenticate at least once
    _valid: bool = False

    # API instance with config details from file
    _api: tweepy.API = None

    # Each API is passed different details and given a corresponding number/uuid
    _number: UUID = None

    # When used, a timestamp will be assigned to an API instance
    _last_used: datetime = None

    # Initial poi
    _init_poi: str = None


    # Initialize API instance
    def __init__(self, path) -> None:
        self._login(path)


    def get_init_poi(self):
        return self._init_poi


    def get_number(self):
        return self._number


    def get_api(self) -> tweepy.API:
        return self._api


    def is_valid(self) -> bool:
        return self._valid


    # (Not implemented yet.)
    def get_timestamp(self):
        return self._last_used


    def set_timestamp(self, new_time: datetime):
        self._last_used = new_time
    

    # Login using config file details
    def _login(self, path) -> None:
        # read the config file
        config = configparser.ConfigParser()
        try:
            config.read(path)

            # Pass the config file details
            api_key = config['twitter']['API_KEY']
            api_key_secret = config['twitter']['SECRET_KEY']

            access_token = config['twitter']['ACCESS_TOKEN']
            access_token_secret = config['twitter']['SECRET_ACCESS_TOKEN']

            # Authenticate Node details
            try:
                auth = tweepy.OAuthHandler(api_key, api_key_secret)
                auth.set_access_token(access_token, access_token_secret)
                
                self._api = tweepy.API(auth, wait_on_rate_limit = True)

                self._valid = True
                self._number = uuid4()
                self._init_poi = config['twitter']['INITIAL_POI']

                # Print Node status
                #print(">> Authenticated: API instance {0} Running.\n".format(self.__number))
            
            except Exception as e:
                print("\t└ ERROR: Please check authentication details for API instance {0}.\n\t\t└ ".format(self._number))
                self._valid = False

        except Exception as e:
            print("\t└ ERROR: Please check authentication details for API instances")
            self.valid = False

