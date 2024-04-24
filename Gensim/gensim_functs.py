import glob
import os
import pprint
import smart_open
import env_vars as env

import gensim
from gensim import corpora, models, similarities, downloader as api
from gensim.models.doc2vec import Doc2Vec, Word2Vec
from Wordnet.wordnet_functs import remove_punct, remove_punct_tokens
from nltk.corpus import stopwords as sw
from gensim.utils import simple_preprocess
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

### TODO: make a class for these functions and make class variables for easier use

save_file = os.path.join(os.getcwd(), env.tmp_model)
save_embeddings = os.path.join(os.getcwd(), env.word_embeddings)


#NOTE: Only works on 1 sentence at a time
def train_model(fname = ''):
    # Sample training data (English and French sentences)
    english_sentences = [
        "In the beginning God created the heaven and the earth .",
        "And the earth was without form , and void ; and darkness was upon the face of the deep . And the Spirit of God moved upon the face of the waters .",
        "And God said , Let there be light : and there was light .",
        "And God saw the light , that it was good : and God divided the light from the darkness .",
        "And God called the light Day , and the darkness he called Night . And the evening and the morning were the first day ."
    ]

    french_sentences = [
        "Au commencement , Dieu créa le ciel et la terre .",
        "Or la terre était vide et vague , les ténèbres couvraient l'abîme , un vent de Dieu tournoyait sur les eaux .",
        "Dieu dit : \" Que la lumière soit \" et la lumière fut .",
        "Dieu vit que la lumière était bonne , et Dieu sépara la lumière et les ténèbres .",
        "Dieu appela la lumière \" jour \" et les ténèbres \" nuit . \" Il y eut un soir et il y eut un matin : premier jour ."
    ]

    jpn_sentences = [
        "はじめに神は天と地とを創造された。",
        "地は形なく、むなしく、やみが淵のおもてにあり、神の霊が水のおもてをおおっていた。",
        "神は「光あれ」と言われた。すると光があった。"
    ]

    hai_sent = [
        "Hou-a ; gītsada lā dung ijung ; gin gū-dsū-dsū duman dung kang-gai lagun alth , lana a-tlāalth un dung lth ītlagadēlth-dang , waigien hin la il shudaian .",
        "Waigien nung swon ishin la un katlagan gien , Nung itlagadas , dung gia poundgai gwī pound tlēlth kāalgun , hin il shouon ."
    ]

    # Combine English, French, Spanish, and Chinese sentences
    combined_sentences = english_sentences + french_sentences + jpn_sentences + hai_sent

    ###TODO: add implementation for other ideographic languages
    # Tokenize and preprocess combined sentences
    def tokenize_sentence(sentence):
        if ("\u3040" <= sentence <= "\u30FF") or ("\u4E00" <= sentence <= "\u9FFF"):
            # If the sentence contains Chinese characters, tokenize by characters
            print(f'entered')
            return list(sentence)
        else:
            # Otherwise, tokenize by words using Gensim's simple_preprocess
            return simple_preprocess(sentence)
        ## possible per-byte implementation
        # for byte in sentence.encode(env.f_enc):
        #     if byte >= 128:
        #         # If the sentence contains Chinese characters, tokenize by characters
        #         return list(sentence)
        #
        #     else:
        #         # Otherwise, tokenize by words using Gensim's simple_preprocess
        #         return simple_preprocess(sentence)

    tokenized_combined_sentences = [tokenize_sentence(sentence) for sentence in combined_sentences]

    # Train Word2Vec model
    model = Word2Vec(tokenized_combined_sentences, vector_size=100, window=5, min_count=1, workers=4)

    # Function to get sentence vector
    def get_sentence_vector(sentence):
        words = tokenize_sentence(sentence)
        word_vectors = [model.wv[word] for word in words if word in model.wv]
        if word_vectors:
            return np.mean(word_vectors, axis=0)
        else:
            return None

    # Function to find most similar sentence
    def most_similar_sentence(input_sentence, sentences):
        input_vector = get_sentence_vector(input_sentence)
        if input_vector is not None:
            sentence_vectors = [get_sentence_vector(sentence) for sentence in sentences]
            similarities = [cosine_similarity([input_vector], [vec])[0][0] for vec in sentence_vectors]
            most_similar_index = np.argmax(similarities)
            return [sentences[most_similar_index], similarities[most_similar_index]]
            # return [sentences, similarities]
        else:
            return None

    # Example usage
    input_sentence = "め"
    most_similar = most_similar_sentence(input_sentence, combined_sentences)
    print("Input Sentence:", input_sentence)
    print("Most Similar Sentence:", most_similar)


