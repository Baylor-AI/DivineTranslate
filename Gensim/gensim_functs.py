import glob
import os
import pprint
import json
from gensim import corpora, models, similarities, downloader as api
from gensim.models.doc2vec import Doc2Vec
from gensim.models.word2vec import Word2Vec
from Wordnet.wordnet_functs import remove_punct
from nltk.corpus import stopwords as sw

tmp_model = '/tmp/gensim.model'

def sentence_sim(txt_file, filelimit=1, linelimit=200):
    corpus = api.load('text8')
    text_corpus = set(get_corpus(txt_directory=txt_file, filelimit=filelimit, linelimit=linelimit))
    processed_text = corpus
    sentences = [s for s in processed_text.sents]
    print(sentences)
    processed_sentences = [sent.lemma_.split() for sent in processed_text.sents]
    # model = Word2Vec(
    #     sentences=processed_sentences,
    #     min_count=10,
    #     size=200,
    #     window=2,
    #     compute_loss=True,
    #     sg=1
    # )
    model = Doc2Vec(
        sentences=processed_sentences,
        min_count=10,
        size=200,
        window=2,
        compute_loss=True,
        sg=1
    )
    print(len(model.wv.vocab))
    info = api.info()
    # print(json.dumps(info, indent=4))
    # print(info.keys())
    document = remove_punct("In the beginning, God created the Heavens and the Earth.").lower()
    doc2 = remove_punct("En el principio Dios creó los cielos y la tierra.")
    print(model.dv.most_similar(document))

def model_training_sentence_sim(txt_file):
    document = remove_punct("In the beginning, God created the Heavens and the Earth.").lower()
    text_corpus = set(get_corpus(txt_directory=txt_file, linelimit=100000))
    # print(text_corpus)
    # no_stop = []
    # i = 0
    # for documents in text_corpus:
    #     if i > 10:
    #         break
    #     for word in remove_punct(documents).lower().split(' '):
    #         if word not in sw.words():
    #             no_stop.append(word)
    #             # print(f'{word} from {documents}')
    #     i+=1
    no_stop = [[word for word in remove_punct(documents).lower().split(' ')
                if word and word not in sw.words()] for documents in text_corpus]
    # no_stop = [[word for word in remove_punct(documents).lower().split(' ')] for documents in text_corpus]
    # print(no_stop)
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in no_stop:
        for token in text:
            frequency[token] += 1
            # print(f'{token} in {text}')
    processed_corpus = [[token for token in text if frequency[token] > 1] for text in no_stop]
    # pprint.pprint(processed_corpus)
    dictionary = corpora.Dictionary(processed_corpus)
    # pprint.pprint(dictionary.token2id)

    new_vec = dictionary.doc2bow(document.split(' '))
    bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]
    if not os.path.exists(os.path.join(os.getcwd(), tmp_model)):
        os.makedirs(tmp_model)
        print(f'Directory Not Found: {tmp_model}')
    else:
        tfidf = models.TfidfModel.load(tmp_model)
    # pprint.pprint(bow_corpus)
    # print(tfidf[dictionary.doc2bow(new_vec)])

    index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=len(dictionary))
    query_document = document.split()
    # print(query_document)
    query_bow = dictionary.doc2bow(query_document)
    sims = index[tfidf[query_bow]]
    print(list(enumerate(sims)))



def get_corpus(txt_directory, filelimit=1, linelimit=10):
    document = "In the beginning, God created the Heavens and the Earth"
    tokens = []
    txt_directory_size = len(txt_directory) + 1
    # creates the directory if it doesn't exist
    if not os.path.exists(os.path.join(os.getcwd(), txt_directory)):
        os.makedirs(txt_directory)
        print(f'Directory Not Found: {txt_directory}')
        raise Exception(f"Directory Not Found: {txt_directory}");

    # grabs all translation files from the directory
    for filename in glob.glob(os.path.join(txt_directory, '*.txt'))[:filelimit]:
        with open(os.path.join(os.getcwd(), filename), mode='r', encoding='utf-8') as file:
            for line in file.readlines()[:linelimit]:
                tokens.append(line.strip())
    if not tokens:
        print(f'Empty Directory: {txt_directory}')
        raise Exception(f'Empty Directory: {txt_directory}')
    return tokens
