from platform import node
from node import Node
from db import db_connect
from colorama import init, Fore, Back
import os

class Controller:

    """
    It may be possible to swap between nodes rather than using multiprocessing to simultaneoulsy 
    index accounts.
    """

    __nodes = []
    __nodeFiles = []
    __connected = False

    def __init__(self) -> None:
        self.refresh_configs()
        self.connect()
    
    #-----------------------------------------------------------------#
    #
    #-----------------------------------------------------------------#

    def get_nodes(self):
        return self.__nodes


    def get_configs(self):
        return self.__nodeFiles


    def connect(self):
        # CONNECT TO DB #
        self.__connected = db_connect()


    def is_connected(self):
        return self.__connected


    def refresh_configs(self):
        #-------------------------------------------------------#
        #   WE SEARCH FOR ALL .ini FILES IN THE GIVEN DIRECTORY #
        #   THEY ARE ADDED TO AN ARRAY.                         #
        #-------------------------------------------------------#

        self.__nodeFiles = [f.path for f in os.scandir('Nodes') if f.name.endswith('.ini') and f.is_file()]

    #-----------------------------------------------------------------#
    #     
    #-----------------------------------------------------------------#

    def create_nodes(self):
        #------------------------------------------------------------#
        #   INITIALIZE NODES AND ADD THEM TO ARRAY IF AUTHENTICATED  #
        #------------------------------------------------------------#
        
        nodes = [Node(path) for path in self.__nodeFiles]
        self.__nodes = [ n for n in nodes if n.is_authenticated()]


    #-----------------------------------------------------------------#
    #
    #-----------------------------------------------------------------#

    def deploy_nodes(self):

        """
        Ideally in the final version, I want to utilize the Queue() class to have dynamically changing
        nodes within a queue to allow the user to have finer control over Nodes. This may help for scaling
        the application to a larger number of Nodes.
        """
        try:
            self.__nodes[1].scrape_user()
        except Exception as e:
            return e
    #-----------------------------------------------------------------#
    #
    #-----------------------------------------------------------------#