import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from graph_data import GraphData

def modularity(G, communities, total_edges):
    """
    Calculate the modularity of a partition of a graph.

    Parameters:
    - G: NetworkX graph
    - communities: list of lists containing node IDs in each community
    - total_edges: total number of edges in the graph
    """
    Q = 0
    m = total_edges
    for community in communities:
        for i in community:
            ki = G.degree(i)
            for j in community:
                kj = G.degree(j)
                if i != j:
                    Aij = 1 if G.has_edge(i, j) else 0
                    Q += (Aij - (ki * kj) / (2 * m))
    return Q / (2 * m)

def first_phase(G, partition, total_edges):
    """
    First phase of the Leiden algorithm.

    Parameters:
    - G: NetworkX graph
    - partition: dictionary containing node IDs as keys and community IDs as values
    - total_edges: total number of edges in the graph

    Returns:
    - partition: updated partition after the first phase
    """
    improvement = True
    while improvement:
        improvement = False
        for node in G.nodes():
            current_community = partition[node]
            best_community = current_community
            best_modularity = modularity(G, [list(comm) for comm in nx.connected_components(G.subgraph(partition.keys()))], total_edges)

            for neighbor in G.neighbors(node):
                if partition[neighbor] != current_community:
                    partition[node] = partition[neighbor]
                    mod = modularity(G, [list(comm) for comm in nx.connected_components(G.subgraph(partition.keys()))], total_edges)
                    if mod > best_modularity:
                        best_modularity = mod
                        best_community = partition[neighbor]

            if best_community != current_community:
                partition[node] = best_community
                improvement = True

    return partition

def second_phase(G, partition, total_edges):
    """
    Second phase of the Leiden algorithm.

    Parameters:
    - G: NetworkX graph
    - partition: dictionary containing node IDs as keys and community IDs as values
    - total_edges: total number of edges in the graph

    Returns:
    - partition: updated partition after the second phase
    """
    communities = {c: set() for c in set(partition.values())}
    for node, comm in partition.items():
        communities[comm].add(node)

    improvement = True
    while improvement:
        improvement = False
        for comm1, _ in communities.items():
            for comm2, nodes2 in communities.items():
                if comm1 != comm2:
                    new_partition = partition.copy()
                    for node in nodes2:
                        new_partition[node] = comm1
                    mod = modularity(G, [list(comm) for comm in nx.connected_components(G.subgraph(new_partition.keys()))], total_edges)
                    if mod > modularity(G, [list(comm) for comm in nx.connected_components(G.subgraph(partition.keys()))], total_edges):
                        partition = new_partition
                        improvement = True
                        break
            if improvement:
                break

    return partition

def leiden_algorithm(G):
    """
    Leiden algorithm for community detection in graphs.

    Parameters:
    - G: NetworkX graph

    Returns:
    - partition: dictionary containing node IDs as keys and community IDs as values
    """
    partition = {node: i for i, node in enumerate(G.nodes())}

    total_edges = G.number_of_edges()
    while True:
        partition = first_phase(G, partition, total_edges)
        partition = second_phase(G, partition, total_edges)
        new_modularity = modularity(G, [list(comm) for comm in nx.connected_components(G.subgraph(partition.keys()))], total_edges)
        if new_modularity <= modularity(G, [list(comm) for comm in nx.connected_components(G.subgraph(partition.keys()))], total_edges):
            break

    return partition

def draw_partitioned_graph(G, P):
    pos = nx.spring_layout(G)  # Positions for all nodes

    # Assign colors based on communities
    colors = [hash(P[node]) % len(P.values()) for node in G.nodes()]

    nx.draw(G, pos, node_color=colors, with_labels=True)
    plt.show()


if __name__ == "__main__":
    G = GraphData()
    final_Leiden_partition = leiden_algorithm(G.G)
    print(final_Leiden_partition)
    draw_partitioned_graph(G.G, final_Leiden_partition)