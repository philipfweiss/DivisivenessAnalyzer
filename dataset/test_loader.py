import json
with open("HSall_rollcalls.json") as f: 
	f = f.read()
pos = 0
decoder = json.JSONDecoder()
bills = []
issue_codes = set()
while True:
	try: 
		obj, pos = decoder.raw_decode(f, pos)
		bills.append(obj)
		if obj["bill_number"] is not None and obj["issue_codes"] is not None:
			for item in obj["issue_codes"]:
				if not item in issue_codes: 
					print(item)
					issue_codes.add(item)
	except json.JSONDecodeError as e:
		#print(e)
		pos += 1
