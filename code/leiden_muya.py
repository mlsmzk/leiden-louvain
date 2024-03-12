import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math

def singleton_partition(G):
    """
    Create a partition where each node is in its own community.

    Args:
        G: The graph that will be partitioned.

    Returns:
        set of frozensets: A partition of the graph where each node is in its own singleton community.
    """
    return {frozenset({v}) for v in G.nodes()}

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
    G = nx.Graph()
    G.add_nodes_from(V)
    G.add_edges_from(E)
    return G

def flatten_partition(P):
    return set(frozenset.union(*P))

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

def partition_quality_change(G, P, v, C):
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
    # Find the community that currently contains v
    current_community = next(comm for comm in P if v in comm)

    # Create a new partition without v in its current community
    new_partition = P.copy()
    new_partition.remove(current_community)
    new_partition.add(current_community - {v})

    # Add v to the target community C
    if C in new_partition:
        new_partition.remove(C)
        new_partition.add(C.union({v}))
    else:
        new_partition.add(frozenset({v}))

    current_modularity = modularity(G, P)
    new_modularity = modularity(G, new_partition)
    return new_modularity - current_modularity

gamma = 0.5
# the resolution parameter, controls the size of the communities detected by the algorithm.
# A higher value of gamma tends to result in smaller, more tightly-knit communities, while a
# lower value tends to produce larger, more inclusive communities.

# In the paper "For each network, we repeated the experiment 10 times. We used modularity with a
# resolution parameter of γ = 1 for the experiments."

theta = 0.1
# higher value of theta increases the likelihood of accepting moves that result in a smaller
# increase in partition quality, thereby introducing more randomness into the process.

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
        if frozenset({v}) in P:
            # Consider only well-connected communities
            T = {C for C in P if C.issubset(S) and
                 sum(1 for u in C for w in S - C if w in G[u]) >= gamma * sum(k[u] for u in C) * (k_S - sum(k[u] for u in C))}

            # Choose a random community to move the node to, based on a probability proportional to the change in partition quality
            delta_hp = {C: partition_quality_change(G, P, v, C) for C in T}
            prob = {C: np.exp(1 / theta * delta_hp[C]) if delta_hp[C] >= 0 else 0 for C in T}
            total_prob = sum(prob.values())
            if total_prob > 0:
                prob = {C: p / total_prob for C, p in prob.items()}
                chosen_community = np.random.choice(list(T), p=list(prob.values()))
                # Update P by removing v from its current community and adding it to the chosen community
                P.remove({v})
                P.add(chosen_community | {v})

    return P

def refine_partition(G, P):
    prefinined = singleton_partition(G)
    for C in P:
        prefinined = merge_nodes_subset(G, prefinined, C)
    return prefinined

def move_nodes_fast(G, P):
    """
    Moves nodes to different communities to improve the partition quality of the graph.

    Args:
        G (Graph): The graph for which the partition is being optimized.
        P (set): The current partition of the graph, where each element is a set representing a community.

    Returns:
        set: The optimized partition of the graph.
    """
    Q = list(G.nodes)
    while Q:
        v = Q.pop(0)
        best_delta = 0
        best_community = None
        for C in P.union({frozenset()}):
            delta = partition_quality_change(G, P, v, C)
            if delta > best_delta:
                best_delta = delta
                best_community = C
        if best_delta > 0:
            # Find the community that currently contains v
            current_community = next(comm for comm in P if v in comm)
            # Update the partition
            P.remove(current_community)
            P.add(current_community - {v})
            if best_community in P:
                P.remove(best_community)
                P.add(best_community.union({v}))
            else:
                P.add(frozenset({v}))
            # Update the queue
            N = {u for (u, _) in G.edges if u not in best_community}
            Q.extend(list(N - set(Q)))
    return P


def Leiden(G, initial_partition=None):
    """
    Executes the Leiden algorithm to detect communities in a graph.

    Args:
        G (Graph): The graph for which communities are to be detected.
        initial_partition (set, optional): An initial partition of the graph. If not provided, a singleton
            partition is used as the starting point.

    Returns:
        set: The final partition of the graph, where each element is a set representing a community.
    """
    if initial_partition is None:
        P = singleton_partition(G)
    else:
        P = initial_partition
    done = False
    iters = 0
    while not done:
        print(iters)
        iters += 1
        P = move_nodes_fast(G, P)
        done = len(P) == len(G.nodes)
        if not done:
            prefinined = refine_partition(G, P)
            G = aggregate_graph(G, prefinined)
            P = {frozenset({v for v in C if v in G.nodes}) for C in P}
    return flatten_partition(P)

if __name__ == "__main__":
    G = nx.karate_club_graph()
    P = singleton_partition(G)
    final_Leiden_partition = Leiden(G, P)
    final_Leiden_partition_draw = {frozenset({node}) for node in final_Leiden_partition}
