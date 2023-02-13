"""Based off of visulaizer from: https://towardsdatascience.com/visualizing-networks-in-python-d70f4cbeb259"""
import networkx as nx
from pandas import DataFrame
import pickle
from matplotlib.pyplot import figure

# Visulaize dataframe data
def generate_visual(df: DataFrame):
    Graph = nx.from_pandas_edgelist(df, 
                                source = 'followed_handle',
                                target = 'follower_handle')
    # figure(figsize = (10,8))
    nx.write_gexf(Graph, 'graph1.gexf')
    # Graph = pickle.load(open('graph1.pickle', 'rb'))
    # nx.draw(Graph)
    