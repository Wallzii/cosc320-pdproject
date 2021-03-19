import re
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
CORPUS_DIR = config['DEFAULT']['CorpusDirectory']

class Document:
    def __init__(self, filename):
        self.filename = filename
        self.paragraphs = []
        self.sentences = []

    def add_paragraphs(self, paragraphs):
        self.paragraphs += paragraphs

    def add_sentences(self, sentences):
        self.sentences += sentences

    def info(self):
        print("Filename:", self.filename)
        print("# paragraphs: {num}".format(num=len(self.paragraphs)))
        print("# sentences: {num}".format(num=len(self.sentences)))

    def print_paragraphs(self):
        if len(self.paragraphs) > 0:
            print("Paragraphs in document '{filename}':".format(filename=self.filename))
            for i, para in enumerate(self.paragraphs):
                print("{file}->paragraphs[{i}]: {para}".format(file=self.filename, i=i, para=para))
        else:
            print("No paragraphs in '{filename}' to display.".format(filename=self.filename))

    def print_sentences(self):
        if len(self.sentences) > 0:
            print("Sentences in document '{filename}':".format(filename=self.filename))
            for i, sentence in enumerate(self.sentences):
                print("{file}->sentence[{i}]: {sentence}".format(file=self.filename, i=i, sentence=sentence))
        else:
            print("No sentences in '{filename}' to display.".format(filename=self.filename))

class Corpus:
    def __init__(self):
        self.documents = {}

    def add_document(self, filename, document: Document):
        if type(document) is Document:
            self.documents[filename] = document
        else:
            raise TypeError("Parameter of add_document() must be of type Document.")

    def info(self):
        print("# documents in corpus: {num}".format(num=len(self.documents)))
        self.__print_documents()

    def __print_documents(self):
        if len(self.documents) > 0:
            print("Document keys in corpus: {keys}".format(keys=[*self.documents]))
        else:
            print("No document keys in corpus to display.")

def split_sentences(st):
    sentences = re.split(r'[.?!]\s*', st)
    if sentences[-1]:
        return sentences
    else:
        return sentences[:-1]

def compile_documents() -> list:
    documents = []
    for file in os.listdir(CORPUS_DIR):
        if file.lower().endswith(".txt"):
            with open(os.path.join(CORPUS_DIR, file), 'r') as f:
                doc = Document(file)
                raw_text = f.read()
                paragraphs = raw_text.splitlines()
                paragraphs = list(filter(None, paragraphs))
                doc.add_paragraphs(paragraphs)
                sentences = split_sentences(raw_text)
                doc.add_sentences(sentences)
                documents.append(doc)
    return documents

if __name__ == '__main__':
    corpus = Corpus()
    documents = compile_documents()
    documents[0].info()
    documents[0].print_paragraphs()
    documents[0].print_sentences()
    corpus.add_document(documents[0].filename, documents[0])
    corpus.add_document(documents[1].filename, documents[1])
    corpus.info()