import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame

class GraphData:
    def __init__(self):
        df_nodes = pd.read_csv("./data/stack_network_nodes.csv")
        df_edges = pd.read_csv("./data/stack_network_links.csv")
        # print(df_nodes)
        # print(df_edges)
        self.G = nx.Graph()
        community = df_nodes['group']
        self.G.add_nodes_from(df_nodes['name'], group=community) #size=df_nodes['nodesize']

        # Assign a color to each community
        community_colors = {}
        for idx, community in enumerate(df_nodes['group']):
            community_colors[community] = plt.cm.tab10(idx)

        # Create a list of node colors based on their communities
        self.node_colors = [community_colors[self.G.nodes[node]['group']] for node in self.G.nodes()]

        edges_data = [(row['source'], row['target']) for _, row in df_edges.iterrows()] #  {'weight': row['value']}
        self.G.add_edges_from(edges_data)

    def __repr__(self):
        nx.draw(self.G, node_size=50, node_color=self.node_colors) # , with_labels=True
        plt.show()


if __name__ == "__main__":
    G = GraphData()
    print(G)