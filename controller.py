from node import Node
from node import Node
from init import db_connect
import os

# CONNECT TO DB #
db_connect()
 

#-------------------------------------------------------#
#   WE SEARCH FOR ALL .ini FILES IN THE GIVEN DIRECTORY #
#   THEY ARE ADDED TO AN ARRAY THEN PASSED TO NODES.    #
#-------------------------------------------------------#

nodeFiles = [f.path for f in os.scandir('/Nodes') if f.name.endswith('.ini') and f.is_file()]

#------------------------------------------------------------#
#   INITIALIZE NODES AND ADD THEM TO ARRAY IF AUTHENTICATED  #
#------------------------------------------------------------#

nodes = [Node(path) for path in nodeFiles if Node(path).is_authenticated()]

