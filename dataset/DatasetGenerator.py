import numpy

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
                matrix = self.generateAdjacencyMatrix(votes)
                filename = "./%s/%s.npy" % (issue, cid)
                os.makedirs(os.path.dirname(filename))
                numpy.save(filename, matrix)

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

    def generateAdjacencyMatrix(self, votes):
        nodes = set()
        for pair in votes.keys(): nodes |= set(pair)
        dim = len(nodes)
        matrix = numpy.matrix.shape((dim, dim))
        for k, v in votes.items():
            matrix[k[0], k[1]] = v
            matrix[k[1], k[0]] = v

        return matrix


#
# dg = DatasetGenerator()
# dg.generate_datasets()
