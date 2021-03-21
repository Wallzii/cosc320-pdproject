def KMP(plag_sentences: list, doc_sentences: list):
    if type(plag_sentences) != list or type(doc_sentences) != list:
        print("Input parameters for function KMP must of type 'list'.")
    else:
        print("Plagiarized input: {list}".format(list=plag_sentences))
        print("Document input: {list}".format(list=doc_sentences))