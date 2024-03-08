import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math

# def modularity(G, communities, total_weight):
#     """
#     Calculate the modularity of a partition of a graph.

#     Parameters:
#     - G: NetworkX graph
#     - communities: list of lists containing node IDs in each community
#     - total_weight: total weight of the graph
#     """
#     Q = 0
#     m = total_weight
#     for community in communities:
#         for i in community:
#             ki = G.degree(i)
#             for j in community:
#                 kj = G.degree(j)
#                 if i != j:
#                     if G.has_edge(i, j):
#                         Aij = 1
#                     else:
#                         Aij = 0
#                     Q += (Aij - (ki * kj) / (2 * m))
#     return Q / (2 * m)


def modularity(G, communities, gamma=1/7):
    total = 0
    for comm in communities:
        E_C_C = get_edges_between_sets(comm, comm, G)
        total += E_C_C - (gamma * math.comb(len(comm), 2))
    return total

def get_edges_between_sets(sub1, sub2, G):
    """
    Get the number of edges between two subsets or partitions in G.
    Will fail if there is overlap between the sets.

    Args:
        sub1: frozenset iterable containing nodes (int) in G
        sub2: frozenset iterable containing nodes (int) in G
        G: nx.graph containing sub1 and sub2
    
    Returns:
        Int representing the number of edges between the two sets
    """
    edges = []
    for u in sub1:
        for v in sub2:
            if v in G[u] and (u,v) not in edges and (v,u) not in edges:
                edges.append((u,v))
    return len(edges)

# def modularity(G, P):
#     """
#     Calculates the modularity of a partition of a graph.

#     Args:
#         G (Graph): The graph.
#         P (set): The partition of the graph, where each element is a set representing a community.

#     Returns:
#         float: The modularity of the partition.
#     """
#     m = len(G.edges)
#     modularity_value = 0
#     for C in P:
#         L_C = sum(1 for (u, v) in G.edges if u in C and v in C)
#         D_C = sum(sum(1 for (_, v) in G.edges if v in C) for node in C)
#         modularity_value += (L_C / m) - (D_C / (2 * m)) ** 2
#     return modularity_value

def singleton_partition(G):
    """
    Create a partition where each node is in its own community.

    Args:
        G: The graph that will be partitioned.

    Returns:
        set of frozensets: A partition of the graph where each node is in its own singleton community.
    """
    return {frozenset({v}) for v in G.nodes()}

def merge_nodes_subset(G, partition, subset, gamma=0.5, theta=0.1):
    R = set()
    for v in subset:
        s = frozenset([v])
        # Recursive size of a set s containing one node v might have to be the degree of the node v
        if get_edges_between_sets(s, subset - s, G) >= gamma * recursive_size(set(s)) * (recursive_size(subset) - recursive_size(set(s))):
            R.add(v)

    for node in R:
        if frozenset({node}) in partition: # If v is a singleton community
            T = set()
            for comm in partition:
                well_connected = gamma * recursive_size(comm) * (recursive_size(subset) - recursive_size(comm))
                if comm.issubset(subset) and get_edges_between_sets(comm, subset-comm, G) >= well_connected:
                    T.add(comm)
            delta_hp = {C: quality_change(G, partition, node, C) for C in T}
            prob = {C: np.exp(1 / theta * delta_hp[C]) if delta_hp[C] >= 0 else 0 for C in T}
            total_prob = sum(prob.values())
            if total_prob > 0:
                prob = {C: p / total_prob for C, p in prob.items()}
                chosen_community = np.random.choice(list(T), p=list(prob.values()))
                partition = {C - {v} if v in C else C for C in partition}
                partition.add(chosen_community | {v})
    return partition

def refine_partition(G, partition):
    P_refined = singleton_partition(G)
    for C in partition:
        P_refined = merge_nodes_subset(G, P_refined, C)
    return P_refined



def leiden_algorithm(G):
    """
    Leiden algorithm for community detection in graphs.

    Parameters:
    - G: NetworkX graph

    Returns:
    - partition: dictionary containing node IDs as keys and community IDs as values
    """
    partition = {node: i for i, node in enumerate(G.nodes())}
    mod = modularity(G, [list(G.nodes)])

    improvement = True
    iters = 0
    while improvement:
        print("iter", iters)
        improvement = False
        for node in G.nodes():
            best_mod = mod
            best_comm = partition[node]
            for neighbor in G.neighbors(node):
                if partition[node] != partition[neighbor]:
                    refine_partition(G, partition)
                    new_partition = partition.copy()
                    new_partition[node] = new_partition[neighbor]
                    new_mod = modularity(G, [list(comm) for comm in nx.connected_components(G.subgraph(new_partition.keys()))])
                    # print(best_mod, new_mod)
                    if new_mod > best_mod:
                        best_mod = new_mod
                        best_comm = partition[neighbor]

            if best_comm != partition[node]:
                partition[node] = best_comm
                mod = best_mod
                improvement = True
            iters += 1

    return partition

def draw_partitioned_graph(G, P):
    pos = nx.spring_layout(G)  # Positions for all nodes

    # Create a mapping from nodes to communities
    node_to_community = {node: comm for comm in P for node in comm}
    # print(set(node_to_community.values()), len(set(node_to_community.values())))

    # Assign colors based on communities
    colors = [hash(node_to_community[node]) % len(node_to_community.values()) for node in G.nodes()]

    nx.draw(G, pos, node_color=colors, with_labels=True)
    plt.show()


if __name__ == "__main__":
    G = nx.karate_club_graph()
    
    final_Leiden_partition = leiden_algorithm(G)
    # print(final_Leiden_partition)
    final_Leiden_partition_draw = {frozenset({node}) for node in final_Leiden_partition}
    draw_partitioned_graph(G, final_Leiden_partition_draw)