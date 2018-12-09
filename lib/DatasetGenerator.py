import numpy
import pickle
import collections
np = numpy


class DatasetGenerator:

    def __init__(self, issues, congresses):
        self.issues = issues
        self.issue_call_map = self.load_pickle('./pickle/issue_call_map.pkl')
        #print(self.issue_call_map.keys())
        # for k in sorted((len(self.issue_call_map[k]), k) for k in self.issue_call_map):
        #     print(k)

        ## issueMap[issue][congress] => rollcalls.
        ## call_uid_map[congressId][(id, rollcall#)] => rollcall
        self.issue_map, self.call_uid_map = {}, {}

        

        # print(len(self.issue_map["Abortion"][112]))
        self.congresses = congresses
        self.load_congress_to_call_uid_map()
        self.load_issue_map()
        self.member_party_map = self.load_pickle('./pickle/member_party_map.pkl')

    def generate_datasets(self):
        graphs = collections.defaultdict(list)
        for issue in self.issues:
            if issue:
                for cid in self.congresses:
                    print("loading", issue, cid, len(self.issue_map[issue][cid]))
                    votes = self.generate_dataset(self.issue_map[issue][cid])
                    graphs[issue].append((cid, votes))
            else:
                for cid in self.congresses: 
                    print("loading", cid, len(self.call_uid_map[cid].values()))
                    votes = self.generate_dataset(self.call_uid_map[cid].values())
                    graphs[issue].append((cid, votes))


        return graphs

                # print(sum([v for v in votes.values()]))
                # matrix = self.generateAdjacencyMatrix(votes)
                # continue
                # filename = "./pickle/graphs/%s/%s.npy" % (issue, cid)
                # os.makedirs(os.path.dirname(filename))
                # numpy.save(filename, matrix)

    def generate_dataset(self, rollcalls):
        congressPeople = set()

        # Map from tuple of conggresspeople to number of times they have agreed.
        votes = collections.defaultdict(int)

        # Count all of the votes in the rollcall object.
        all_senators = set()
        for rc in rollcalls:
            for key in rc.votes.keys():
                for senator in rc.votes[key]: 
                    all_senators.add(senator)
                # self.countVotes(rc, key, votes)
        sen_list = list(all_senators)
        all_senators = {v:k for k, v in enumerate(sen_list)}
        # print(all_senators)
        # print(len(all_senators))
        dim = len(all_senators)
        matrix = np.zeros((dim, dim))
        
        for rc in rollcalls:
            for key in rc.votes.keys():
                vec = np.zeros(dim)
                for senator in rc.votes[key]: 
                    vec[all_senators[senator]] = 1
                matrix += np.outer(vec, vec)
        # print("mat", matrix)
        return matrix, sen_list

    # def countVotes(self, rc, key, votes):
    #     for i in range(len(rc.votes[key])):
    #         for j in range(i+1, len(rc.votes[key])):
    #             votepair = (rc.votes[key][i], rc.votes[key][j]) # Note that i < j.
    #             print(votepair)
    #             votes[votepair]+= 1

    def generateAdjacencyMatrix(self, votes):
        nodes = set()
        for pair in votes.keys(): nodes |= set(pair)
        dim = len(nodes)
        matrix = numpy.matrix.shape((dim, dim))
        for k, v in votes.items():
            matrix[k[0], k[1]] = v
            matrix[k[1], k[0]] = v

        return matrix

    def load_pickle(self, file):
        with open(file, "rb") as input_file: return pickle.load(input_file)

    def load_issue_map(self):
        for issue in self.issues:
            roll_call_uids = self.issue_call_map[issue]
            self.issue_map[issue] = collections.defaultdict(list)
            for uid in roll_call_uids: ## (congress#,rollcall#)
                congressID = uid[0]
                if congressID not in self.call_uid_map: continue
                self.issue_map[issue][congressID].append(self.call_uid_map[congressID][uid])

    def load_congress_to_call_uid_map(self):
        for i in self.congresses:
            print(i)
            self.call_uid_map[i] = self.load_pickle("./pickle/call_uid_map/congress_%d.pkl" % i)




# dg = DatasetGenerator(['Abortion'], range(88, 110))
# graphs = dg.generate_datasets()
# print([len(grap for x in graphs])
# print(graphs[0])
