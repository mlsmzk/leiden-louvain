import networkx as nx
import random
import math
import numpy as np
import matplotlib.pyplot as plt

def singleton_partition(G):
    """
    Create a partition where each node is in its own community.

    Args:
        G: The graph that will be partitioned.

    Returns:
        set of frozensets: A partition of the graph where each node is in its own singleton community.
    """
    return {frozenset({v}) for v in G.nodes()}

def make_graph(V, E):
    """
    Make a graph given vertices and edges
    Args:
        V: A set representing the partitions of the graph
        E: A list of (u,v) tuples representing edges
    """
    G = nx.Graph()
    G.add_nodes_from(V)
    G.add_edges_from(E)
    return G

class Graph():
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

    def __repr__(self):
        """
        Returns a string representation of the graph.
        """
        return f"Graph(nodes={self.nodes}, edges={self.edges})"

    def draw(self):
        """
        Draws the graph using NetworkX and Matplotlib, displaying only the numbers for each node label.
        """
        G = nx.Graph()
        # Create a mapping from frozenset nodes to numbers
        node_labels = {node: list(node)[0] for node in self.nodes}
        G.add_nodes_from(node_labels.values())
        G.add_edges_from([(node_labels[u], node_labels[v]) for u, v in self.edges])
        nx.draw(G, with_labels=True, node_color='lightblue')
        plt.show()

def draw_partitioned_graph(G, P):
    pos = nx.spring_layout(G)  # Positions for all nodes

    # Create a mapping from nodes to communities
    node_to_community = {node: comm for comm in P for node in comm}

    # Assign colors based on communities
    colors = [hash(node_to_community[node]) % 256 for node in G.nodes()]

    nx.draw(G, pos, node_color=colors, with_labels=True)
    plt.show()

from networkx.utils import groups
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
    V = P # currently set of frozensets
    
    E = []
    for (u, v) in G.edges:
        for C in P:
            for D in P:
                if u in C and v in D:
                    E.append((C, D))

    print("nodes", V)
    print("edges", E)
    return make_graph(V, E)

def recursive_size(s):
    """
    Computes ||S||, the recursive size of a set.
    E.g. {{1,2}, {3,4}, {5,6}} would return 6 despite
    the normal set size being 3.

    Args:
        s (set): A set containing frozensets.

    Returns:
        int: The size of the set of frozensets.
    """
    size = 0
    for subset in s:
        if isinstance(subset, frozenset):
            size += len(subset)
        elif isinstance(subset, set):
            size += recursive_size(subset)
    return size

def flatten_partition(P):
    """
    Flatten a partition P containing sets into one set.
    E.g. {{1,2}, {3,4}, {5,6}} -> {1,2,3,4,5,6}

    Args:
        P: A set of frozensets
    
    Returns:
        Set of ints representing nodes in P, flattened into one
    """
    return set(frozenset.union(*P))

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

# Set of functions needed for delta_H_P(v -> C)
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
        P_new.add(frozenset([node]))
    return P_new

def constant_potts_quality(G, P, gamma=1/7):
    total = 0
    for comm in P:
        E_C_C = get_edges_between_sets(comm, comm, G)
        total += E_C_C - (gamma * math.comb(recursive_size(comm), 2))
    return total

def quality_change(G, P, node, target_community):
    return constant_potts_quality(G, maybe_move_node(node, target_community, P)) - constant_potts_quality(G, P)

# gamma = 0.5
# the resolution parameter, controls the size of the communities detected by the algorithm.
# A higher value of gamma tends to result in smaller, more tightly-knit communities, while a
# lower value tends to produce larger, more inclusive communities.

# In the paper "For each network, we repeated the experiment 10 times. We used modularity with a
# resolution parameter of γ = 1 for the experiments."

# theta = 0.1
# higher value of theta increases the likelihood of accepting moves that result in a smaller
# increase in partition quality, thereby introducing more randomness into the process.

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

def refine_partition(G, P):
    P_refined = singleton_partition(G)
    for C in P:
        P_refined = merge_nodes_subset(G, P_refined, C)
    return P_refined

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
            delta = quality_change(G, P, v, C)
            if delta > best_delta:
                best_delta = delta
                best_community = C
        if best_delta > 0:
            # Find the community that currently contains v
            current_community = next((comm for comm in P if v in comm), None)
            if current_community is not None:
                # Update the partition
                P.remove(current_community)
                P.add(current_community - {v})
            if best_community is not None:
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
        print("iters", iters)
        P = move_nodes_fast(G, P)
        done = len(P) == len(G.nodes)
        if not done:
            # if iters == 2:
            #     return P
            P_refined = refine_partition(G, P)
            G = aggregate_graph(G, P_refined)
            # for C in P: # Maintain P: for each community
            #     print("C", C)
            #     new = []
            #     for v in C: # for each node
            #         curr = []
            #         if v in G.nodes: # if in G
            #             curr.append(v)
            #         curr = frozenset(curr)
            #         new.append(curr) # add to P
            # P = set(new) # convert to set
            # print(len(G.nodes), len(P))
            # print("P:\n" , P)
        iters += 1
    return flatten_partition(P)

if __name__ == "__main__":
    G = nx.karate_club_graph()
    S = {node for node, degree in G.degree() if degree >= 3}
    # print(S)
    P = singleton_partition(G)
    # print(P)

    # Test merge_subsets code
    # def test(G, partition, subset, gamma=0.5, theta=0.1):
    #     R = set()
    #     for v in subset:
    #         s = frozenset([v])
    #         # Recursive size of a set s containing one node v might have to be the degree of the node v
    #         if get_edges_between_sets(s, subset - s, G) >= gamma * recursive_size(s) * (recursive_size(subset) - recursive_size(s)):
    #             R.add(v)
    #     print("R is:\n", R)
    # test(G, P, {frozenset([1]), frozenset([32]), frozenset([14]), frozenset([23])})

    
    merge_nodes_subset(G, P, S)
    P_refined = refine_partition(G, P)
    move_nodes_fast(G, P)
    print(P)
    final_Leiden_partition = Leiden(G, P)
    final_Leiden_partition_draw = {frozenset({node}) for node in final_Leiden_partition}
    draw_partitioned_graph(G, final_Leiden_partition_draw)
