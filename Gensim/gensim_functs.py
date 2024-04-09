import glob
import os
import pprint
import smart_open
import nltk.tokenize as tok
import gensim
from gensim import corpora, models, similarities, downloader as api
from gensim.models.doc2vec import Doc2Vec, Word2Vec
from Wordnet.wordnet_functs import remove_punct, remove_punct_tokens
from nltk.corpus import stopwords as sw

### TODO: make a class for these functions and make class variables for easier use
lang_dir = 'DBTextFiles'
tmp_model = 'model\gensim.model'
word_embeddings = 'model\Word2Vec.model'
save_file = os.path.join(os.getcwd(), tmp_model)
save_embeddings = os.path.join(os.getcwd(), word_embeddings)

def train_doc2vec(txt_file, filelimit=1, linelimit=200, epochs=500 ):
    # train_corpus = [TaggedDocument(words=doc, tags=[i]) for i, doc in enumerate(read_corpus(txt_file))]
    train_corpus = list(read_corpus(txt_file))
    # test_corpus = list(read_corpus(lee_test_file, tokens_only=True))
    if os.path.exists(save_file):
        print(f'Save File Found: {save_file}')
        try:
            model = Doc2Vec.load(save_file)
        except Exception as e:
            print(f"Error loading existing model: {e}")
            return None
    else:
        print('Creating save file location...')
        temp_dir = os.getcwd()
        for item in tmp_model.split('\\'):
            if '.model' not in item and not os.path.exists(os.path.join(temp_dir, item)):
                temp_dir = os.path.join(temp_dir, item)
                os.makedirs(temp_dir)
        model = gensim.models.doc2vec.Doc2Vec(vector_size=300, min_count=2, epochs=epochs)

    model.build_vocab(train_corpus)
    # train_x = np.array([model.infer_vector(doc.words) for doc in train_corpus])
    # train_x_torch = torch.tensor(train_x, dtype=torch.float32, device=device)
    print('Training Model...')
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    print('Training complete!')
    # model.train(train_x_torch)
    print('Saving file...')
    model.save(save_file)
    print('Saving complete!')
    return model


def read_corpus(fname, tokens_only=False):  # grabs all translation files from the directory
    # for filename in glob.glob(os.path.join(lang_dir, '*.txt'))[:filelimit]:
    filename = os.path.join(os.path.join(os.getcwd(), lang_dir), fname)
    # print(f'{filename} vs {fname}')
    with smart_open.open(filename, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            if line.strip():
                tokens = gensim.utils.simple_preprocess(line)
                if tokens_only:
                    yield tokens
                else:
                    # For training data, add tags
                    yield gensim.models.doc2vec.TaggedDocument(tokens, [i])


def sentence_sim(txt_file, infer_val = 'And God said , Let there be light : and there was light .', filelimit=1, linelimit=5):
    if os.path.exists(os.path.join(os.getcwd(), tmp_model)):
        print(f'Save File Found: {save_file}')
        model = Doc2Vec.load(save_file)
    else:
        raise FileNotFoundError("Model does not exist. Cannot check similarities")

    # vector = model.infer_vector(
    #     ['And', 'God', 'said', 'Let', 'there', 'be', 'light', 'and', 'there', 'was', 'light'])
    vector = model.infer_vector(
        remove_punct_tokens(tok.word_tokenize("Y dijo Dios: Sea la luz: y fue la luz."))
    )
    sims = model.dv.most_similar([vector], topn=len(model.dv))

    print(f'Inferred Sim: {sims[0:linelimit]}')
    printed = 0
    txt_file_path = os.path.join(os.path.join(os.getcwd(),lang_dir), txt_file)
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # Print sentences with similarity scores
        for index, similarity_score in sims:
            # Ensure index is within the range of lines
            if 0 <= index < len(lines) and lines[index].strip():
                line = lines[index].strip()  # Remove trailing newline character
                print(f"Line {index + 1}: {line}")
                print(f"Similarity Score: {similarity_score}")
                printed += 1
            # else:
            #     print(f"Index {index} is out of range.")
            if printed > linelimit:
                break
    # preprocessed = test_doc.split()
    # sims = model.dv.most_similar(preprocessed, topn=len(model.dv))
    # print(f'Test Sim: {sims[:linelimit]}')
    model.save_word2vec_format(word_embeddings)


from gensim.models import KeyedVectors
### TODO: complete sentence similarity generator
def word_sim(word, linelimit=5):
    if os.path.exists(os.path.join(os.getcwd(), save_embeddings)):
        print(f'Save File Found: {save_embeddings}')
        model = KeyedVectors.load_word2vec_format(save_embeddings)
    else:
        raise FileNotFoundError("Model does not exist. Cannot check similarities")

    print(model.most_similar(word)[:linelimit])

    return


### TODO: get the model training to work.
def model_training_sentence_sim(txt_dir):
    document = remove_punct("In the beginning, God created the Heavens and the Earth.").lower()
    text_corpus = set(get_corpus(txt_directory=txt_dir, linelimit=100))

    no_stop = [[word for word in remove_punct(documents).lower().split(' ')
                if word and word not in sw.words()] for documents in text_corpus]
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
    pprint.pprint(dictionary.id2token)

    new_vec = dictionary.doc2bow(document.split(' '))
    bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]
    tfidf_model = 'model/tfidf.model'
    tfidf_file = os.path.join(os.getcwd(), tmp_model)
    if not os.path.exists(tfidf_file):
        print(f'File Not Found: {tfidf_model}')
        tfidf = models.TfidfModel(bow_corpus)
    else:
        tfidf = models.TfidfModel.load(tfidf_file)
    pprint.pprint(bow_corpus)
    print(tfidf[dictionary.doc2bow(new_vec)])
    tfidf = models.TfidfModel(bow_corpus)

    index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=len(dictionary))
    query_document = document.split()
    # print(query_document)
    query_bow = dictionary.doc2bow(query_document)
    sims = index[tfidf[query_bow]]
    # tfidf.save(tmp_model)
    print(list(enumerate(sims))[:5])


def get_corpus(txt_directory, filelimit=1, linelimit=10):
    document = "In the beginning, God created the Heavens and the Earth"
    tokens = []

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
