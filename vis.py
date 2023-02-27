from pandas import DataFrame
# Visualize network graph from dataframe
def generate_visual(df: DataFrame, num: int) -> None:
    import networkx as nx
    import matplotlib.pyplot as plt
    from dbservices import get_follower_relationships

    print(">> Constructing Network ...")    
    df = get_follower_relationships(num)

    print(">> Visualizing Network Data ...")
    G = nx.from_pandas_edgelist(df,'followed_handle', 'follower_handle', create_using=nx.DiGraph(), edge_attr='zoo')
    
    print(">> Plotting Network Graph ...")
    nx.draw(G, nx.kamada_kawai_layout(G), with_labels = True, arrowsize = 1, node_size = 20, alpha = 0.70, font_size = 1, font_color = 'black', edge_color = 'grey', node_color = 'red', width = 0.3)
    plt.title("Network Visualization Graph", color = 'white')
    
    print(">> Saving Graph...")
    plt.savefig('graphs/network_test.png', dpi = 3000, format = 'png', bbox_inches = 'tight', transparent = True)
    print('>> Done.')
