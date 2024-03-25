import glob
import os
import pprint

from gensim import corpora, models, similarities
from Wordnet.wordnet_functs import remove_punct
from nltk.corpus import stopwords as sw


def sentence_sim(txt_file):
    document = "In the beginning, God created the Heavens and the Earth."
    text_corpus = get_corpus(txt_directory=txt_file)
    no_stop = []
    i = 0
    for documents in text_corpus:
        if i > 10:
            break
        for word in remove_punct(documents).lower().split(' '):
            if word not in sw.words():
                no_stop.append(word)
                print(f'{word} from {documents}')
        i+=1
    # no_stop = [[word for word in remove_punct(documents).lower().split(' ') if word not in sw.words()] for documents in text_corpus]
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in no_stop:
        for token in text:
            frequency[token] += 1
    processed_corpus = [[token for token in text if frequency[token] > 1] for text in no_stop]
    pprint.pprint(processed_corpus)
    dictionary = corpora.Dictionary(processed_corpus)

    new_vec = dictionary.doc2bow(document.lower().split(' '))
    bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]
    tfidf = models.TfidfModel(bow_corpus)

    index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=len(dictionary))
    sims = index[tfidf[new_vec]]
    print(list(enumerate(sims)))


def get_corpus(txt_directory):
    document = "In the beginning, God created the Heavens and the Earth"
    tokens = []
    txt_directory_size = len(txt_directory) + 1
    # creates the directory if it doesn't exist
    if not os.path.exists(os.path.join(os.getcwd(), txt_directory)):
        os.makedirs(txt_directory)
        print(f'Directory Not Found: {txt_directory}')
        raise Exception(f"Directory Not Found: {txt_directory}");

    # grabs all translation files from the directory
    for filename in glob.glob(os.path.join(txt_directory, '*.txt')):
        with open(os.path.join(os.getcwd(), filename), mode='r', encoding='utf-8') as file:
            for line in file.readlines():
                tokens.append(line.strip())
            break
    if not tokens:
        print(f'Empty Directory: {txt_directory}')
        raise Exception(f'Empty Directory: {txt_directory}')
    return tokens
