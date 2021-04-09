import re
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
VERBOSE = config.getboolean('DEFAULT', 'VerboseMode')


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
            sentences = self.__split_sentences(raw_text)
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


    def __split_sentences(self, string) -> list:
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