import os
import env_vars as env


def read_all_files(txt_dir, lang = ''):
    lines = []
    for root, dirs, files in os.walk(txt_dir):
        for filename in [file for file in files if file.endswith(f'.txt') and file.startswith(lang)]:
            print(filename)
            lines += [line.strip() for line in read_file_lines(os.path.join(root, filename))]
    return lines


def read_file_lines(filename):
    """
    Read the lines from a file and return them as a list.
    """
    with open(filename, 'r', encoding=env.f_enc) as file:
        lines = [line.strip() for line in file if len(line) > 0]
    return lines


def serialize_list(list, target_file):
    with open(target_file, 'w', encoding=env.f_enc) as f:
        for sentence in list:
            for word in sentence:
                f.write(word.strip())
                f.write(' ')
            f.write('\n')


def deserialize_list(target_file):
    if os.path.exists(target_file):
        unique_items = []
        with open(target_file, 'r', encoding=env.f_enc) as f:
            temp = f.readlines()
            for items in temp:
                sent = simple_preprocess(items)
                if len(sent) > 0:
                    unique_items.append(sent)
        return unique_items
    return []


def train_word2vec(train_corpus, update_vocab=False, vector_size=100, window=5, min_count=1, epochs=10, workers=4, ):
    save_embeddings = os.path.join(os.getcwd(), env.model_dir, env.word_embeddings)
    if os.path.exists(save_embeddings):
        ### TODO: put these types of debug messages into an actual logger
        print(f'Save File Found: {save_embeddings}')
        try:
            model = Word2Vec.load(save_embeddings)
            model.build_vocab(corpus_iterable=train_corpus, update=update_vocab)
        except IndexError as i:
            print(f"Error building vocab for model: {i}")
            return None
        except Exception as e:
            print(f"Error loading existing model: {e}")
            return None
    else:
        print('Creating save file location...')

        model = Word2Vec( vector_size=vector_size, window=window, min_count=min_count, epochs=epochs, workers=workers)
        model.build_vocab(corpus_iterable=train_corpus)

    train_file = os.path.join(os.getcwd(), env.model_dir, env.train_sents)

    unique_items = deserialize_list(train_file)

    for item in train_corpus:
        if item not in unique_items:
            unique_items.append(item)

    serialize_list(unique_items, train_file)

    print('Training Word2Vec Model...')
    model.train(corpus_iterable=train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    print('Training complete!')
    print('Saving Word2Vec file...')
    model.save(save_embeddings)
    print('Saving complete!')
    return model


def train_model_per_directory(txt_dir, epochs=10, update_vocab=False):
    for root, dirs, files in os.walk(txt_dir):
        if files:
            lang_code = files[0][:env.lang_code_size]
            model_file = lang_code + "_" + env.model_dir
            print(f'Training {model_file} model on files: {files}')
            # swp_model_name = env.word_embeddings
            swp_modl_dir = env.model_dir
            env.model_dir = os.path.join(env.model_dir, model_file)
            if not os.path.exists(env.model_dir):
                os.makedirs(env.model_dir)
            # env.word_embeddings = os.path.join(env.model_dir , env.word_embeddings.split("\\")[-1])
            print(f'{env.word_embeddings}')
            for filename in [file for file in files if file.endswith('.txt')]:
                lines = [simple_preprocess(text) for text in
                         [line.strip() for line in read_file_lines(os.path.join(root, filename))
                          if len(line.strip()) > 0]
                         ]
                if len(lines) > 0:
                    train_word2vec(train_corpus=lines, update_vocab=update_vocab, epochs=epochs)
            # env.word_embeddings = swp_model_name
            env.model_dir = swp_modl_dir



def get_trained_sents(lang = 'eng'):
    for root, dirs, files in os.walk(env.model_dir):
        for dirname in dirs:
            if dirname.startswith(lang):
                train_file = os.path.join(root, dirname, env.train_sents)
                ### TODO: put these types of debug messages into an actual logger
                # print(f'Looking for: {train_file}')
                if os.path.exists(train_file):
                    # print(f'Trained File Found: {train_file}')
                    return read_file_lines(train_file)
    return []


def use_lang_model(lang = 'eng'):
    for root, dirs, files in os.walk(env.model_dir):
        for dirname in dirs:
            if dirname.startswith(lang):
                save_embeddings = os.path.join(root, dirname, env.word_embeddings)
                ### TODO: put these types of debug messages into an actual logger
                # print(f'Looking for: {save_embeddings}')
                if os.path.exists(save_embeddings):

                    # print(f'Save File Found: {save_embeddings}')
                    return Word2Vec.load(save_embeddings)
    print(f'No Model Found at: {env.model_dir}')
    return None


def tokenize_sentences(list):
    ### TODO: Fix null list remover (ask chatgpt or something)
    # for list_with_none in list:
    #     list = [x for x in list_with_none if x is not None]

    # Tokenize and preprocess combined sentences
    tokenized_combined_sentences = [simple_preprocess(sentence) for sentence in list]
    return tokenized_combined_sentences


from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

### Builds the model's vocabulary given that new words exist in the input
# train_model_per_directory(env.lang_dir, update_vocab=True)
#
### grabs sentence similarities for gensim
def gensim_sentence_sim(input_sentence, chosen_lang, limit = 1):
    model = use_lang_model(chosen_lang)
    tokenized_combined_sentences = get_trained_sents(chosen_lang)

    if model is not None and len(tokenized_combined_sentences) > 0:
        print("Finding Similarities:")
        # Function to get sentence vector
        def get_sentence_vector(sentence):
            words = simple_preprocess(sentence)
            word_vectors = [model.wv[word] for word in words if word in model.wv]
            if word_vectors:
                return np.mean(word_vectors, axis=0)
            else:
                return np.zeros(model.vector_size)

        # Function to find most similar sentence
        def most_similar_sentence(input_sentence, sentences, limit=1):

            input_vector = get_sentence_vector(input_sentence)
            if input_vector is not None:
                most_similar_items = set()
                temp_sents = sentences
                sentence_vectors = [get_sentence_vector(sentence) for sentence in sentences]
                for i in range(limit):
                    if i > len(sentence_vectors):
                        break
                    similarities = [cosine_similarity([input_vector], [vec])[0][0] for vec in sentence_vectors]
                    most_similar_index = np.argmax(similarities)
                    print(f'Found match #{(i + 1)}: {(sentences[most_similar_index], similarities[most_similar_index])}')
                    most_similar_items.add(
                        (temp_sents.pop(most_similar_index), round(similarities.pop(most_similar_index), 3))
                    )
                    sentence_vectors.pop(most_similar_index)

                return most_similar_items
                # return [sentences[most_similar_index], similarities[most_similar_index]]
            else:
                return None

        # Example usage
        most_similar = most_similar_sentence(input_sentence=input_sentence, sentences=tokenized_combined_sentences, limit=limit)
        print("\nInput Sentence:", input_sentence)
        print("Most Similar Sentence:", *[f'\n{item}' for item in sorted(most_similar, key=lambda x: x[1], reverse = True)])

if __name__ == '__main__':
    ### Builds the model's vocabulary given that new words exist in the input
    train_model_per_directory(env.lang_dir, update_vocab=True)
    arb_lim = 5
    # gensim_sentence_sim(
    #     input_sentence="于是 ， 地上长出了青草和结种子的蔬菜 ， 各从其类 ； 又长出结果子的树木 ， 各从其类 ， 果子都包着核。 神看这是好的。",
    #     chosen_lang='cmn',
    #     limit=arb_lim
    # )

    gensim_sentence_sim(
        input_sentence="god made the heavens and earth",
        chosen_lang='eng',
        limit=arb_lim
    )