def train_doc2vec(txt_file, vector_size=100, min_count=5, epochs=5):
    # train_corpus = [TaggedDocument(words=doc, tags=[i]) for i, doc in enumerate(read_corpus(txt_file))]
    train_corpus = list(read_corpus(txt_file))
    # test_corpus = list(read_corpus(lee_test_file, tokens_only=True))
    if os.path.exists(save_file):
        print(f'Save File Found: {save_file}')
        try:
            model = Doc2Vec.load(save_file)
            model.build_vocab(train_corpus, update=True)
        except Exception as e:
            print(f"Error loading existing model: {e}")
            return None
    else:
        print('Creating save file location...')
        temp_dir = os.getcwd()
        for item in env.tmp_model.split('\\'):
            nextdir = env.tmp_model.split('\\')
            print(f"making directory: {nextdir} -> {item}")
            if '.model' not in item and not os.path.exists(os.path.join(temp_dir, item)):
                temp_dir = os.path.join(temp_dir, item)
                os.makedirs(temp_dir)
            print(f'directory made: {temp_dir}')
        model = Doc2Vec(vector_size=vector_size, min_count=min_count, epochs=epochs)
        model.build_vocab(train_corpus)

    print('Training Doc2Vec Model...')
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    print('Training complete!')
    print('Saving Doc2Vec Model...')
    model.save(save_file)
    print('Saving complete!')
    return model


def train_word2vec(txt_file, vector_size=100, min_count=5, epochs=5):
    train_corpus = list(read_corpus(txt_file, tokens_only=True))
    if os.path.exists(save_embeddings):
        print(f'Save File Found: {save_embeddings}')
        try:
            model = Word2Vec.load(save_embeddings)
            model.build_vocab(train_corpus, update=True)
        except Exception as e:
            print(f"Error loading existing model: {e}")
            return None
    else:
        print('Creating save file location...')
        temp_dir = os.getcwd()
        for item in env.word_embeddings.split('\\'):
            if '.model' not in item and not os.path.exists(os.path.join(temp_dir, item)):
                temp_dir = os.path.join(temp_dir, item)
                os.makedirs(temp_dir)
        model = Word2Vec(vector_size=vector_size, min_count=min_count, epochs=epochs)
        model.build_vocab(train_corpus)

    print('Training Word2Vec Model...')
    print(train_corpus[:vector_size])
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    print('Training complete!')
    print('Saving Word2Vec file...')
    model.save(save_embeddings)
    print('Saving complete!')
    print(model.wv.key_to_index)
    return model


def read_corpus(fname, tokens_only=False):  # grabs all translation files from the directory
    # for filename in glob.glob(os.path.join(env.lang_dir, '*.txt'))[:filelimit]:
    filename = os.path.join(os.path.join(os.getcwd(), env.lang_dir), fname)
    lang_tag = fname.split('\\')[-1][:env.lang_code_size]
    print(lang_tag)
    # print(f'{filename} vs {fname}')
    with smart_open.open(filename, encoding=env.f_enc) as f:
        for i, line in enumerate(f):
            if line.strip():
                tokens = gensim.utils.simple_preprocess(line)
                if tokens_only:
                    for token in tokens:
                        yield str(lang_tag + '_' + token)
                        # yield token
                else:
                    # For training data, add tags
                    # print(tokens, [i])
                    # print(([str(lang_tag + '_' + token) for token in tokens], [str(i), str(lang_tag)]))
                    # yield gensim.models.doc2vec.TaggedDocument(tokens,  [i, str(lang_tag)])
                    tags = [lang_tag, i,  line]
                    yield gensim.models.doc2vec.TaggedDocument(
                        # tokens, [line.strip()].append(word for word in tokens)
                        tokens, tags
                    )  # [str(lang_tag + '_' + token) for token in tokens], [str(i), str(lang_tag)])


