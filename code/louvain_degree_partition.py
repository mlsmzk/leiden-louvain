import networkx as nx
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from graph_data import GraphData

def degree_partition(G):
    """
    Create a partition where nodes with the same degree are in the same community.

    Args:
        G: The graph that will be partitioned.

    Returns:
        set of frozensets: A partition of the graph where nodes with the same degree are in the same community.
    """
    # Get the degree of each node
    degrees = {v: G.degree(v) for v in G.nodes()}
    
    # Group nodes by their degree
    communities = collections.defaultdict(set)
    for node, degree in degrees.items():
        communities[degree].add(node)

    return {frozenset(community) for community in communities.values()}

class Graph:
    """
    Represents a graph with a set of nodes and edges.

    Attributes:
        nodes (set): The set of nodes in the graph.
        edges (set): The set of edges in the graph, where each edge is represented as a tuple (node1, node2).
    """

    def __init__(self, nodes, edges):
        """
        Initializes a new Graph object.

        Args:
            nodes (set): The set of nodes for the graph.
            edges (set): The set of edges for the graph, where each edge is represented as a tuple (node1, node2).
        """
        self.nodes = nodes
        self.edges = edges
        self.G = nx.Graph()
        # Create a mapping from frozenset nodes to numbers
        node_labels = {node: list(node)[0] for node in self.nodes}
        self.G.add_nodes_from(node_labels.values())
        self.G.add_edges_from([(node_labels[u], node_labels[v]) for u, v in self.edges])

    def __repr__(self):
        """
        Returns a string representation of the graph.
        """
        return f"Graph(nodes={self.nodes}, edges={self.edges})"

    def draw(self, with_labels=True):
        """
        Draws the graph using NetworkX and Matplotlib, displaying only the numbers for each node label.
        """

        nx.draw(self.G, node_size=50, with_labels=with_labels, node_color='lightblue')
        plt.show()


def aggregate_graph(G, P):
    """
    Creates an aggregate graph where each community in the partition becomes a node, and an edge is added between two nodes
    if there is at least one edge between the corresponding communities in the original graph.

    Args:
        G (graph): The original graph.
        P (set): The partition of the graph.

    Returns:
        Graph: The aggregate graph.
    """
    V = P
    E = set()
    for (u, v) in G.edges:
        for C in P:
            for D in P:
                if u in C and v in D:
                    E.add((C, D))
    return Graph(V, E)



# num of edges between community C and community D, for instance
def get_edges_between_two_comms(comm1, comm2, G, P):
    res = 0
    # Convert the set of frozensets to a dictionary
    P_dict = {node: comm for comm in P for node in comm}
    members1 = [node for node in G.nodes if P_dict[node] == comm1]
    members2 = [node for node in G.nodes if P_dict[node] == comm2]
    for node in members1:
        res += len(set(members2) & set(G[node]))
    return res

def get_edges_between_communities(G, P):
    counts = {}
    for i, k1 in enumerate(P):
        for j, k2 in enumerate(P):
            if i <= j:
                counts[k1, k2] = get_edges_between_two_comms(k1, k2, G, P)
    return counts

def H(G, P, gamma=1/7):
    total = 0
    counts = get_edges_between_communities(G, P)  # E(C,D) in the paper
    for comm in P:
        comm_size = len(comm)
        total += counts[comm, comm] - (gamma * math.comb(comm_size, 2))
    return total

def maybe_move_node(node, community, P):
    P_new = set()
    node_moved = False
    for comm in P:
        if node in comm and comm != community:
            P_new.add(comm - {node})
        else:
            P_new.add(comm)
    for comm in P_new:
        if comm == community:
            P_new.remove(comm)
            P_new.add(comm | {node})
            node_moved = True
            break
    if not node_moved:
        P_new.add(frozenset({node}))
    return P_new


def move_node(node, community, P):
    P_new = set()
    node_moved = False
    for comm in P:
        if node in comm and comm != community:
            P_new.add(comm - {node})
        else:
            P_new.add(comm)
    for comm in P_new:
        if comm == community:
            P_new.remove(comm)
            P_new.add(comm | {node})
            node_moved = True
            break
    if not node_moved:
        P_new.add(frozenset({node}))
    return P_new


def move_nodes(G, P, gamma=1/7):
    H_old = H(G, P, gamma)
    improvement = True
    while improvement:
        improvement = False
        for node in G.nodes():
            best_community = None
            best_increase = 0
            for community in P.union({frozenset()}):
                P_new = maybe_move_node(node, community, P)
                increase = H(G, P_new, gamma) - H_old
                if increase > best_increase:
                    best_increase = increase
                    best_community = community
            if best_increase > 0:
                P = move_node(node, best_community, P)
                H_old = H(G, P, gamma)
                improvement = True
    return P

import networkx as nx
import matplotlib.pyplot as plt

def draw_partitioned_graph(G, P):
    pos = nx.spring_layout(G)  # Positions for all nodes

    # Create a mapping from nodes to communities
    node_to_community = {node: comm for comm in P for node in comm}

    # Assign colors based on communities
    colors = [hash(node_to_community[node]) % 256 for node in G.nodes()]

    nx.draw(G, pos, node_color=colors, with_labels=True, font_size=8)  # Set font size to 8
    plt.show()


def flattened(P):
    return set(frozenset.union(*P))

def Louvain(G, P):
    done = False
    iteration = 0
    while not done:
        P = move_nodes(G, P)
        print(f"Iteration {iteration}:")
        draw_partitioned_graph(G, P)
        done = len(P) == len(G.nodes())  # Terminate when each community consists of only one node
        if not done:
            G = aggregate_graph(G, P)
            P = degree_partition(G)
        iteration += 1
    return flattened(P)


if __name__ == "__main__":
    # G = nx.karate_club_graph()
    G = GraphData()

    P = degree_partition(G.G)
    # print(P)

    agg_graph = aggregate_graph(G.G,P)

    # G.draw(h=True)
    # agg_graph.draw()

    Louvain(G.G, P)
