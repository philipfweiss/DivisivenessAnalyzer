"""
Algorithm that spectrally parititons a projection of
the congressional voting graph.
"""

from DatasetGenerator import *
import scipy.sparse
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')

np.set_printoptions(suppress=True)
class SpectralPartition:
    def __init__(self, projection):
        print("hello")
        dg = DatasetGenerator(["Israel"], range(96, 114))
        graphs = dg.generate_datasets()
        ctr = 0
        eigen = []
        ys = []
        print('loo')
        for graph in graphs["Israel"]:
            if sum(graph[1].values()) == 0: continue
            vals, _  = self.plot_graph(graph, dg, False, ctr, False)
            eigen.append(vals[1])
            ys.append(96 + ctr)
            ctr+=1
        plt.xlabel('Congress')
        plt.title('Connectivity of Congressional Voting Graph (Israel)')
        plt.ylabel('Divisiveness Coefficient (Fiedler Eigenvalue)')
        plt.plot(ys, eigen)
        plt.show()


    def plot_graph(self, graph, dg, show, ctr, should_plot):
        congress, graph = graph
        adj_matrix, senators = self.get_adjacency_matrix(graph)            # adj_matrix = self.clean_adjacency_matrix(adj_matrix)
        laplacian = scipy.sparse.csgraph.laplacian(adj_matrix, normed=True)
        vals, vecs = np.linalg.eigh(laplacian)
        colors = []
        for i, senator in enumerate(senators):
            # print(senator)
            colors.append('dodgerblue' if dg.member_party_map[(congress, senator)] == "Republican" else 'r')
        x, y = vecs[:, 1:3].T

        if should_plot:
            ax = plt.subplot(4, 4, 1 + ctr)
            ctr+=1
            ax.set_title("Congress %s" % str(96 + ctr) )
            ax.scatter(x, y, c=colors)
        else:
            return (vals, vecs)

        if show:
            plt.show()

    def clean_adjacency_matrix(self, adj_matrix):
        adj_matrix = (adj_matrix > np.min(np.max(adj_matrix, axis=0), axis=0)/4).astype(float)
        return adj_matrix

    def get_adjacency_matrix(self, graph):
        senators = set()
        for k in graph: senators |= set(k)
        senators = list(sorted(senators))
        senator_to_index = {k:i for (i, k) in enumerate(senators)}

        adj_matrix = np.zeros([len(senators), len(senators)])
        for i, si in enumerate(senators):
            for j, sj in enumerate(senators[i+1:]):
                item = graph[(si, sj)]
                # print(item)
                adj_matrix[i, i+j+1] = item
                adj_matrix[i+j+1, i] = item
        degrees = np.sum(adj_matrix, axis=0)
        # adj_matrix = adj_matrix[degrees > 5000,:]
        # adj_matrix = adj_matrix[:, degrees > 5000]
        return adj_matrix, senators

SpectralPartition(None)
