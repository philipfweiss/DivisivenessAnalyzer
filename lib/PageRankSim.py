from DatasetGenerator import *
import scipy.sparse
import numpy as np
import matplotlib.pyplot as plt


class PageRankSim:
    def __init__(self, graph):
        self.graph = graph
        self.teleportmatrix = self.generateTeleportMatrix(beta=0.001)

    def generateTeleportMatrix(self, beta):
        senators = self.getSenators()
        if len(senators) == 0: return None
        senators = list(sorted(senators))
        adj_matrix = np.zeros([len(senators), len(senators)])
        numsen = len(senators)

        beta_term =  (1 - beta) / float(len(senators))
        _, graph = self.graph
        for i, si in enumerate(senators):
            deg = sum([graph[(si, sj)] + graph[(sj, si)] for sj in senators])
            for j, sj in enumerate(senators):
                if (si, sj) not in graph: continue
                item = max(graph[(si, sj)], graph[(sj, si)]) / float(deg)
                adj_matrix[i, j] = beta * item + beta_term
        return adj_matrix

    def powerIteration(self, senatorIdx, numIters):
        senators = self.getSenators()
        if len(senators) == 0: return None
        r = np.matrix([1 if i == senatorIdx else 0 for i in range(len(senators))]).T
        for i in range(numIters):
            r = np.matmul(self.teleportmatrix, r)

    def getSenators(self):
        senators = set()
        _, graph = self.graph
        for k in graph: senators |= set(k)
        return senators


dg = DatasetGenerator(["Israel"], range(96, 114))
graphs = dg.generate_datasets()
for graph in graphs["Israel"]:
    pr = PageRankSim(graph)
    pr.powerIteration(4, 5)
