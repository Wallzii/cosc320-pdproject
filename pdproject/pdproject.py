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
        self.num_sentences = 0
        self.sentences = []

    def add_paragraphs(self, paragraphs):
        self.paragraphs += paragraphs

    def add_sentence(self, sentence):
        self.sentences.append(sentence)
        self.num_sentences += 1

    def info(self):
        print("Filename:", self.filename)
        print("# paragraphs: {num}".format(num=len(self.paragraphs)))
        print("# sentences: {num}".format(num=self.num_sentences))

    def print_paragraphs(self):
        if len(self.paragraphs) > 0:
            print("Paragraphs in '{filename}':".format(filename=self.filename))
            for i, para in enumerate(self.paragraphs):
                print("{file}->paragraphs[{i}]: {para}".format(file=self.filename, i=i, para=para))
        else:
            print("No paragraphs in '{filename}' to display.".format(filename=self.filename))

    def print_sentences(self):
        if self.num_sentences > 0:
            print("Sentences in '{filename}':".format(filename=self.filename))
            for i, sentence in enumerate(self.sentences):
                print("sentence[{i}]: {sentence}".format(i=i, sentence=sentence))
        else:
            print("No sentences in '{filename}' to display.".format(filename=self.filename))

class Corpus:
    def __init__(self):
        self.num_documents = 0
        self.documents = []

    def add_document(self, document: Document):
        if type(document) is Document:
            self.documents.append(document)
            self.num_documents += 1
        else:
            raise TypeError("Parameter of add_document() must be of type Document.")

    def info(self):
        print("# documents in corpus: {num}".format(num=self.num_documents))
        self.__print_documents()

    def __print_documents(self):
        if self.num_documents > 0:
            for i, document in enumerate(self.documents):
                print("document[{i}]: {document}".format(i=i, document=document.filename))
        else:
            print("No documents in Corpus to display.")

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
                documents.append(doc)
    return documents

if __name__ == '__main__':
    documents = compile_documents()
    documents[0].info()
    documents[0].print_paragraphs()