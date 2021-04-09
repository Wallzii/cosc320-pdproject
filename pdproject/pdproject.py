# import nltk
import re
import os
import sys
import configparser

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from kmp import KMPSearch
from lcss import LCSS
from rabinkarp import RabinKarp
from tryItABunch import tryItABunch, tryItABunchKMP, tryItABunchKMPEqual, tryItABunchKMPLargePat, tryItABunchKMPWrapper, \
                        tryItABunchLCSS, tryItABunchLCSSEqual, tryItABunchLCSSLargePat, tryItABunchLCSSWrapper, tryItABunchRabinKarpEqual


config = configparser.ConfigParser()
config.read('config.ini')
CORPUS_DIR = config['DEFAULT']['CorpusDirectoryMultiple']
CORPUS_DIR_SINGULAR = config['DEFAULT']['CorpusDirectorySingular']
PLAG_DIR = config['DEFAULT']['PlagiarizedDirectory']
CORPUS_USE_SINGULAR = config.getboolean('DEFAULT', 'CorpusUseSingular')
VERBOSE = config.getboolean('DEFAULT', 'VerboseMode')
ENABLE_KMP = config.getboolean('ALGORITHMS', 'Enable_KMP')
ENABLE_LCSS = config.getboolean('ALGORITHMS', 'Enable_LCSS')
ENABLE_RabinKarp = config.getboolean('ALGORITHMS', 'Enable_RabinKarp')
ANALYSIS_KMP = config.getboolean('ANALYSIS', 'RuntimeAnalysis_KMP')
ANALYSIS_KMP_WRAPPER = config.getboolean('ANALYSIS', 'RuntimeAnalysis_KMP_Wrapper')
ANALYSIS_LCSS = config.getboolean('ANALYSIS', 'RuntimeAnalysis_LCSS')
ANALYSIS_LCSS_WRAPPER = config.getboolean('ANALYSIS', 'RuntimeAnalysis_LCSS_Wrapper')
ANALYSIS_RabinKarp = config.getboolean('ANALYSIS', 'RuntimeAnalysis_RabinKarp')
ANALYSIS_RabinKarp_WRAPPER = config.getboolean('ANALYSIS', 'RuntimeAnalysis_RabinKarp_Wrapper')
ANALYSIS_ALL = config.getboolean('ANALYSIS', 'RuntimeAnalysis_All')
ANALYSIS_ALL_WRAPPER = config.getboolean('ANALYSIS', 'RuntimeAnalysis_All_Wrapper')