def sentence_sim(txt_file, infer_val='And God said , Let there be light : and there was light .', filelimit=1,
                 linelimit=5):
    if os.path.exists(os.path.join(os.getcwd(), env.tmp_model)):
        print(f'Save File Found: {save_file}')
        model = Doc2Vec.load(save_file)
    else:
        raise FileNotFoundError("Model does not exist. Cannot check similarities")
    print(f'Inferring: {gensim.utils.simple_preprocess(infer_val)}')
    # vector = model.infer_vector(
    #     ["起初 ， 神创造天地。"]
    # )
    # vector = model.infer_vector(
    #     gensim.utils.simple_preprocess("Y dijo Dios: Sea la luz: y fue la luz.")
    # )

    vector = model.infer_vector(
        gensim.utils.simple_preprocess(infer_val)
    )
    print(f'{len(vector)} vs {len(model.dv)}')
    sims = model.dv.most_similar([vector])
    ents = [entity for entity in model.dv.index_to_key]
    print( f'Vector size: {len(ents)} \n {ents}' )
    print(f'Inferred Sim: {sims[:linelimit]}')
    # printed = 0
    # for line in sims:
    #     print(line)
    #     if line:
    #         printed += 1
    #     if printed >= linelimit:
    #         break

    # txt_file_path = os.path.join(os.path.join(os.getcwd(), env.lang_dir), txt_file)
    # with open(txt_file_path, 'r', encoding=env.f_enc) as file:
    #     lines = file.readlines()
    #     # Print sentences with similarity scores
    #     for index, similarity_score in sims:
    #         index = int(index)
    #         # Ensure index is within the range of lines
    #         # print(index, similarity_score)
    #         if 0 <= index < len(lines) and lines[index].strip():
    #             line = lines[index].strip()  # Remove trailing newline character
    #             print(f"Similarity Score: {round(similarity_score * 100, 2)} -> "
    #                   f"Line {index + 1}: {line}")
    #             printed += 1
    #         # else:
    #         #     print(f"Index {index} is out of range.")
    #         if printed > linelimit:
    #             break

    # print(model.docvecs['12345'])


### TODO: complete sentence similarity generator
def word_sim(word, linelimit=5):
    if os.path.exists(os.path.join(os.getcwd(), save_embeddings)):
        print(f'Save File Found: {save_embeddings}')
        model = Word2Vec.load(save_embeddings)
        model = Doc2Vec.load(save_file)
    else:
        raise FileNotFoundError("Model does not exist. Cannot check similarities")
    print(word)
    word = str(word).encode(encoding=env.f_enc)
    print(word)
    sim = model.wv.key_to_index
    # sim = model.wv.similar_by_word(word, topn=linelimit)
    print(sim)
    if model.wv.similar_by_word(word):
        print(model.wv.similar_by_word(word)[:linelimit])
    else:
        print("Word Does Not Exist")
        print(model.wv.key_to_index)

    return model


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
    tfidf_file = os.path.join(os.getcwd(), env.tmp_model)
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
    # tfidf.save(env.tmp_model)
    print(list(enumerate(sims))[:5])


def get_corpus(txt_directory, filelimit=1, linelimit=10):
    document = "In the beginning, God created the Heavens and the Earth"
    tokens = []

    # creates the directory if it doesn't exist
    if not os.path.exists(os.path.join(os.getcwd(), txt_directory)):
        os.makedirs(txt_directory)
        print(f'Directory Not Found: {txt_directory}')
        raise Exception(f"Directory Not Found: {txt_directory}")

    # grabs all translation files from the directory
    for filename in glob.glob(os.path.join(txt_directory, '*.txt'))[:filelimit]:
        with open(os.path.join(os.getcwd(), filename), mode='r', encoding=env.f_enc) as file:
            for line in file.readlines()[:linelimit]:
                tokens.append(line.strip())
    if not tokens:
        print(f'Empty Directory: {txt_directory}')
        raise Exception(f'Empty Directory: {txt_directory}')
    return tokens
