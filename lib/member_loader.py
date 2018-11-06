import json
import collections
from Models import *
import pickle

party_codes = {}
with open("HSall_parties.csv") as f:
	for line in f:
		line = line.split(",")
		if line[0] == "congress": continue # first line
		party_codes[int(line[2])] = line[3]
print(party_codes)

person_to_party_map = {}
with open("HSall_members.csv") as f:
	for line in f:
		line = line.split(",")
		if line[0] == "congress": continue # first line
		congress, uid, party = int(line[0]), int(line[2]), int(line[6])
		person_to_party_map[(congress, uid)] = party_codes[party]
print(person_to_party_map)

with open("pickle/member_party_map.pkl", "wb") as f:
	f.write(pickle.dumps(person_to_party_map))