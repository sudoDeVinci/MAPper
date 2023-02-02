from array import array
from node import Worker as Node
from platform import node
from api_instance import API_custom
from db import db_connect
from colorama import init, Fore, Back
import os

class Controller:

    """
    outdated, need to rewrite
    """

    # These api credentials are for finding followers of a user
    __api_list = []
    __api_files = []

    # Whether the database can be successfully connected to
    __connected: bool = False

    """
    For now, we are using only one Node instance. In the future, it will be completely possible to use multiple in parallel for
    faster scraping, but this will require almost double the number of api credentials. I don't feel like opening 20 twitter accounts
    right now.
    """
    __node = None


    def __init__(self) -> None:
        self.connect()
        if self.__connected == True:
            self.refresh_configs()
    
    #-----------------------------------------------------------------#
    #
    #-----------------------------------------------------------------#

    def get_api_list(self) -> list[API_custom]:
        return self.__api_list


    def connect(self) -> None:
        # CONNECT TO DB #
        self.__connected = db_connect()


    def is_connected(self) -> bool:
        return self.__connected


    def refresh_configs(self) -> None:
        #-------------------------------------------------------#
        #   WE SEARCH FOR ALL .ini FILES IN THE GIVEN DIRECTORY #
        #   THEY ARE ADDED TO AN ARRAY.                         #
        #-------------------------------------------------------#

        self.__api_files = [f.path for f in os.scandir('credentials') if f.name.endswith('.ini') and f.is_file()]
        self.__create_api_list()
    #-----------------------------------------------------------------#
    #     
    #-----------------------------------------------------------------#

    def __create_api_list(self) -> None:
        #------------------------------------------------------------#
        #   INITIALIZE API instances AND ADD THEM TO ARRAY IF AUTHENTICATED  #
        #------------------------------------------------------------#
        """
        We pass the paths to the custom API objects and add those who can be used to authenticate. 
        """
        creds = [API_custom(path) for path in self.__api_files]
        self.__api_list = [ n for n in creds if n.is_valid()]

    #-----------------------------------------------------------------#
    #
    #-----------------------------------------------------------------#

    def deploy(self) -> int:

        """
        Ideally in the final version, I want to utilize the Queue() class to have dynamically changing
        credentials within a queue to allow the user to have finer control over creds. This may help for scaling
        the application to a larger number of creds.
        """
        

        """
        Right now I',m only passing a single api object, but in the future,
        I would pass the entire list 
        """
        self.__node = Node(self.__api_list[0])
        try:
            self.__node.scrape_user()
        except Exception as e:
            print(e)
        
        return 0
    #-----------------------------------------------------------------#
    #
    #-----------------------------------------------------------------#