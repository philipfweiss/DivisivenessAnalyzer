"""
Algorithm that spectrally parititons a projection of
the congressional voting graph.
"""

from DatasetGenerator import *
import scipy.sparse
import numpy as np
import matplotlib.pyplot as plt
import os


plt.style.use("ggplot")

plt.style.use('ggplot')

np.set_printoptions(suppress=True)
class SpectralPartition:
    def __init__(self, projection):
        print("hello")
<<<<<<< HEAD
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

=======
        issues = [
            'Foreign and Defense Policy',
            'Abortion',
            'Pollution and Environmental Protection',
            'Social Welfare',
            'Medicaid',
            'Civil Liberties',
            'Israel',
            'Firearms',
            # 'Border security and unlawful immigration',
            '',
        ]
        dg = DatasetGenerator(issues, range(65, 115))
        graphs = dg.generate_datasets()
        # print(graphs)
        # graphs: map<str issue, list<(congress, map<pair<senator>, int>)>>
        congress_graphs = []
        output_dir = "output_100y_test"
        for issue in issues:
            print(issue)

            dirname = output_dir + "/vecs_%s" % issue.replace(" ", "_").lower()
            if not os.path.isdir(dirname): os.makedirs(dirname)
            congress_graph = []
            for graph in graphs[issue]:
                # print(graph)
                congress, graph = graph
                year = congress * 2 + 1788
                if np.sum(graph[0]) == 0: continue
                adj_matrix, senators = graph
                if np.max(adj_matrix) < 10: continue
                # adj_matrix = self.clean_adjacency_matrix(adj_matrix)
                laplacian = scipy.sparse.csgraph.laplacian(adj_matrix, normed=True)
                vals, vecs = np.linalg.eigh(laplacian)
                colors = []
                x, y = vecs[:, 1:3].T
                dem_xs = []
                for i, senator in enumerate(senators):
                    # print(senator)
                    party = dg.member_party_map[(congress, senator)]
                    if party == "Democrat": 
                        colors.append("b")
                        dem_xs.append(x[i])
                    elif party == "Republican": colors.append("r")
                    else: colors.append("k")
                if np.average(dem_xs) > 0: x = -x
                if np.median(y) > 0: y = -y
                plt.scatter(x, y, c=colors)
                plt.savefig("%s/%d.png" % (dirname, year))
                plt.cla(); plt.close()
                congress_graph.append([year, vals[1]])
            plt.plot(*np.array(congress_graph).T)
            plt.ylim(0,1)
            plt.savefig(output_dir + "/vals_%s.png" % issue.replace(" ", "_").lower())
            plt.cla(); plt.close();
            congress_graphs.append((issue, congress_graph))
        colors = list(plt.cm.rainbow(np.linspace(0,1,len(issues)-1))) + ['k']
        print(colors)
        linewidth = 1
        for i, ((issue, congress_graph), c) in enumerate(zip(congress_graphs, colors)):
            if issue == '':
                issue = 'ALL'
                linewidth = 2
            plt.plot(*np.array(congress_graph).T, label=issue, color=c,
                        linewidth=linewidth)
        plt.legend(fontsize="xx-small")
        plt.ylim(0,1)
        plt.savefig(output_dir + "/all_vals.png")
            
>>>>>>> a6321b1736814fc354b9cd4d67bbb42f51f1ef0c
    def clean_adjacency_matrix(self, adj_matrix):
        adj_matrix = (adj_matrix > np.min(np.max(adj_matrix, axis=0), axis=0)/4).astype(float)
        return adj_matrix

    def get_adjacency_matrix(self, graph):
        senators = set()
        for k in graph: senators |= set(k)
<<<<<<< HEAD
        senators = list(sorted(senators))
        senator_to_index = {k:i for (i, k) in enumerate(senators)}

        adj_matrix = np.zeros([len(senators), len(senators)])
=======
        # print(len(senators))
        senators = list(sorted(senators))
        senator_to_index = {k:i for (i, k) in enumerate(senators)}

        # print(senators, senator_to_index)
        adj_matrix = np.zeros([len(senators), len(senators)])
        # print(adj_matrix)
>>>>>>> a6321b1736814fc354b9cd4d67bbb42f51f1ef0c
        for i, si in enumerate(senators):
            for j, sj in enumerate(senators[i+1:]):
                item = graph[(si, sj)]
                # print(item)
                adj_matrix[i, i+j+1] = item
<<<<<<< HEAD
                adj_matrix[i+j+1, i] = item
        degrees = np.sum(adj_matrix, axis=0)
        # adj_matrix = adj_matrix[degrees > 5000,:]
        # adj_matrix = adj_matrix[:, degrees > 5000]
=======
                adj_matrix[i+j+1, i] = item 
        print(adj_matrix)
        # degrees = np.sum(adj_matrix, axis=0)
        # print(list(sorted(degrees)))
        # adj_matrix = adj_matrix[degrees > 5000,:]
        # adj_matrix = adj_matrix[:, degrees > 5000]
        # print(adj_matrix)
>>>>>>> a6321b1736814fc354b9cd4d67bbb42f51f1ef0c
        return adj_matrix, senators

SpectralPartition(None)
