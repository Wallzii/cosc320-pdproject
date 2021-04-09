import configparser

import document

config = configparser.ConfigParser()
config.read('config.ini')
VERBOSE = config.getboolean('DEFAULT', 'VerboseMode')


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

    def add_document(self, filename: str, doc: document.Document):
        """Adds a Document object to the documents dictionary of the corpus."""
        if type(doc) is document.Document:
            self.documents[filename] = doc
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