import csv

class myDict(dict):
    def __getitem__(self, item):
        self.setdefault(item, 0)
        return dict.__getitem__(self, item)

    def getSortedPairs(self):
        keys = self.keys()

        freq_pair = []

        for k in keys:
            freq_pair += [(self.get(k), k)]

        freq_pair = sorted(freq_pair, reverse=True)

        return freq_pair




class CSVParser:
    def __init__(self, csv_name):
        self.data = []
        with open(csv_name, "r") as f:
            self.reader = csv.DictReader(f)
            for row in self.reader:
                self.data += [row]

normalization_map = {
    "us": "united states",
    "u.s.": "united states",
    "usa": "united states",
    "u.s.a.": "united states",
    "america": "united states",
    "uk" : "united kingdom",
    "u.k.": "united kingdom",
    "ussr" : "soviet union",
    "u.s.s.r." : "soviet union",
    "ussr / soviet union" : "soviet union",
    "e.u." : "european union",
    "eu" : "european union",
    "un" : "united nations",
    "u.n." : "united nations",
    "u.a.e" : "united arab emirates",
    "uae": "united arab emirates",
}

if __name__ == '__main__':
    csv = CSVParser("data_sources/r_polandball_archive.csv")
