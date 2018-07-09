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

class NormalizationMap:
    def __init__(self):
        self.normalization_map = {
            "U.S.": "United States"
        }
