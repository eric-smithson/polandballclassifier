import json
import re
import utils


class DataParser:
    def __init__(self):
        self.allcomics = {}
        self.countryset = set()
        self.countryhist = utils.myDict()

    def run(self):
        self.parseTxtData()
        self.parsePolandballArchive()
        self.buildCountrySet()
        self.output()

    def parseTxtData(self):
        def parseCountries(line):
            countries = line.split("-")[1]
            clist = re.split("[,&]", countries)
            for i in range(len(clist)):
                country = clist[i].strip().lower()
                if country in utils.normalization_map:
                    country = utils.normalization_map[country]
                clist[i] = country

            return clist

        with open("data_sources/data.txt") as f:
            for line in f.readlines():
                if not line.startswith("http://i.imgur.com"):
                    continue

                id = line.split("/")[3].split(".")[0].strip()
                if id in self.allcomics:
                    continue

                entry = {}

                entry["url"] = line.split(" ")[0]

                entry["countries"] = parseCountries(line)

                if "(" in line and ")" in line:
                    entry["size"] = line.split("(")[1].split(")")[0].strip().decode("utf-8").replace(u'\u00d7', "x")

                if len(line.split("-")) > 2:
                    entry["details"] = line.split("-", 2)[2].strip()

                self.allcomics[id] = entry

    def parsePolandballArchive(self):
        def parseCountries(line):
            countries = line.split(",")
            for i in range(0, len(countries)):
                country = countries[i].strip().lower()
                if country in utils.normalization_map:
                    country = utils.normalization_map[country]

                countries[i] = country

            return countries

        parser = utils.CSVParser("data_sources/r_polandball_archive.csv")
        csv = parser.data

        for row in csv:
            entry = {}

            if not row["Submission url"].startswith("http://i.imgur.com") or len(row["Countries/-balls featured"]) == 0:
                continue

            id = row["Submission url"].split("/")[3].split(".")[0].strip()
            if id in self.allcomics:
                continue

            entry["url"] = row["Submission url"]
            entry["countries"] = parseCountries(row["Countries/-balls featured"])
            entry["details"] = row["Title"]

            self.allcomics[id] = entry

    def buildCountrySet(self):
        if len(self.allcomics) == 0:
            raise ValueError

        for id, comic in self.allcomics.iteritems():
            if "various" in comic["countries"]:
                continue
            for country in comic["countries"]:
                # TODO: Find a way to normalize country names
                self.countryset.add(country)
                self.countryhist[country] += 1


    def output(self):
        with open("data_normalization/output.json", "w") as f:
            json.dump(self.allcomics, f, indent=2)

        with open("data_normalization/country_list.json", "w") as f:
            json.dump(sorted(list(self.countryset)), f, indent=2)

        with open("data_normalization/country_freq.json", "w") as f:
            json.dump([{"count": x[0], "name": x[1]} for x in self.countryhist.getSortedPairs()], f, indent=2)

if __name__ == '__main__':
    parser = DataParser()
    parser.run()
