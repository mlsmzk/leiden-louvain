import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math

def modularity(G, P):
    """
    Calculates the modularity of a partition of a graph.

    Args:
        G (Graph): The graph.
        P (set): The partition of the graph, where each element is a set representing a community.

    Returns:
        float: The modularity of the partition.
    """
    m = len(G.edges)
    modularity_value = 0
    for C in P:
        L_C = sum(1 for (u, v) in G.edges if u in C and v in C)
        D_C = sum(sum(1 for (_, v) in G.edges if v in C) for node in C)
        modularity_value += (L_C / m) - (D_C / (2 * m)) ** 2
    return modularity_value

def singleton_partition(G):
    """
    Create a partition where each node is in its own community.

    Args:
        G: The graph that will be partitioned.

    Returns:
        set of frozensets: A partition of the graph where each node is in its own singleton community.
    """
    return [[v] for v in G.nodes()]

def aggregate_graph(P):
    G = nx.Graph()
    G.add_nodes_from(P)
    for (u, v) in G.edges:
        for C in P:
            for D in P:
                if u in C and v in D:
                    G.add_edge(C, D)
    return G

def locate_community(node, P):
    return next(comm for comm in P if node in comm)

def partition_quality_change(G, P, v_community, C):
    """
    Calculates the change in modularity when moving a node to a different community.

    Args:
        G (Graph): The graph.
        P (set): The current partition of the graph.
        v (frozenset): The node to be moved.
        C (frozenset): The community to which the node will be moved.

    Returns:
        float: The change in modularity.
    """
    # Create a new partition without v in its current community
    v = v_community[0]
    new_partition = P.copy()
    new_partition.remove([v])

    # is it necessary to keep the same number of communities?
    new_partition.append([])

    # Add v to the target community C
    if C in new_partition:
        new_partition.remove(C)
        new_partition.append(C + [v])
    else:
        new_partition.append([v])

    current_modularity = modularity(G, P)
    new_modularity = modularity(G, new_partition)
    return new_modularity - current_modularity

gamma = 0.5
theta = 0.1
def merge_nodes_subset(G, P, S):
    """
    Refines a given partition of a graph by merging well-connected nodes within a specified subset into communities.

    Args:
        G (dict): The graph inputted, where keys are nodes and values are dictionaries
                  of neighboring nodes with edge weights.
        P (dict): The current partition of the graph, where keys are nodes and values are communities.
        S (set): The subset of nodes within which to merge well-connected nodes.

    Returns:
        dict: The updated partition of the graph after merging well-connected nodes within the subset.
    """
    # Calculate the degree of each node and the subset
    k = {v: len(G[v]) for v in S}
    k_S = sum(k.values())

    # Consider only nodes that are well connected within the subset
    R = {v for v in S if sum(1 for u in G[v] if u in S and u != v) >= gamma * k[v] * (k_S - k[v])}

    for v in R:
        # Consider only nodes that are in singleton communities
        if [v] in P:
            # Consider only well-connected communities
            T = {C for C in P if C.issubset(S) and
                 sum(1 for u in C for w in S - C if w in G[u]) >= gamma * sum(k[u] for u in C) * (k_S - sum(k[u] for u in C))}

            # Find the community v is in
            current_community = locate_community(v, P)
            # Choose a random community to move the node to, based on a probability proportional to the change in partition quality
            delta_hp = {C: partition_quality_change(G, P, current_community, C) for C in T}
            prob = {C: np.exp(1 / theta * delta_hp[C]) if delta_hp[C] >= 0 else 0 for C in T}
            total_prob = sum(prob.values())
            if total_prob > 0:
                prob = {C: p / total_prob for C, p in prob.items()}
                chosen_community = np.random.choice(list(T), p=list(prob.values()))
                # Update P by removing v from its current community and adding it to the chosen community
                P.remove([v])
                P.append(chosen_community + [v])

    return P

def refine_partition(G, P):
    P_refined = singleton_partition(G)
    for comm in P:
        P_refined = merge_nodes_subset(G, P, comm)
    return P_refined

def move_nodes_fast(G, P):
    queue = []
    while len(queue) > 0:
        v = queue.pop(0)
        v_community = locate_community(v, P)
        possibilities = {comm : partition_quality_change(G, P, v_community, comm) for comm in P}
        best_comm = max(possibilities, key=possibilities.values())
        if best_comm > 0:
            P.remove(v_community)
            v_community.remove(v)
            P.append(v_community)
            P.remove(best_comm)
            best_comm.append(v)
            P.append(best_comm)
            for neighbor in G[v]:
                if neighbor not in best_comm:
                    queue.append(neighbor)

    return P

def leiden_algorithm(G):
    """
    Leiden algorithm for community detection in graphs.

    Parameters:
    - G: NetworkX graph

    Returns:
    - partition: dictionary containing node IDs as keys and community IDs as values
    """
    partition = singleton_partition(G)
    partition = move_nodes_fast(G, partition)

    done = False
    iters = 0
    while not done:
        print("iter", iters)
        done = len(G) == len(partition)
        if not done:
            P_refined = refine_partition(G, partition)
            G = aggregate_graph(G, P_refined)
            partition = [[v for v in C if v in G] for C in partition]
        iters += 1

    return partition

def flatten_extend(t):
    flat_list = []
    for row in t:
        flat_list.extend(row)
    return flat_list

def draw_partitioned_graph(G, P):
    pos = nx.spring_layout(G)  # Positions for all nodes

    # Create a mapping from nodes to communities

    node_to_community = {}
    for comm in P:
        for node in comm:
            node_to_community[node] = comm
    # print(set(node_to_community.values()), len(set(node_to_community.values())))

    # Assign colors based on communities
    colors = [hash(frozenset(node_to_community[node])) % len(node_to_community.values()) for node in G.nodes()]

    nx.draw(G, pos, node_color=colors, with_labels=True)
    plt.show()


if __name__ == "__main__":
    G = nx.karate_club_graph()
    
    final_Leiden_partition = leiden_algorithm(G)
    print(final_Leiden_partition)
    draw_partitioned_graph(G, final_Leiden_partition)