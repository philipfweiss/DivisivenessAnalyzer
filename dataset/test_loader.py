import csv
import re
from urllib.request import urlopen


def title_contains_keywords(title, keywords):
    return any([keyword in title.lower().split() for keyword in keywords])

def load_bill_data(file):
    file = urlopen("https://voteview.com/static/data/out/rollcalls/HSall_rollcalls.json")
    content = file.read()
    c = re.findall("issue_codes\":\[[^\]]*\]", content)
    print()

        # csv_reader = csv.reader(f, delimiter='\t')
        # for line in csv_reader:
        #     if title_contains_keywords(line[26], ['abortion', 'child']):#['gun', 'assault', 'firearm', 'weapon']):
        #         print(line[1], line[26])



load_bill_data("bills80-92.txt")