class Document:
    """
    Object used to store a parsed textfile. Document contains the filename, as well as a list 
    of paragraphs and sentences. Document objects are intended to be stored within the Corpus 
    object.

    __init__(filename: str)

    Methods:
    \tadd_paragraphs(), add_sentences(), info(), print_paragraphs(), print_sentences().
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.paragraphs = []
        self.sentences = []
        self.raw_text = ""

    def parse(self, raw_text: str):
        """
        Parses the input string into the Document attributes. Sentences and paragraphs are extracted 
        from the input string and appended to Document.sentences[] and Document.paragraphs[], respectively. 
        The input string becomes Document.raw_text.
        """
        if type(raw_text) is str:
            self.raw_text = raw_text
            paragraphs = raw_text.splitlines()
            paragraphs = list(filter(None, paragraphs))
            self.__add_paragraphs(paragraphs)
            sentences = split_sentences(raw_text)
            sentences = list(filter(None, sentences))
            self.__add_sentences(sentences)
        else:
            raise TypeError("Parameter of Document.parse() was {type} and must be of type 'str'.".format(type=type(raw_text)))

    def __add_paragraphs(self, paragraphs: list):
        if type(paragraphs) is list:
            self.paragraphs += paragraphs
        else:
            raise TypeError("Parameter of Document.add_paragraphs() was {type} and must be of type 'list'.".format(type=type(paragraphs)))


    def __add_sentences(self, sentences: list):
        if type(sentences) is list:
            self.sentences += sentences
        else:
            raise TypeError("Parameter of Document.add_sentences() was {type} and must be of type 'list'.".format(type=type(sentences)))

    def info(self):
        """Outputs the filename for a Document object, along with number of paragraphs and sentences."""
        print("Document '{file}' contains {num_par} paragraph(s) and {num_sen} sentence(s), and has an overall length of {len} characters.".format(file=self.filename, num_par=len(self.paragraphs), num_sen=len(self.sentences), len=len(self.raw_text)))

    
    def number_paragraphs(self) -> int:
        return len(self.paragraphs)

    
    def print_paragraphs(self):
        """Prints out all paragraphs contained with a Document object."""
        if len(self.paragraphs) > 0:
            if VERBOSE:
                print("Paragraphs in Document '{filename}':".format(filename=self.filename))
                for i, para in enumerate(self.paragraphs):
                    print("{file}->paragraphs[{i}]: {para}".format(file=self.filename, i=i, para=para))
            else:
                print("Paragraphs in '{filename}': {paragraphs}".format(filename=self.filename, paragraphs=self.paragraphs))
        else:
            print("No paragraphs in '{filename}' to display.".format(filename=self.filename))

    def print_sentences(self):
        """Prints out all sentences contained within a Document object."""
        if len(self.sentences) > 0:
            if VERBOSE:
                print("Sentences in Document '{filename}':".format(filename=self.filename))
                for i, sentence in enumerate(self.sentences):
                    print("{file}->sentence[{i}]: {sentence}".format(file=self.filename, i=i, sentence=sentence))
            else:
                print("Sentences in '{filename}': {sentences}".format(filename=self.filename, sentences=self.sentences))
        else:
            print("No sentences in '{filename}' to display.".format(filename=self.filename))


class Corpus:
    """
    Object used to store a collection of Document objects. Document objects are stored within a 
    dictionary, where the key is the filename of the given Document and the value is the 
    Document object itself.

    Methods:
    \tadd_document(), info().
    """
    def __init__(self):
        self.documents = {}
        self.keys = []

    def add_document(self, filename: str, document: Document):
        """Adds a Document object to the documents dictionary of the corpus."""
        if type(document) is Document:
            self.documents[filename] = document
            self.keys.append(filename)
        else:
            raise TypeError("Parameter of Corpus.add_document() was {type} and must be of type 'Document'.".format(type=type(document)))

    def info(self):
        """Outputs number of documents in the corpus along with their dictionary keys."""
        if len(self.documents) > 0:
            if VERBOSE:
                print("Corpus contains {documents} document(s): {keys}".format(documents=len(self.documents), keys=[*self.documents]))
            else:
                print("Corpus contains {documents} document(s).".format(documents=len(self.documents)))
        else:
            print("No Document keys in Corpus to display.")

    def get_keys(self) -> list:
        return self.keys


class Results:
    def __init__(self):
        self.highest_hit = float('inf')
        self.highest_doc = None
        self.lowest_hit = float('-inf')
        self.lowest_doc = None
        self.scores = []
        self.documents = []
        self.num_results = 0

    def add(self, document: Document, hit_rate: float):
        if self.highest_hit == float('inf'):
            self.highest_hit = hit_rate
            self.highest_doc = document
        elif hit_rate > self.highest_hit:
            self.highest_hit = hit_rate
            self.highest_doc = document
        elif hit_rate != 0 and self.lowest_hit == float('-inf'):
            self.lowest_hit = hit_rate
            self.lowest_doc = document
        elif hit_rate != 0 and hit_rate < self.lowest_hit:
            self.lowest_hit = hit_rate
            self.lowest_doc = document
        self.scores.append(hit_rate)
        self.documents.append(document.filename)
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


def split_sentences(string) -> list:
    """
    Separates a string into its component sentences and stores each individual sentence 
    into an output list. Any sentence-terminating punctuation is removed from the sentence 
    when stored into the output list.
    """
    sentences = re.split(r'[.?!]\s*', string)
    if sentences[-1]:
        return sentences
    else:
        return sentences[:-1]


def compile_corpus_documents() -> list:
    """
    Checks for the existence of .txt files stored within the defined corpus directory and 
    parses those files into Document objects. Each Document object is appended to a list 
    which is returned to the function caller. The returned list can then be used to create 
    a corpus of documents by calling compile_corpus() with the returned list as a parameter.
    
    The corpus directory to be searched is defined within 'config.ini' located at the root 
    of the project directory.

    Intended Usage:
    \tdocuments = compile_corpus_documents()

    \tcorpus = compile_corpus(documents)
    """
    documents = []
    print("\nScanning for documents to add to corpus...")
    for file in os.listdir(CORPUS_DIR):
        if file.lower().endswith(".txt"):
            with open(os.path.join(CORPUS_DIR, file), 'r') as f:
                doc = Document(file)
                raw_text = f.read()
                doc.parse(raw_text)
                documents.append(doc)
        else:
            print("An invalid file was found and will be ignored: '{file}'".format(file=file))
    if len(documents) == 0:
        print("No valid documents were found when scanning directory '{dir}'.".format(dir=os.path.join(CORPUS_DIR)))
        return False
    else:
        return documents


def compile_plag_document():
    print("Scanning for potentially plagiarized document...")
    file = os.listdir(PLAG_DIR)
    if file[0].lower().endswith(".txt"):
        with open(os.path.join(PLAG_DIR, file[0]), 'r') as f:
            doc = Document(file[0])
            raw_text = f.read()
            doc.parse(raw_text)
            return doc
    else:
        print("Invalid file type found: '{dir}'".format(dir=os.path.join(PLAG_DIR, file[0])))
        print("Directory '{dir}' must contain only one file of type '.txt' and no sub-directories.".format(dir=os.path.join(PLAG_DIR)))
        return False


def extract_corpus_files() -> list:
    documents = []
    file = os.listdir(CORPUS_DIR_SINGULAR)
    if file[0].lower().endswith(".txt"):
        with open(os.path.join(CORPUS_DIR_SINGULAR, file[0]), 'r') as f:
            doc = Document(file[0])
            raw_text = f.read()
            if type(raw_text) is str:
                doc.raw_text = raw_text
                essay = raw_text.splitlines()
                essay = list(filter(None, essay))
                doc._Document__add_paragraphs(essay)
            else:
                raise TypeError("Parameter of Document.parse() was {type} and must be of type 'str'.".format(type=type(raw_text)))
            for i in range(doc.number_paragraphs()):
                filename = "input{x}".format(x=i)
                filename += ".txt"
                temp_doc = Document(filename)
                raw_text = doc.paragraphs[i]
                temp_doc.parse(raw_text)
                documents.append(temp_doc)
        return documents
    else:
        print("Invalid file type found: '{dir}'".format(dir=os.path.join(PLAG_DIR, file[0])))
        print("Directory '{dir}' must contain only one file of type '.txt' and no sub-directories.".format(dir=os.path.join(PLAG_DIR)))
        return False


def compile_corpus(documents: list) -> Corpus:
    """
    Compiles a list of Document objects into a Corpus. When this function is called, 
    a new Corpus object is created, populated with Document objects, and then returned to 
    the function caller. The returned Corpus object can then use its methods to access its 
    held Document objects and their methods.

    Intended Usage:
    \tdocuments = compile_corpus_documents()

    \tcorpus = compile_corpus(documents)
    """
    print("\nCompiling corpus from set of documents...")
    corpus = Corpus()
    for document in documents:
        try:
            corpus.add_document(document.filename, document)
        except TypeError:
            print("Parameter of add_document() was {type} and must be of type 'Document'.".format(type=type(document)))
            return False
        except:
            return False
    return corpus


def KMP_wrapper(corpus: Corpus, plagiarized: Document, results: Results):
    for i, corp_doc in enumerate(corpus.documents):
        total_hit_rate = 0
        if VERBOSE: print()
        print("KMPSearch() starting...\n---> Potentially plagiarized input: '{plag}'\n---> Corpus document: '{corp}' (document {x} of {x_len})\n".format(plag=plagiarized.filename, corp=corp_doc, x=(i + 1), x_len=len(corpus.documents)))
        for pattern in plagiarized.sentences:
            total_hit_rate += KMPSearch(pattern, corpus.documents[corp_doc].raw_text)
            if pattern is plagiarized.sentences[len(plagiarized.sentences) - 1]:
                if VERBOSE:
                    if total_hit_rate == 0:
                        print("No pattern matches found.")
                    print("\n------------------------------------------------------------")
                    print("Total plagiarism hit rate of '{plag_doc}' in '{corp_doc}': {rate:.2f}%".format(plag_doc=plagiarized.filename, corp_doc=corp_doc, rate=total_hit_rate))
                    hit_rate_analysis(total_hit_rate)
                    print("------------------------------------------------------------")
                results.add(corpus.documents[corp_doc], total_hit_rate)


def KMP_wrapper_analysis(amt_patterns:int, amt_corpus_docs:int, pattern: str, string: str):
    for i in range(amt_corpus_docs):
        # print("i = {i}".format(i=i))
        for j in range(amt_patterns):
            # print("j = {j}".format(j=j))
            KMPSearch(pattern, string)


def LCSS_wrapper(corpus: Corpus, plagiarized: Document, results: Results):
    for i, corp_doc in enumerate(corpus.documents):
        total_hit_rate = 0
        if VERBOSE: print()
        print("LCSS() starting...\n---> Potentially plagiarized input: '{plag}'\n---> Corpus document: '{corp}' (document {x} of {x_len})\n".format(plag=plagiarized.filename, corp=corp_doc, x=(i + 1), x_len=len(corpus.documents)))
        for pattern in plagiarized.paragraphs:
            total_hit_rate += LCSS(corpus.documents[corp_doc].raw_text, pattern)
            if pattern is plagiarized.paragraphs[len(plagiarized.paragraphs) - 1]: # If we are checking the last paragraph:
                if VERBOSE:
                    if total_hit_rate == 0:
                        print("No pattern matches found.")
                    print("\n------------------------------------------------------------")
                    print("Total plagiarism hit rate of '{plag_doc}' in '{corp_doc}': {rate:.2f}%".format(plag_doc=plagiarized.filename, corp_doc=corp_doc, rate=total_hit_rate))
                    hit_rate_analysis(total_hit_rate)
                    print("------------------------------------------------------------")
                results.add(corpus.documents[corp_doc], total_hit_rate)


def LCSS_wrapper_analysis(amt_patterns:int, amt_corpus_docs:int, pattern: str, string: str):
    for i in range(amt_corpus_docs):
        # print("i = {i}".format(i=i))
        for j in range(amt_patterns):
            # print("j = {j}".format(j=j))
            LCSS(string, pattern)


def rabinkarp_wrapper(corpus: Corpus, plagiarized: Document, results: Results):
    for i, corp_doc in enumerate(corpus.documents):
        total_hit_rate = 0
        if VERBOSE: print()
        print("RabinKarp() starting...\n---> Potentially plagiarized input: '{plag}'\n---> Corpus document: '{corp}' (document {x} of {x_len})\n".format(plag=plagiarized.filename, corp=corp_doc, x=(i + 1), x_len=len(corpus.documents)))
        for pattern in plagiarized.sentences:
            total_hit_rate += RabinKarp(pattern, corpus.documents[corp_doc].raw_text)
            if pattern is plagiarized.sentences[len(plagiarized.sentences) - 1]:
                if VERBOSE:
                    if total_hit_rate == 0:
                        print("No pattern matches found.")
                    print("\n------------------------------------------------------------")
                    print("Total plagiarism hit rate of '{plag_doc}' in '{corp_doc}': {rate:.2f}%".format(plag_doc=plagiarized.filename, corp_doc=corp_doc, rate=total_hit_rate))
                    hit_rate_analysis(total_hit_rate)
                    print("------------------------------------------------------------")
                results.add(corpus.documents[corp_doc], total_hit_rate)


def rabinkarp_wrapper_analysis(amt_patterns:int, amt_corpus_docs:int, pattern: str, string: str):
    for i in range(amt_corpus_docs):
        # print("i = {i}".format(i=i))
        for j in range(amt_patterns):
            # print("j = {j}".format(j=j))
            RabinKarp(pattern, string)


def hit_rate_analysis(rate: int):
    if rate > 20:
        print("This document has an extremely high plagiarism threshhold and has been flagged for review.")
    elif rate > 10:
        print("It is possible this document is plagiarized, but further inspection is suggested.")
    elif rate == 0:
        print("This document is not plagiarized.")
    else:
        print("It is unlikely that this document is plagiarized.")


def square_n(n:list):
    for i in range(len(n)):
        for i in range(len(n)):
            True


if __name__ == '__main__':
    if VERBOSE:
        print("Verbose output enabled.")

    # If analysis mode of any algorithm is enabled, do not conduct plagiarism search (disable analysis mode in 'config.ini'):
    if not ANALYSIS_KMP and not ANALYSIS_KMP_WRAPPER and not ANALYSIS_LCSS and not ANALYSIS_LCSS_WRAPPER and not ANALYSIS_RabinKarp and not ANALYSIS_RabinKarp_WRAPPER:
        # Get the potentially plagiarized document:
        plagiarized = compile_plag_document()
        if plagiarized is False:
            print("Application closing as there is no document to check for plagiarism. Please place a document of type '.txt' into directory '{dir}' and run the program again.".format(dir=os.path.join(PLAG_DIR)))
            sys.exit()
        else:
            print("Valid document found: '{doc}'".format(doc=plagiarized.filename))
            plagiarized.info()

        # Use a singular document as input for the corpus (each individual line in the file is treated as a single document), or a set of individual documents:
        if CORPUS_USE_SINGULAR:
            # Get single input document to populate the corpus (CorpusDirectorySingular in config.ini):
            documents = extract_corpus_files()
            if documents is False:
                print("Application closing as there is no document to construct a corpus. Please place a document of type '.txt' into directory '{dir}' and run the program again.".format(dir=os.path.join(CORPUS_DIR_SINGULAR)))
                sys.exit()
            else:
                print("Valid set of documents created.")
        else:
            # Scan for multiple input documents to populate the corpus (CorpusDirectoryMultiple in config.ini):
            documents = compile_corpus_documents()
            if documents is False:
                print("Application closing as there are no documents to construct a corpus. Please place documents of type '.txt' into directory '{dir}' and run the program again.".format(dir=os.path.join(CORPUS_DIR)))
                sys.exit()
            else:
                print("Valid set of documents created.")

        # Construct the corpus from the found documents:
        corpus = compile_corpus(documents)
        if corpus is False:
            print("Application closing as an error was encountered when compiling the corpus.")
            sys.exit()
        else:
            print("A valid corpus has been created.")
            corpus.info()

        # Conduct KMPSearch on each sentence in the plagiarized document against the raw text of all corpus documents:
        if ENABLE_KMP:
            kmp_results = Results()
            KMP_wrapper(corpus, plagiarized, kmp_results)
        else:
            print("\nKMPSearch() has been disabled for plagiarism detection.")

        # Conduct LCSS on the each paragraph of the plagiarized document against the raw text of all corpus documents:
        if ENABLE_LCSS:
            lcss_results = Results()
            LCSS_wrapper(corpus, plagiarized, lcss_results)
        else:
            print("LCSS() has been disabled for plagiarism detection.")

        if ENABLE_RabinKarp:
            rabinkarp_results = Results()
            rabinkarp_wrapper(corpus, plagiarized, rabinkarp_results)
        else:
            print("\nKMPSearch() has been disabled for plagiarism detection.")

        if VERBOSE:
            print("Plagiarism detection on document '{doc}' against {corpus} was successfully completed.".format(doc=plagiarized.filename,corpus=corpus.keys))
        else:
            print("Plagiarism detection on document '{doc}' against {size} corpus documents was successfully completed.".format(doc=plagiarized.filename,size=len(corpus.documents)))
        print("\n-------------------- RESULTS SUMMARY --------------------\n")
        if ENABLE_KMP:
            print("*** Results for KMPSearch algorithm:")
            kmp_results.display()
            print()
        if ENABLE_LCSS:
            print("*** Results for LCSS algorithm:")
            lcss_results.display()
            print()
        if ENABLE_RabinKarp:
            print("*** Results for RabinKarp algorithm:")
            rabinkarp_results.display()
            print()


    # Runtime analysis of KMP (set RuntimeAnalysis_KMP to True in 'config.ini'):
    if ANALYSIS_KMP:
        # Plot basic n^2 function:
        # nValues, tValues = tryItABunch(square_n, startN=10, endN=1000, stepSize=10, numTrials=20, listMax = 10)
        # plt.plot(nValues, tValues, color="blue", label="n^2") 

        # Plot KMPSearch(): m = n:
        nValuesEqual, tValuesEqual = tryItABunchKMPEqual( KMPSearch, startN = 50, endN = 20000, stepSize=50, numTrials=20)
        plt.plot(nValuesEqual, tValuesEqual, color="blue", label="KMPSearch() m = n")

        # Plot KMPSearch(): m < n:
        nValues, tValues = tryItABunchKMP( KMPSearch, startN = 50, endN = 20000, stepSize=50, numTrials=10, patternLength = 20)
        plt.plot(nValues, tValues, color="red", label="KMPSearch() m < n")

        # # Plot KMPSearch(): m > n:
        nValuesLargePat, tValuesLargePat = tryItABunchKMPLargePat( KMPSearch, startN = 50, endN = 20000, stepSize=50, numTrials=10, stringLength = 20)
        plt.plot(nValuesLargePat, tValuesLargePat, color="green", label="KMPSearch() m > n")

        plt.xlabel("Length of string, n", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("KMPSearch Runtimes", fontsize=30)
        plt.show()


    if ANALYSIS_KMP_WRAPPER:
        # Plot KMP_wrapper(): w = z
        nValuesWrap, tValuesWrap = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1)
        plt.plot(nValuesWrap, tValuesWrap, color="red", label="KMP_wrapper(KMPSearch()) w = z; n = z, m = z")
        
        # Plot KMP_wrapper(): w < z
        nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsSmaller = True)
        plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="yellow", label="KMP_wrapper(KMPSearch()) w < z, w = (z / 2); n = z, m = z")
        
        # Plot KMP_wrapper(): w > z
        nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsLarger = True)
        plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="green", label="KMP_wrapper(KMPSearch()) w > z, w = (z * 2); n = z, m = z")

        plt.xlabel("Length of set S[], z", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("KMPSearch Runtimes within Wrapper Function", fontsize=30)
        plt.show()


    # Runtime analysis of LCSS (set RuntimeAnalysis_LCSS to True in 'config.ini'):
    if ANALYSIS_LCSS:
        # Plot basic n^2 function:
        # nValues, tValues = tryItABunch(square_n, startN=10, endN=1000, stepSize=10, numTrials=20, listMax = 10)
        # plt.plot(nValues, tValues, color="blue", label="n^2") 

        # Plot LCSS(): m = n:
        nValuesEqual, tValuesEqual = tryItABunchLCSSEqual( LCSS, startN = 50, endN = 1000, stepSize=50, numTrials=10)
        plt.plot(nValuesEqual, tValuesEqual, color="blue", label="LCSS() m = n")

        # Plot LCSS(): m < n:
        nValues, tValues = tryItABunchLCSS( LCSS, startN = 50, endN = 10000, stepSize=50, numTrials=10, patternLength = 20)
        plt.plot(nValues, tValues, color="red", label="LCSS() m < n")

        # # Plot LCSS(): m > n:
        nValuesLargePat, tValuesLargePat = tryItABunchLCSSLargePat( LCSS, startN = 50, endN = 10000, stepSize=50, numTrials=10, stringLength = 20)
        plt.plot(nValuesLargePat, tValuesLargePat, color="green", label="LCSS() m > n")

        plt.xlabel("Length of string, n", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("LCSS Runtimes", fontsize=30)
        plt.show()


    if ANALYSIS_LCSS_WRAPPER:
        # Plot LCSS_wrapper(): w = z
        nValuesWrap, tValuesWrap = tryItABunchLCSSWrapper( LCSS_wrapper_analysis, startN = 50, endN = 500, stepSize=50, numTrials=1)
        plt.plot(nValuesWrap, tValuesWrap, color="red", label="LCSS_wrapper(LCSS()) w = z; n = z, m = z")
        
        # Plot LCSS_wrapper(): w < z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchLCSSWrapper( LCSS_wrapper_analysis, startN = 50, endN = 250, stepSize=50, numTrials=1, amtPatternsSmaller = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="yellow", label="LCSS_wrapper(LCSS()) w < z, w = (z / 2); n = z, m = (z / 2)")
        
        # Plot LCSS_wrapper(): w > z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchLCSSWrapper( LCSS_wrapper_analysis, startN = 50, endN = 250, stepSize=50, numTrials=1, amtPatternsLarger = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="green", label="LCSS_wrapper(LCSS()) w > z, w = (z * 2); n = z, m = (z * 2)")

        plt.xlabel("Length of set S[], z", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("LCSS Runtimes within Wrapper Function", fontsize=30)
        plt.show()


    # Runtime analysis of RabinKarp (set RuntimeAnalysis_RabinKarp to True in 'config.ini'):
    if ANALYSIS_RabinKarp:
        # Plot basic n^2 function:
        # nValues, tValues = tryItABunch(square_n, startN=10, endN=1000, stepSize=10, numTrials=20, listMax = 10)
        # plt.plot(nValues, tValues, color="blue", label="n^2")

        # Plot KMPSearch(): m = n:
        nValuesEqual, tValuesEqual = tryItABunchKMPEqual( RabinKarp, startN = 50, endN = 10000, stepSize=50, numTrials=10)
        # nValuesEqual2, tValuesEqual2 = tryItABunchRabinKarpEqual( RabinKarp, startN = 50, endN = 10000, stepSize=50, numTrials=10)
        plt.plot(nValuesEqual, tValuesEqual, color="blue", label="RabinKarp() m = n")
        # plt.plot(nValuesEqual2, tValuesEqual2, color="darkblue", label="RabinKarp() m = n")

        # Plot KMPSearch(): m < n:
        nValues, tValues = tryItABunchKMP( RabinKarp, startN = 50, endN = 10000, stepSize=50, numTrials=10, patternLength = 20)
        plt.plot(nValues, tValues, color="red", label="RabinKarp() m < n")

        # # Plot KMPSearch(): m > n: *** THIS IS AN INVALID TEST AS m MUST BE <= n ***
        # nValuesLargePat, tValuesLargePat = tryItABunchKMPLargePat( RabinKarp, startN = 50, endN = 10000, stepSize=50, numTrials=10, stringLength = 20)
        # plt.plot(nValuesLargePat, tValuesLargePat, color="green", label="RabinKarp() m > n")

        plt.xlabel("Length of string, n", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("RabinKarp Runtimes", fontsize=30)
        plt.show()


    if ANALYSIS_RabinKarp_WRAPPER:
        # Plot KMP_wrapper(): w = z
        nValuesWrap, tValuesWrap = tryItABunchKMPWrapper( rabinkarp_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1)
        plt.plot(nValuesWrap, tValuesWrap, color="red", label="rabinkarp_wrapper(RabinKarp()) w = z; n = z, m = z")
        
        # Plot KMP_wrapper(): w < z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( rabinkarp_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsSmaller = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="yellow", label="rabinkarp_wrapper(RabinKarp()) w < z, w = (z / 2); n = z, m = z")
        
        # Plot KMP_wrapper(): w > z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( rabinkarp_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsLarger = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="green", label="rabinkarp_wrapper(RabinKarp()) w > z, w = (z * 2); n = z, m = z")

        plt.xlabel("Length of set S[], z", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("RabinKarp Runtimes within Wrapper Function", fontsize=30)
        plt.show()


    if ANALYSIS_ALL:
        '''
        KMP ANALYSIS
        '''
        # Plot KMPSearch(): m = n:
        nValuesEqual, tValuesEqual = tryItABunchKMPEqual( KMPSearch, startN = 50, endN = 10000, stepSize=50, numTrials=20)
        plt.plot(nValuesEqual, tValuesEqual, color="red", label="KMPSearch() m = n")
        # Plot KMPSearch(): m < n:
        # nValues, tValues = tryItABunchKMP( KMPSearch, startN = 50, endN = 20000, stepSize=50, numTrials=10, patternLength = 20)
        # plt.plot(nValues, tValues, color="red", label="KMPSearch() m < n")
        # # Plot KMPSearch(): m > n:
        # nValuesLargePat, tValuesLargePat = tryItABunchKMPLargePat( KMPSearch, startN = 50, endN = 20000, stepSize=50, numTrials=10, stringLength = 20)
        # plt.plot(nValuesLargePat, tValuesLargePat, color="red", label="KMPSearch() m > n")

        '''
        LCSS ANALYSIS
        '''
        # Plot LCSS(): m = n:
        # nValuesEqual, tValuesEqual = tryItABunchLCSSEqual( LCSS, startN = 50, endN = 1000, stepSize=50, numTrials=10)
        # plt.plot(nValuesEqual, tValuesEqual, color="green", label="LCSS() m = n")
        # Plot LCSS(): m < n:
        # nValues, tValues = tryItABunchLCSS( LCSS, startN = 50, endN = 5000, stepSize=50, numTrials=10, patternLength = 20)
        # plt.plot(nValues, tValues, color="green", label="LCSS() m < n")
        # # Plot LCSS(): m > n:
        # nValuesLargePat, tValuesLargePat = tryItABunchLCSSLargePat( LCSS, startN = 50, endN = 5000, stepSize=50, numTrials=10, stringLength = 20)
        # plt.plot(nValuesLargePat, tValuesLargePat, color="green", label="LCSS() m > n")

        '''
        RABIN-KARP ANALYSIS
        '''
        # Plot KMPSearch(): m = n:
        nValuesEqual, tValuesEqual = tryItABunchKMPEqual( RabinKarp, startN = 50, endN = 10000, stepSize=50, numTrials=20)
        # nValuesEqual, tValuesEqual = tryItABunchRabinKarpEqual( RabinKarp, startN = 50, endN = 10000, stepSize=50, numTrials=10)
        plt.plot(nValuesEqual, tValuesEqual, color="blue", label="RabinKarp() m = n")
        # Plot KMPSearch(): m < n:
        # nValues, tValues = tryItABunchKMP( RabinKarp, startN = 50, endN = 1000, stepSize=50, numTrials=10, patternLength = 20)
        # plt.plot(nValues, tValues, color="blue", label="RabinKarp() m < n")
        # # Plot KMPSearch(): m > n:
        # nValuesLargePat, tValuesLargePat = tryItABunchKMPLargePat( RabinKarp, startN = 50, endN = 1000, stepSize=50, numTrials=10, stringLength = 20)
        # plt.plot(nValuesLargePat, tValuesLargePat, color="blue", label="RabinKarp() m > n")

        plt.xlabel("Length of string, n", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("Algorithm Runtimes", fontsize=30)
        plt.show()


    if ANALYSIS_ALL_WRAPPER:
        '''
        KMP WRAPPER ANALYSIS
        '''
        # Plot KMP_wrapper(): w = z
        nValuesWrap, tValuesWrap = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1)
        plt.plot(nValuesWrap, tValuesWrap, color="red", label="KMP_wrapper(KMPSearch()) w = z; n = z, m = z")
        # Plot KMP_wrapper(): w < z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsSmaller = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="red", label="KMP_wrapper(KMPSearch()) w < z, w = (z / 2); n = z, m = z")
        # Plot KMP_wrapper(): w > z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsLarger = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="red", label="KMP_wrapper(KMPSearch()) w > z, w = (z * 2); n = z, m = z")


        '''
        LCSS WRAPPER ANALYSIS
        '''
        # Plot LCSS_wrapper(): w = z
        # nValuesWrap, tValuesWrap = tryItABunchLCSSWrapper( LCSS_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1)
        # plt.plot(nValuesWrap, tValuesWrap, color="green", label="LCSS_wrapper(LCSS()) w = z; n = z, m = z")
        # Plot LCSS_wrapper(): w < z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchLCSSWrapper( LCSS_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsSmaller = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="green", label="LCSS_wrapper(LCSS()) w < z, w = (z / 2); n = z, m = z")
        # Plot LCSS_wrapper(): w > z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchLCSSWrapper( LCSS_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsLarger = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="green", label="LCSS_wrapper(LCSS()) w > z, w = (z * 2); n = z, m = z")

        '''
        RABIN-KARP WRAPPER ANALYSIS
        '''
        # Plot KMP_wrapper(): w = z
        nValuesWrap, tValuesWrap = tryItABunchKMPWrapper( rabinkarp_wrapper_analysis, startN = 50, endN = 500, stepSize=50, numTrials=1)
        plt.plot(nValuesWrap, tValuesWrap, color="blue", label="rabinkarp_wrapper(RabinKarp()) w = z; n = z, m = z")
        # Plot KMP_wrapper(): w < z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( rabinkarp_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsSmaller = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="blue", label="rabinkarp_wrapper(RabinKarp()) w < z, w = (z / 2); n = z, m = z")
        # Plot KMP_wrapper(): w > z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( rabinkarp_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsLarger = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="blue", label="rabinkarp_wrapper(RabinKarp()) w > z, w = (z * 2); n = z, m = z")

        plt.xlabel("Length of set S[], z", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("Algorithm Runtimes within Wrapper Functions", fontsize=30)
        plt.show()