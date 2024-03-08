import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def modularity(G, communities, total_weight):
    """
    Calculate the modularity of a partition of a graph.

    Parameters:
    - G: NetworkX graph
    - communities: list of lists containing node IDs in each community
    - total_weight: total weight of the graph
    """
    Q = 0
    m = total_weight
    for community in communities:
        for i in community:
            ki = G.degree(i)
            for j in community:
                kj = G.degree(j)
                if i != j:
                    if G.has_edge(i, j):
                        Aij = G[i][j].get('weight', 1)
                    else:
                        Aij = 0
                    Q += (Aij - (ki * kj) / (2 * m))
    return Q / (2 * m)

def leiden_algorithm(G):
    """
    Leiden algorithm for community detection in graphs.

    Parameters:
    - G: NetworkX graph

    Returns:
    - partition: dictionary containing node IDs as keys and community IDs as values
    """
    partition = {node: i for i, node in enumerate(G.nodes())}

    total_weight = sum([d.get('weight', 1) for u, v, d in G.edges(data=True)])
    mod = modularity(G, [list(G.nodes)], total_weight)

    improvement = True
    while improvement:
        improvement = False
        for node in G.nodes():
            best_mod = mod
            best_comm = partition[node]
            for neighbor in G.neighbors(node):
                if partition[node] != partition[neighbor]:
                    new_partition = partition.copy()
                    new_partition[node] = new_partition[neighbor]
                    new_mod = modularity(G, [list(comm) for comm in nx.connected_components(G.subgraph(new_partition.keys()))], total_weight)
                    if new_mod > best_mod:
                        best_mod = new_mod
                        best_comm = partition[neighbor]

            if best_comm != partition[node]:
                partition[node] = best_comm
                mod = best_mod
                improvement = True

    return partition

def draw_partitioned_graph(G, P):
    pos = nx.spring_layout(G)  # Positions for all nodes

    # Create a mapping from nodes to communities
    node_to_community = {node: comm for comm in P for node in comm}
    print(set(node_to_community.values()), len(set(node_to_community.values())))

    # Assign colors based on communities
    colors = [hash(node_to_community[node]) % 256 for node in G.nodes()]

    nx.draw(G, pos, node_color=colors, with_labels=True)
    plt.show()


if __name__ == "__main__":
    G = nx.karate_club_graph()
    
    final_Leiden_partition = leiden_algorithm(G)
    final_Leiden_partition_draw = {frozenset({node}) for node in final_Leiden_partition}
    draw_partitioned_graph(G, final_Leiden_partition_draw)