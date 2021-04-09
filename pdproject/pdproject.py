import os
import sys
import configparser

import document
import corpus
import results
import kmp
import lcss
import rabinkarp


config = configparser.ConfigParser()
config.read('config.ini')
CORPUS_DIR = config['DEFAULT']['CorpusDirectoryMultiple']
CORPUS_DIR_SINGULAR = config['DEFAULT']['CorpusDirectorySingular']
PLAG_DIR = config['DEFAULT']['PlagiarizedDirectory']
CORPUS_USE_SINGULAR = config.getboolean('DEFAULT', 'CorpusUseSingular')
VERBOSE = config.getboolean('DEFAULT', 'VerboseMode')
ENABLE_KMP = config.getboolean('ALGORITHMS', 'Enable_KMP')
ENABLE_LCSS = config.getboolean('ALGORITHMS', 'Enable_LCSS')
ENABLE_RABIN_KARP = config.getboolean('ALGORITHMS', 'Enable_RabinKarp')


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
                doc = document.Document(file)
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
            doc = document.Document(file[0])
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
            doc = document.Document(file[0])
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
                temp_doc = document.Document(filename)
                raw_text = doc.paragraphs[i]
                temp_doc.parse(raw_text)
                documents.append(temp_doc)
        return documents
    else:
        print("Invalid file type found: '{dir}'".format(dir=os.path.join(PLAG_DIR, file[0])))
        print("Directory '{dir}' must contain only one file of type '.txt' and no sub-directories.".format(dir=os.path.join(PLAG_DIR)))
        return False


def compile_corpus(documents: list) -> corpus.Corpus:
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
    corp = corpus.Corpus()
    for document in documents:
        try:
            corp.add_document(document.filename, document)
        except TypeError:
            print("Parameter of add_document() was {type} and must be of type 'Document'.".format(type=type(document)))
            return False
        except:
            return False
    return corp


def KMP_wrapper(corpus: corpus.Corpus, plagiarized: document.Document, results: results.Results):
    """
    Wrapper function to run KMP against a corpus of documents.
    """
    for i, corp_doc in enumerate(corpus.documents):
        total_hit_rate = 0
        if VERBOSE: print()
        print("KMPSearch() starting...\n---> Potentially plagiarized input: '{plag}'\n---> Corpus document: '{corp}' (document {x} of {x_len})\n".format(plag=plagiarized.filename, corp=corp_doc, x=(i + 1), x_len=len(corpus.documents)))
        for pattern in plagiarized.sentences:
            total_hit_rate += kmp.KMPSearch(pattern, corpus.documents[corp_doc].raw_text)
            if pattern is plagiarized.sentences[len(plagiarized.sentences) - 1]:
                if VERBOSE:
                    if total_hit_rate == 0:
                        print("No pattern matches found.")
                    print("\n------------------------------------------------------------")
                    print("Total plagiarism hit rate of '{plag_doc}' in '{corp_doc}': {rate:.2f}%".format(plag_doc=plagiarized.filename, corp_doc=corp_doc, rate=total_hit_rate))
                    hit_rate_analysis(total_hit_rate)
                    print("------------------------------------------------------------")
                results.add(corpus.documents[corp_doc], total_hit_rate)


def LCSS_wrapper(corpus: corpus.Corpus, plagiarized: document.Document, results: results.Results):
    """
    Wrapper function to run LCSS against a corpus of documents.
    """
    for i, corp_doc in enumerate(corpus.documents):
        total_hit_rate = 0
        if VERBOSE: print()
        print("LCSS() starting...\n---> Potentially plagiarized input: '{plag}'\n---> Corpus document: '{corp}' (document {x} of {x_len})\n".format(plag=plagiarized.filename, corp=corp_doc, x=(i + 1), x_len=len(corpus.documents)))
        for pattern in plagiarized.paragraphs:
            total_hit_rate += lcss.LCSS(corpus.documents[corp_doc].raw_text, pattern)
            if pattern is plagiarized.paragraphs[len(plagiarized.paragraphs) - 1]:
                if VERBOSE:
                    if total_hit_rate == 0:
                        print("No pattern matches found.")
                    print("\n------------------------------------------------------------")
                    print("Total plagiarism hit rate of '{plag_doc}' in '{corp_doc}': {rate:.2f}%".format(plag_doc=plagiarized.filename, corp_doc=corp_doc, rate=total_hit_rate))
                    hit_rate_analysis(total_hit_rate)
                    print("------------------------------------------------------------")
                results.add(corpus.documents[corp_doc], total_hit_rate)


def rabinkarp_wrapper(corpus: corpus.Corpus, plagiarized: document.Document, results: results.Results):
    """
    Wrapper function to run Rabin-Karp against a corpus of documents.
    """
    for i, corp_doc in enumerate(corpus.documents):
        total_hit_rate = 0
        if VERBOSE: print()
        print("RabinKarp() starting...\n---> Potentially plagiarized input: '{plag}'\n---> Corpus document: '{corp}' (document {x} of {x_len})\n".format(plag=plagiarized.filename, corp=corp_doc, x=(i + 1), x_len=len(corpus.documents)))
        for pattern in plagiarized.sentences:
            total_hit_rate += rabinkarp.RabinKarp(pattern, corpus.documents[corp_doc].raw_text)
            if pattern is plagiarized.sentences[len(plagiarized.sentences) - 1]:
                if VERBOSE:
                    if total_hit_rate == 0:
                        print("No pattern matches found.")
                    print("\n------------------------------------------------------------")
                    print("Total plagiarism hit rate of '{plag_doc}' in '{corp_doc}': {rate:.2f}%".format(plag_doc=plagiarized.filename, corp_doc=corp_doc, rate=total_hit_rate))
                    hit_rate_analysis(total_hit_rate)
                    print("------------------------------------------------------------")
                results.add(corpus.documents[corp_doc], total_hit_rate)


def hit_rate_analysis(rate: int):
    if rate > 20:
        print("This document has an extremely high plagiarism threshhold and has been flagged for review.")
    elif rate > 10:
        print("It is possible this document is plagiarized, but further inspection is suggested.")
    elif rate == 0:
        print("This document is not plagiarized.")
    else:
        print("It is unlikely that this document is plagiarized.")


if __name__ == '__main__':
    if VERBOSE:
        print("Verbose output enabled.")

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
        kmp_results = results.Results()
        KMP_wrapper(corpus, plagiarized, kmp_results)
    else:
        print("\nWARNING: KMPSearch() has been disabled for plagiarism detection.")

    # Conduct LCSS on the each paragraph of the plagiarized document against the raw text of all corpus documents:
    if ENABLE_LCSS:
        lcss_results = results.Results()
        LCSS_wrapper(corpus, plagiarized, lcss_results)
    else:
        print("WARNING: LCSS() has been disabled for plagiarism detection.")

    if ENABLE_RABIN_KARP:
        rabinkarp_results = results.Results()
        rabinkarp_wrapper(corpus, plagiarized, rabinkarp_results)
    else:
        print("WARNING: RabinKarp() has been disabled for plagiarism detection.\n")

    if ENABLE_KMP or ENABLE_LCSS or ENABLE_RABIN_KARP:
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
    if ENABLE_RABIN_KARP:
        print("*** Results for RabinKarp algorithm:")
        rabinkarp_results.display()
        print()