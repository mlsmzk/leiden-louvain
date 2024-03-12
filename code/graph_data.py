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
        self.H = nx.Graph()
        for _, row in df_nodes.iterrows():
            # Assuming the first column contains node labels
            node_label = row[0]
            # Assuming the 'group' column contains community labels
            community = row['group']
            self.G.add_node(node_label, group=community)
            self.H.add_node(node_label)

        # Assign a color to each community
        communities = set(nx.get_node_attributes(self.G, 'group').values())
        print(communities)

        community_colors = {}
        for idx, community in enumerate(communities):
            community_colors[community] = plt.cm.tab10(idx)

        # Create a list of node colors based on their communities
        self.node_colors = [community_colors[self.G.nodes[node]['group']] for node in self.G.nodes()]

        edges_data = [(row['source'], row['target']) for _, row in df_edges.iterrows()] #  {'weight': row['value']}
        self.G.add_edges_from(edges_data)
        self.H.add_edges_from(edges_data)

    def draw(self, h=False):
        if h:
            nx.draw(self.H, node_size=50) # , with_labels=True
            plt.show()
            return
        nx.draw(self.G, with_labels=True, node_size=50, node_color=self.node_colors) # , with_labels=True
        plt.show()


if __name__ == "__main__":
    graph = GraphData()
    graph.draw(h=False)