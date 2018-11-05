import json
import collections
from Models import *
import pickle

call_uid_map = {}
issue_call_map = collections.defaultdict(list)

with open("HSall_rollcalls.json") as f: calls_json = f.read()

class VoteFileReader(object):
	def __init__(self):
		self.it = iter(open("HSall_votes.csv"))
		self.next() # skip header line
		self.next() 
	def next(self): 
		try: self.current_line = next(self.it)
		except StopIteration: self.current_line = None
	def get_votes(self, call):
		while True:
			line = self.current_line
			if line is None: return
			line = line.split(",")
			if line[1] == "House":
				line = list(map(int, line[0:1] + line[2:]))
				uid = (line[0], line[1]) 
				voter = line[2]
				cast_code = line[3]
				if uid > call.identifier: return # next call!
				if uid == call.identifier:
					if cast_code in [1, 2, 3]: call.votes["yes"].append(voter)
					if cast_code in [4, 5, 6]: call.votes["no"].append(voter)
					if cast_code in [7, 8, 9]: call.votes["abstain"].append(voter)
			self.next()

def dump_pickle():
	with open("pickle/call_uid_map/congress_%d.pkl" % congress_number, "wb") as f:
		f.write(pickle.dumps(call_uid_map))
		call_uid_map.clear()
	with open("pickle/issue_call_map.pkl", "wb") as f:
		f.write(pickle.dumps(issue_call_map))


vote_file_reader = VoteFileReader()
pos = 0
decoder = json.JSONDecoder()
congress_number = 0
while True:
	try:
		if pos > len(calls_json): break
		obj, pos = decoder.raw_decode(calls_json, pos)
		if obj["chamber"] != "House": continue # restrict to house
		topics = []
		for field in ["issue_codes", "peltzman_codes", "clausen_codes", "crs_subjects"]:
			if obj[field]: topics.extend(obj[field])
		if obj["crs_policy_area"]: topics.append(obj["crs_policy_area"])
		if not topics: continue
		topics = list(sorted(set(topics)))
		uid = (obj["congress"], obj["rollnumber"])
		if uid[0] > congress_number:
			print("\rcongress number: %d" % uid[0], end="")
			dump_pickle()
			congress_number = uid[0]
		call = RollCall(uid, topics)
		vote_file_reader.get_votes(call)
		if len(call.votes["yes"]) != obj["yea_count"]:
			print()
			print("WARNING: mismatched YEA count:", end=" ")
			print(call.identifier, len(call.votes["yes"]), obj["yea_count"])
		elif len(call.votes["no"]) != obj["nay_count"]:
			print()
			print("WARNING: mismatched NAY count:", end=" ")
			print(call.identifier, len(call.votes["no"]), obj["nay_count"])
		else:
			call_uid_map[uid] = call
			for topic in topics: issue_call_map[topic].append(uid)
	except json.JSONDecodeError as e:
		pos += 1

dump_pickle()
print()
print("done!")