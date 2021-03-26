# import nltk
import re
import os
import sys
import configparser

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from kmp import KMPSearch
from tryItABunch import tryItABunch, tryItABunchKMP, tryItABunchKMPEqual, tryItABunchKMPLargePat, tryItABunchKMPWrapper, tryItABunchKMPWrapperEqual


config = configparser.ConfigParser()
config.read('config.ini')
CORPUS_DIR = config['DEFAULT']['CorpusDirectoryMultiple']
CORPUS_DIR_SINGULAR = config['DEFAULT']['CorpusDirectorySingular']
PLAG_DIR = config['DEFAULT']['PlagiarizedDirectory']
VERBOSE = config.getboolean('DEFAULT', 'VerboseMode')
ENABLE_KMP = config.getboolean('ALGORITHMS', 'Enable_KMP')
ANALYSIS_KMP = config.getboolean('ANALYSIS', 'RuntimeAnalysis_KMP')


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
            print("Corpus contains {documents} document(s): {keys}".format(documents=len(self.documents), keys=[*self.documents]))
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

    def add(self, document: Document, hit_rate: float): #97 -> 1.2
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
        self.documents.append(document.filename) # 10,000 chars/doc -> 1,000,000 docs -> 10,000,000 * 10,000 -> 100,000,000,000
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
                # print(filename)
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
    # corpus[str_1, str_2, ..., str_s] where str_1...s = some document's raw text
    # plag[pat_1, pat_2, ..., pat_p] where pat_1...p = some document's individual component sentences
    # kmp_wrapper() = O(p*s)
    # kmp() = O(m + n)
    # for corp_doc, i in corpus.documents:
    for i, corp_doc in enumerate(corpus.documents):
        total_hit_rate = 0
        print("\nKMPSearch() starting...\n---> Potentially plagiarized input: '{plag}'\n---> Corpus document: '{corp}' (document {x} of {x_len})\n".format(plag=plagiarized.filename, corp=corp_doc, x=i, x_len=len(corpus.documents)))
        for pattern in plagiarized.sentences:
            total_hit_rate += KMPSearch(pattern, corpus.documents[corp_doc].raw_text)
            if pattern is plagiarized.sentences[len(plagiarized.sentences) - 1]:
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
    if not ANALYSIS_KMP:
        # Get the potentially plagiarized document:
        plagiarized = compile_plag_document()
        if plagiarized is False:
            print("Application closing as there is no document to check for plagiarism. Please place a document of type '.txt' into directory '{dir}' and run the program again.".format(dir=os.path.join(PLAG_DIR)))
            sys.exit()
        else:
            print("Valid document found: '{doc}'".format(doc=plagiarized.filename))
            plagiarized.info()

        # Scan for multiple input documents to populate the corpus (CorpusDirectoryMultiple in config.ini):
        # documents = compile_corpus_documents()
        # if documents is False:
        #     print("Application closing as there are no documents to construct a corpus. Please place documents of type '.txt' into directory '{dir}' and run the program again.".format(dir=os.path.join(CORPUS_DIR)))
        #     sys.exit()
        # else:
        #     print("Valid set of documents created.")

        # Scan single input document to populare the corpus (CorpusDirectorySingular in config.ini):
        documents = extract_corpus_files()

        # Construct the corpus from the found documents:
        corpus = compile_corpus(documents)
        if corpus is False:
            print("Application closing as an error was encountered when compiling the corpus.")
            sys.exit()
        else:
            print("A valid corpus has been created.")
            corpus.info()

        # Create empty results object for statistics tracking:
        results = Results()

        # Conduct KMPSearch on the first sentence of the plagiarized document against the raw text of the first corpus document:
        if ENABLE_KMP:
            KMP_wrapper(corpus, plagiarized, results)
        else:
            print("KMPSearch() has been disabled for plagiarism detection.")

        print("\nPlagiarism detection on document '{doc}' against {corpus} was successfully completed.".format(doc=plagiarized.filename,corpus=corpus.keys))
        results.display(show_quartiles=False)


    # Runtime analysis of KMP (set RuntimeAnalysis_KMP to True in 'config.ini'):
    if ANALYSIS_KMP:
        # Plot m < n:
        nValues, tValues = tryItABunch(square_n, startN=10, endN=1000, stepSize=10, numTrials=20, listMax = 10)
        plt.plot(nValues, tValues, color="blue", label="square_n()")

        # nValues, tValues = tryItABunchKMP( KMPSearch, startN = 50, endN = 20000, stepSize=50, numTrials=10, patternLength = 10)
        # plt.plot(nValues, tValues, color="red", label="KMPSearch() m < n")

        # nValues, tValues = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 1, endN = 2, stepSize=1, numTrials=1, patternLength = 10, amt_patterns = 25, amt_corpus_docs = 100)
        # plt.plot(nValues, tValues, color="darkred", label="KMP_wrapper(KMPSearch()) m < n, pat=25,corp=100")

        nValuesWrap, tValuesWrap = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, patternLength = 10)
        plt.plot(nValuesWrap, tValuesWrap, color="red", label="KMP_wrapper(KMPSearch()) m < n, P.length = n ,S.len = n, m = 10, s.len = n")
        nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, patternLength = 10, amtPatternsSmaller = True)
        plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="yellow", label="KMP_wrapper(KMPSearch()) m < n, P.length = n / 2 ,S.len = n, m = 10, s.len = n")
        nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, patternLength = 10, amtPatternsLarger = True)
        plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="green", label="KMP_wrapper(KMPSearch()) m < n, P.length = n * 2 ,S.len = n, m = 10, s.len = n")

        # Plot m = n:
        # nValuesEqual, tValuesEqual = tryItABunchKMPEqual( KMPSearch, startN = 50, endN = 20000, stepSize=50, numTrials=10)
        # plt.plot(nValuesEqual, tValuesEqual, color="blue", label="KMPSearch() m = n")

        # nValuesEqual, tValuesEqual = tryItABunchKMPWrapperEqual( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amt_patterns = 100, amt_corpus_docs = 100)
        # plt.plot(nValuesEqual, tValuesEqual, color="blue", label="KMP_wrapper() m = n")

        # # Plot m > n:
        # nValuesLargePat, tValuesLargePat = tryItABunchKMPLargePat( KMPSearch, startN = 50, endN = 20000, stepSize=50, numTrials=10, stringLength = 10)
        # plt.plot(nValuesLargePat, tValuesLargePat, color="green", label="KMPSearch() m > n")

        plt.xlabel("n")
        plt.ylabel("Time(ms)")
        plt.legend()
        plt.title("KMPSearch Runtimes")
        plt.show()