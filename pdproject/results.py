"""
Class used to store and report results data on algorithms used for plagiarism detection.
"""


import numpy as np

import document


class Results:
    def __init__(self):
        self.highest_hit = float('inf')
        self.highest_doc = None
        self.lowest_hit = float('-inf')
        self.lowest_doc = None
        self.scores = []
        self.documents = []
        self.num_results = 0

    def add(self, doc: document.Document, hit_rate: float):
        if self.highest_hit == float('inf'):
            self.highest_hit = hit_rate
            self.highest_doc = doc
        elif hit_rate > self.highest_hit:
            self.highest_hit = hit_rate
            self.highest_doc = doc
        elif hit_rate != 0 and self.lowest_hit == float('-inf'):
            self.lowest_hit = hit_rate
            self.lowest_doc = doc
        elif hit_rate != 0 and hit_rate < self.lowest_hit:
            self.lowest_hit = hit_rate
            self.lowest_doc = doc
        self.scores.append(hit_rate)
        self.documents.append(doc.filename)
        self.num_results += 1

    def display(self, show_quartiles = False):
        if self.highest_hit == float('inf'):
            highest_hit = 0
            highest_doc = 'N/A'
        else:
            highest_hit = self.highest_hit
            highest_doc = self.highest_doc.filename
        if self.lowest_hit == float('-inf'):
            lowest_hit = 0
            lowest_doc = "N/A"
        else:
            lowest_hit = self.lowest_hit
            lowest_doc = self.lowest_doc.filename
        print("\n---> Total documents checked: \t{num_results}".format(num_results=self.num_results))
        print("\n---> Highest hit rate: \t\t\t{hit_h:.2f}%\n---> Associated document: \t\t{doc_h}".format(hit_h=highest_hit, doc_h=highest_doc))
        print("\n---> Lowest hit rate: \t\t\t{hit_l:.2f}%\n---> Associated document: \t\t{doc_l}".format(hit_l=lowest_hit, doc_l=lowest_doc))
        if len(self.scores) != 0: 
            print("\nAll results:")
        else:
            print("\nNo results to display.")
        for i in range(len(self.scores)):
            if self.scores[i] != 0:
                print("\t{filename}: {hits:.2f}%".format(filename=self.documents[i], hits=self.scores[i]))
        if len(self.scores) != 0: 
            print("\nFiles without hits have been excluded in the results above.")
        if show_quartiles:
            np_quartiles = np.quantile(self.scores, [0.25,0.5,0.75])
            quartiles = np_quartiles.tolist()
            print("\nHit rate statistics:")
            print("---> 1st-Quartile: \t\t\t\t{median:.2f}%".format(median=quartiles[0]))
            print("---> Median: \t\t\t\t\t{median:.2f}%".format(median=quartiles[1]))
            print("---> 3rd-Quartile: \t\t\t\t{median:.2f}%".format(median=quartiles[2]))
            print("---> Mean: \t\t\t\t\t\t{median:.2f}%".format(median=np.mean(self.scores)))