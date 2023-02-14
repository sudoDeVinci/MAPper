from pandas import DataFrame
# Visualize network graph from dataframe
def generate_visual(df: DataFrame) -> None:
    import networkx as nx
    import matplotlib.pyplot as plt
    from dbservices import get_follower_relationships

    print(">> Constructing network Graph ...")    
    df = get_follower_relationships()

    print(">> Visualizing network graph...")
    G = nx.from_pandas_edgelist(df,'followed_handle', 'follower_handle', create_using=nx.DiGraph(), edge_attr='zoo')
    
    print(">> Plotting ...")
    nx.draw(G, nx.kamada_kawai_layout(G), with_labels = True, arrowsize = 1, node_size = 70, alpha = 0.75, font_size = 3, font_color = 'black', edge_color = 'grey', node_color = 'red', width = 0.5)


    plt.title("Network Visualization Graph")
    plt.savefig('graphs/network.png', dpi = 3000, format = 'png', bbox_inches = 'tight', transparent = True)
    print('>> Done.')
