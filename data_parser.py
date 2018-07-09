import json
import re
import utils

cset = set()
cdict = utils.myDict()

def parseCountryList(line):
    countries = line.split("-")[1]
    clist = re.split("[,&]", countries)
    for i in range(len(clist)):
        clist[i] = clist[i].strip()

        cdict[clist[i]] += 1
        cset.add(clist[i])

    return clist

data = []

with open("data_sources/data.txt") as f:
    for line in f.readlines():
        if not line.startswith("http://i.imgur.com"):
            continue

        entry = {}

        entry["url"] = line.split(" ")[0]
        entry["id"] = line.split("/")[3].split(".")[0].strip()
        entry["countries"] = parseCountryList(line)

        if "(" in line and ")" in line:
            entry["size"] = line.split("(")[1].split(")")[0].strip().decode("utf-8").replace(u'\u00d7', "x")

        if len(line.split("-")) > 2:
            entry["details"] = line.split("-", 2)[2].strip()

        data += [entry]

with open("data_normalization/output.json", "w") as f:
    json.dump(data, f, indent=2)

with open("data_normalization/country_list.json", "w") as f:
    json.dump(sorted(list(cset)), f, indent=2)

with open("data_normalization/country_freq.json", "w") as f:
    json.dump([{"count": x[0], "name": x[1]} for x in cdict.getSortedPairs()], f, indent=2)
