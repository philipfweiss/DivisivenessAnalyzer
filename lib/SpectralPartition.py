"""
Algorithm that spectrally parititons a projection of
the congressional voting graph.
"""

from DatasetGenerator import *
import scipy.sparse
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True)
class SpectralPartition:
    def __init__(self, projection):
        print("hello")
        dg = DatasetGenerator(["Abortion"], range(90, 114))
        graphs = dg.generate_datasets()
        # print(graphs)
        # graphs: map<str issue, list<(congress, map<pair<senator>, int>)>>
        for graph in graphs["Abortion"]:
            congress, graph = graph
            if sum(graph.values()) == 0: continue
            adj_matrix, senators = self.get_adjacency_matrix(graph)
            # adj_matrix = self.clean_adjacency_matrix(adj_matrix)
            laplacian = scipy.sparse.csgraph.laplacian(adj_matrix, normed=True)
            vals, vecs = np.linalg.eigh(laplacian)
            colors = []
            for i, senator in enumerate(senators):
                # print(senator)
                colors.append("br"[dg.member_party_map[(congress, senator)] == "Republican"])
            x, y = vecs[:, 1:3].T
            plt.scatter(x, y, c=colors)
            plt.show()
            
    def clean_adjacency_matrix(self, adj_matrix):
        adj_matrix = (adj_matrix > np.min(np.max(adj_matrix, axis=0), axis=0)/4).astype(float)
        return adj_matrix

    def get_adjacency_matrix(self, graph):
        senators = set()
        for k in graph: senators |= set(k)
        print(len(senators))
        senators = list(sorted(senators))
        senator_to_index = {k:i for (i, k) in enumerate(senators)}

        print(senators, senator_to_index)
        adj_matrix = np.zeros([len(senators), len(senators)])
        print(adj_matrix)
        for i, si in enumerate(senators):
            for j, sj in enumerate(senators[i+1:]):
                item = graph[(si, sj)]
                # print(item)
                adj_matrix[i, i+j+1] = item
                adj_matrix[i+j+1, i] = item 
        print(adj_matrix)
        degrees = np.sum(adj_matrix, axis=0)
        print(list(sorted(degrees)))
        adj_matrix = adj_matrix[degrees > 5000,:]
        adj_matrix = adj_matrix[:, degrees > 5000]
        print(adj_matrix)
        return adj_matrix, senators

SpectralPartition(None)