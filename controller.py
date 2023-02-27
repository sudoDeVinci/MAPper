from multiprocessing import Process
from worker import Worker
from api_instance import API_custom
from db import db_connect
from dbservices import get_follower_relationships
from vis import generate_visual
from colorama import init, Fore, Back
from pandas import DataFrame
import os

class Controller:

    """
    outdated, need to rewrite
    """

    # These api credentials are for finding followers of a user
    __api_list = []
    __api_files = []

    # Whether the database can be successfully connected to
    __connected = False

    __workers: list[Worker] = None

    __processes: list[Process] = None 


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

    def visualize_followers(self, num: int) -> int:
        df = get_follower_relationships(num)
        generate_visual(df, num)
        return 0

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

        self.__workers = [Worker(self.__api_list[i]) for i in range(len(self.__api_list))]
        self.__processes = [Process(target = w.scrape_user) for w in self.__workers]
        try:
            for p in self.__processes: p.start()
            for p in self.__processes: p.join()
        except Exception as e:
            print(e)
        
        return 0
    #-----------------------------------------------------------------#
    #
    #-----------------------------------------------------------------#

# Take in user input and convert to integer

def stdin_int(prompt: str) -> int:
    while(True):
        num: str = input(f"\033[0;36m>> {prompt}: \033[0m").strip()
        try:
            num = int(num)
            if num < 0:
                print(f"\n\033[91mERROR: Sample Size must be positive.\033[0m\n")
                continue
            return num
        except ValueError as e:
            print(f"\n\033[91mERROR: {num} Input is not an integer.\033[0m\n")
            continue