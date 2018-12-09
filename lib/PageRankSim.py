from DatasetGenerator import *
import scipy.sparse
import numpy as np
import matplotlib.pyplot as plt
from networkx import *
from networkx.drawing.nx_agraph import graphviz_layout


CURRENT_TOPIC = ""
plt.style.use('ggplot')

# class PageRankSim:
#     def __init__(self, graph, teleport, dg):
#         self.graph = graph
#         self.dg = dg
#         self.teleport = teleport
#         self.teleportmatrix = self.generateTeleportMatrix(0.1, teleport)
#         self.r = self.powerIteration(4, 100)

#     def generateTeleportMatrix(self, beta, teleport):
#         senators = self.getSenators()
#         if len(senators) == 0: return None
#         if teleport is None: teleport = senators

#         senators = sorted(list(senators))
#         adj_matrix = np.zeros([len(senators), len(senators)])
#         numsen = len(senators)

#         _, graph = self.graph
#         # for i, si in enumerate(senators):
#         #     deg = sum([graph[(si, sj)] + graph[(sj, si)] for sj in senators])
#         #     for j, sj in enumerate(senators):
#         #         if (si, sj) not in graph: continue
#         #         prob = max(graph[(si, sj)], graph[(sj, si)]) / float(deg)
#         #         adj_matrix[i, j] = (1 - beta) * prob + (beta if j == teleport else 0)

#         ## Now we normalize the columns
#         for i in range(numsen):
#             colsum = sum([adj_matrix[i, j] for j in range(numsen)])

#         return adj_matrix

#     def powerIteration(self, senatorIdx, numIters):
#         senators = sorted(list(self.getSenators()))
#         if len(senators) == 0: return None
#         r = np.matrix([1 if i == senatorIdx else 0 for i in range(len(senators))])
#         for i in range(numIters):
#             r = np.matmul(r, self.teleportmatrix)
#         return r

#     def getSenators(self):
#         newsen = set()
#         _, gp = self.graph
#         for k in gp: newsen |= set(k)
#         return newsen

#     ## Percent of PPR mass that is same party
#     def findSameParty(self):
#         senators = sorted(self.getSenators())
#         if len(senators) == 0: return None
#         congress, _ = self.graph

#         if self.teleport > len(senators): return None
#         # print("FOO", self.teleport, len(senators))

#         if (congress, senators[self.teleport]) not in self.dg.member_party_map: return None
#         teleportParty = self.dg.member_party_map[(congress, senators[self.teleport])]
#         congress, _ = self.graph
#         same = 0
#         for idx, prob in enumerate(self.r.T):
#             party = self.dg.member_party_map[(congress, senators[idx])]
#             if party == teleportParty:
#                 same += prob

#         return same


#     def visualize(self):
#         # nx.draw(self.teleportmatrix)
#         senators = sorted(self.getSenators())
#         lensen = len(senators)
#         congress, _ = self.graph

#         A=numpy.matrix(numpy.zeros((lensen, lensen)))
#         color_map = []
#         for idx, node in enumerate(self.r.T):
#             val = .2 + 190 * node
#             val = val if val < 1 else 1
#             val = val if val > .2 else .2
#             party = self.dg.member_party_map[(congress, senators[idx])]
#             color = 'red' if party == 'Republican' else 'blue'
#             color_map.append(lighten_color(color, float(val)))

#         G=nx.from_numpy_matrix(A)
#         nx.draw(G, pos=graphviz_layout(G), node_size=30, node_color = color_map, prog='dot')
#         plt.show()


def lighten_color(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])



dg = DatasetGenerator([CURRENT_TOPIC], range(70, 115))
graphs = dg.generate_datasets()

demsen = collections.defaultdict(int)
repsen = collections.defaultdict(int)
dg_dems = {}
dg_reps = {}
for graph in graphs[CURRENT_TOPIC]:
    strs = set()
    cong, (g, strs) = graph
    dg_dems[cong] = np.zeros(len(strs))
    dg_reps[cong] = np.zeros(len(strs))
    for i, s in enumerate(strs):
        party = dg.member_party_map[(cong, s)]
        if party == "Republican":
            repsen[s] += 1
            dg_reps[cong][i] = 1
        elif party == "Democrat":
            demsen[s] += 1
            dg_dems[cong][i] = 1
    # print(dg_dems.shape)

# most_dem = max([(v, k) for k, v in demsen.items()])[1]
# most_rep = max([(v, k) for k, v in repsen.items()])[1]
# print(most_dem)
# print(most_rep)

dem_polarization = []

class PageRankSim(object):
    def __init__(self, graph, idx, dg):
        _, (self.graph, _) = graph
        # print(self.graph)
        self.idx = idx
        self.dg = dg
    def findSameParty(self):
        vv = self.dg / np.sum(self.dg) + (1 - self.dg) / np.sum(1 - self.dg)
        mat = self.graph * vv.reshape([-1, 1])
        mat = mat / np.sum(mat, axis=0, keepdims=True)
        beta = 0.8
        teleport = np.zeros([mat.shape[0], 1])
        teleport[self.idx] = 1
        mat = beta * mat + (1 - beta) * teleport
        r0 = np.random.randn(self.graph.shape[0], 1) ** 2
        r0 = r0 / np.sum(r0)
        niter = 0
        while True:
            rnew = np.matmul(mat, r0)
            if np.allclose(r0, rnew): break
            r0 = rnew
            niter += 1
        print(np.average(self.dg), np.dot(np.ravel(r0), self.dg), "iterations", niter)
        return np.dot(np.ravel(r0), self.dg)

x1, x2 = [], []

senator = [14828, 94828]
senator_name = "Ralph Hall"
senator_party = dg_dems

for graph in graphs[CURRENT_TOPIC]:
    #
    congress, (g, strs) = graph
    # if not strs: continue
    strs = {v:k for k, v in enumerate(strs)}

    # dem_idx = strs.index(most_dem)
    # print(g.shape, len(strs))
    # rep_idx = strs.index(most_rep)
    idx = None
    for s in senator:
        if s in strs: 
            idx = strs[s]
            break
    if idx is None: continue

    # print("ROO", rep_idx, most_rep, strs)
    dpr = PageRankSim(graph, idx, senator_party[congress])
    dsim = dpr.findSameParty()

    # rpr = PageRankSim(graph, rep_idx, dg_reps[congress])
    # rsim = rpr.findSameParty()

    # if rsim is not None:
    #     rsim = float(rsim)
    #     x1.append((congress * 2 + 1788, rsim))
    if dsim is not None:
        dsim = float(dsim)
        x2.append((congress * 2 + 1788, dsim))

# axes = plt.gca()
_, ax = plt.subplots()
ax.axhline(y=0.5, xmin=0.0, xmax=1.0, color='r')
plt.title("PPR Partisanship for " + senator_name)
plt.plot(*np.array(x2).T)
plt.show()
