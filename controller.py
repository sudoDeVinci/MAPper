from node import Node
from db import db_connect
from multiprocessing import Process
import colorama
import os

class Controller:

    """
    It may be possible to swap between nodes rather than using multiprocessing to simultaneoulsy 
    index accounts.
    """

    __nodes = []
    __nodeFiles = []

    def __init__(self) -> None:
        self.refresh_configs()
        self.connect()

    def node_count(self):
        return len(self.__nodeFiles)

    def connect(self):
        # CONNECT TO DB #
        db_connect()
    
    def refresh_configs(self):
        #-------------------------------------------------------#
        #   WE SEARCH FOR ALL .ini FILES IN THE GIVEN DIRECTORY #
        #   THEY ARE ADDED TO AN ARRAY.                         #
        #-------------------------------------------------------#

        self.__nodeFiles = [f.path for f in os.scandir('Nodes') if f.name.endswith('.ini') and f.is_file()]

    def create_nodes(self):
        #------------------------------------------------------------#
        #   INITIALIZE NODES AND ADD THEM TO ARRAY IF AUTHENTICATED  #
        #------------------------------------------------------------#

        self.__nodes = [Node(path) for path in self.__nodeFiles if Node(path).is_authenticated()]

    def deploy_nodes(self, init_users):

        """
        Ideally in the final version, I want to utilize the Queue() class to have dynamically changing
        nodes within a queue to allow the user to have finer control over Nodes. This may help for scaling
        the application to a larger number of Nodes.
        """

        processes = [Process(target=node.scrape_user(), args=user_at) for node, user_at in zip(self.__nodes, init_users)]
        for p in processes:
            p.start()
            p.join()