import snap

class DatasetGenerator:

    def __init__(self, issues, issueMap, congresses, partyMapping):
        self.issues = issues
        self.issueMap = issueMap
        self.congresses = congresses
        self.partyMapping = partyMapping

    def generate_datasets(self):
        for issue in self.issues:
            for cid in self.congresses:
                votes = self.generate_dataset(issue, cid)

                filename = "./%s/%s.pickle" % (issue, cid)
                os.makedirs(os.path.dirname(filename))
                with open(filename, 'wb') as handle:
                    pickle.dump(votes, handle, protocol=pickle.HIGHEST_PROTOCOL)


    def generate_dataset(self, issue, cid):
        rollcalls = [rc for rc in self.issueMap[issue] if rc.identifier[0] == cid]
        congressPeople = set()

        # Map from tuple of conggresspeople to number of times they have agreed.
        votes = collections.defaultdict(int)

        # Count all of the votes in the rollcall object.
        for rc in rollcalls:
            for key in [rc.votes.keys()]:
                self.countVotes(rc, key, votes)

        return votes

    def countVotes(self, rc, key, votes):
        for i in range(len(rc.votes[key])):
            for j in range(i+1, len(rc.votes[key])):
                votepair = (rc.votes[i], rc.votes[j]) # Note that i < j.
                votes[votepair]+= 1

    # def generateProjection(self, votes):
    #     graph = snap.TUNGraph.New()
    #     nodes = set()
    #
    #     for pair in votes.keys(): nodes |= set(pair)
    #     for node in nodes: graph.AddNode(node)
    #     for pair in votes.keys(): graph.AddEdge2()
    #     return (votes, graph)

#
# dg = DatasetGenerator()
# dg.generate_datasets()
