from DatasetGenerator import *
import scipy.sparse
import numpy as np
import matplotlib.pyplot as plt
from networkx import *
from networkx.drawing.nx_agraph import graphviz_layout


CURRENT_TOPIC = "Abortion"
plt.style.use('ggplot')

class PageRankSim:
    def __init__(self, graph, teleport, dg):
        self.graph = graph
        self.dg = dg
        self.teleport = teleport
        self.teleportmatrix = self.generateTeleportMatrix(0.1, teleport)
        self.r = self.powerIteration(4, 100)

    def generateTeleportMatrix(self, beta, teleport):
        senators = self.getSenators()
        if len(senators) == 0: return None
        if teleport is None: teleport = senators

        senators = sorted(list(senators))
        adj_matrix = np.zeros([len(senators), len(senators)])
        numsen = len(senators)

        _, graph = self.graph
        for i, si in enumerate(senators):
            deg = sum([graph[(si, sj)] + graph[(sj, si)] for sj in senators])
            for j, sj in enumerate(senators):
                if (si, sj) not in graph: continue
                prob = max(graph[(si, sj)], graph[(sj, si)]) / float(deg)
                adj_matrix[i, j] = (1 - beta) * prob + (beta if j == teleport else 0)

        ## Now we normalize the columns
        for i in range(numsen):
            colsum = sum([adj_matrix[i, j] for j in range(numsen)])

        return adj_matrix

    def powerIteration(self, senatorIdx, numIters):
        senators = sorted(list(self.getSenators()))
        if len(senators) == 0: return None
        r = np.matrix([1 if i == senatorIdx else 0 for i in range(len(senators))])
        for i in range(numIters):
            r = np.matmul(r, self.teleportmatrix)
        return r

    def getSenators(self):
        newsen = set()
        _, gp = self.graph
        for k in gp: newsen |= set(k)
        return newsen

    ## Percent of PPR mass that is same party
    def findSameParty(self):
        senators = sorted(self.getSenators())
        if len(senators) == 0: return None
        congress, _ = self.graph

        if self.teleport > len(senators): return None
        # print("FOO", self.teleport, len(senators))

        if (congress, senators[self.teleport]) not in self.dg.member_party_map: return None
        teleportParty = self.dg.member_party_map[(congress, senators[self.teleport])]
        congress, _ = self.graph
        same = 0
        for idx, prob in enumerate(self.r.T):
            party = self.dg.member_party_map[(congress, senators[idx])]
            if party == teleportParty:
                same += prob

        return same


    def visualize(self):
        # nx.draw(self.teleportmatrix)
        senators = sorted(self.getSenators())
        lensen = len(senators)
        congress, _ = self.graph

        A=numpy.matrix(numpy.zeros((lensen, lensen)))
        color_map = []
        for idx, node in enumerate(self.r.T):
            val = .2 + 190 * node
            val = val if val < 1 else 1
            val = val if val > .2 else .2
            party = self.dg.member_party_map[(congress, senators[idx])]
            color = 'red' if party == 'Republican' else 'blue'
            color_map.append(lighten_color(color, float(val)))

        G=nx.from_numpy_matrix(A)
        nx.draw(G, pos=graphviz_layout(G), node_size=30, node_color = color_map, prog='dot')
        plt.show()


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
for graph in graphs[CURRENT_TOPIC]:
    strs = set()
    cong, g = graph
    for k in g: strs |= set(k)
    for s in strs:
        party = dg.member_party_map[(cong, s)]
        if party == "Republican":
            repsen[s] += 1
        else:
            demsen[s] += 1


most_dem = max([(v, k) for k, v in demsen.items()])[1]
most_rep = max([(v, k) for k, v in repsen.items()])[1]


dem_polarization = []

x1, x2 = [], []
for graph in graphs[CURRENT_TOPIC]:
    #
    congress, g = graph
    for k in g: strs |= set(k)
    dem_idx = sorted(list(strs)).index(most_dem)
    print(most_dem)
    rep_idx = sorted(list(strs)).index(most_rep)

    # print("ROO", rep_idx, most_rep, strs)
    dpr = PageRankSim(graph, dem_idx, dg)
    dsim = dpr.findSameParty()

    rpr = PageRankSim(graph, rep_idx, dg)
    rsim = rpr.findSameParty()

    if rsim is not None:
        rsim = float(rsim)
        x1.append((congress * 2 + 1788, rsim))
    if dsim is not None:
        dsim = float(dsim)
        x2.append((congress * 2 + 1788, dsim))

axes = plt.gca()
fig, ax = plt.subplots()
ax.axhline(y=0.5, xmin=0.0, xmax=1.0, color='r')
axes.set_ylim([.15,.85])

plt.title("Personalized Pagerank Polarization for Charles B. Rangel (D. NY) [Abortion]")
plt.plot([x for (x, _) in x1], [y for (_, y) in x1])
# plt.plot([x for (x, _) in x2], [y for (_, y) in x2])

plt.show()
