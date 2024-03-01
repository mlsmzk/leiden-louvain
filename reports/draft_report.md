# “Eliminating Disconnected Communities: A Comparative Study on Louvain and Leiden”

### Abstract

The Louvain algorithm is a known algorithm for identifying communities within a graph. One weakness of the algorithm is its tendency to group nodes that are not well connected as a subgraph. In this paper, we explore why this is a weakness of the Louvain algorithm, and how the Leiden algorithm, which is an improvement upon its predecessor, is a marked improvement; most notably in its removal of poorly connected communities.

### Annotated Bibliography

[From Louvain to Leiden: Guaranteeing Well-Connected Communities V.A. Traag, L. Waltman, and N.J. van Eck](https://arxiv.org/pdf/1810.08473.pdf)

This paper is the paper we are replicating for this project. It introduces the Leiden algorithm, a community detection method developed to improve upon the Louvain algorithm, a widely-used approach for identifying communities in networks. The Louvain algorithm has been criticized for producing poorly connected or even disconnected communities, which can be problematic for clustering and interpreting the communities of complex networks. To overcome this issue, the authors propose the Leiden algorithm, which guarantees the connectivity of communities by ensuring that all subsets of all communities are locally optimally assigned. This is achieved through a refined optimization process that includes fast local moves and random neighbor moves, leading to improved speed and quality of community partitions compared to the Louvain algorithm. The paper provides a detailed description of both the Louvain and the Leiden algorithms, and a comparative analysis between them, demonstrating its superior performance of the Leiden algorithm in terms of creating more well-communities and efficiency.
After doing more in-depth research on the topic, we decided that this paper is the only source we will be employing. The reason is that there are very few research papers written about the Leiden algorithm to begin with, and their contents largely overlap with this paper. Moreover, all of them analyze the algorithm from the perspective of how Leiden improves upon Louvain, and none of them have reached the comprehensiveness of this paper. Therefore, we believe this paper is sufficient for our project.

### The Experiment

The primary finding of the paper is that the Leiden algorithm repairs Louvain’s weakness of creating badly connected communities. In our simulations, we verify the truth of the Louvain algorithm’s initial flaw and that the Leiden algorithm indeed bridges this gap. Our extension is to find data on communities from a real source to compare node membership found by the Leiden algorithm to real partition formation. One such source of data would’ve been Reddit, though further research has shown Reddit is not usable for the project due to its privacy policy. Once the data is obtained, we can extend the paper’s findings by performing analysis on the quality of data fit.

### Preliminary Results

We have run through both of the models on the small network data “Zachary’s Karate Club”. Zachary's Karate Club is a built-in dataset of the python library NetworkX, and it is a well-known social network dataset that represents the friendships between 34 members of a karate club at a US university in the 1970s that is often used for testing and as a benchmark in social network analysis, community detection, and graph clustering research, including the academic paper we are replicating in this project.
It is important to note that the karate club eventually split into two separate clubs due to a conflict between the instructor (node 0) and the club president (node 33), and by only looking at the network before community detection, it is pretty obvious that there are two loosely formed clusters around note 0 and node 33.

### Interpretation

As shown in the Figure in our codes, the Louvain model separated the graph into four communities, as represented by different colors. By looking at the graph, it is clear that node 9 is poorly connected to the rest of its community, and the community consisting of nodes 24, 25, 28, and 31 is somewhat interfered with by nodes from nearby communities. Despite these minor flaws, it overall does a pretty good job of segregating nodes into communities. This is expected because Louvain's major flaw of creating poorly connected or disconnected communities usually only occurs in larger network data.
Theoretically speaking, the Leiden model is supposed to perform better than the Louvain model. However, our results show the exact opposite – all of the nodes that are categorized into a community seem to be far away from one another. There are probably three main reasons:

1. Incorrect implementation of the partitioning quality function: The integration of quality functions is a crucial step in the Leiden model. It aims to evaluate the goodness of a partition of a network into communities by dividing nodes with dense internal connections and sparse connections between different clusters. The quality function we chose is modularity. A higher modularity value indicates a better partitioning of the network into communities, with more intra-community edges and fewer inter-community edges. Our other Leiden model functions seem to follow the logic of the pseudo codes in the appendix of the paper, and we are not so certain about the quality function.
2. The definition of “well-connected communities”: We define “well-connected” communities as communities that have direct contact with 4 other nodes, given the small size of the network. There should be better evaluation metrics that we need to look into.
3. Leiden performs the best with large network data, and the data we tested with is too small.
4. The parameters we chose are not the best; we should experiment with more.
   Besides Leiden, our other concern is whether we can achieve our extension of the project, which is to compare the efficiency of the two models.

### Next Steps

Altogether, we will:

1. Experiment with different parameter values for the Leiden algorithm.
2. Test Leiden on larger data.
3. Fully implement the extension.
4. Write a complete report.

In terms of individual work, Muya's priority will be fixing the quality function and researching how we can showcase that Leiden is more efficient than Louvain. Miles's priority will be obtaining the data. We will split the report writing tasks once we finish our priority tasks.
