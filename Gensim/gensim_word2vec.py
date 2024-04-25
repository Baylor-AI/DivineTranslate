import os
import env_vars as env


def read_all_files(txt_dir):
    lines = []
    for root, dirs, files in os.walk(txt_dir):
        print(files)
        for filename in [file for file in files if file.endswith(f'.txt')]:
            lines += [line.strip() for line in read_file_lines(os.path.join(root, filename))]
    return lines


def read_file_lines(filename):
    """
    Read the lines from a file and return them as a list.
    """
    with open(filename, 'r', encoding=env.f_enc) as file:
        lines = [line.strip() for line in file if line]
    return lines


def train_word2vec(train_corpus, update_vocab=False, vector_size=100, window=5, min_count=1, epochs=1, workers=4, ):
    save_embeddings = os.path.join(os.getcwd(), env.word_embeddings)
    if os.path.exists(save_embeddings):
        print(f'Save File Found: {save_embeddings}')
        try:
            model = Word2Vec.load(save_embeddings)
            model.build_vocab(train_corpus, update=update_vocab)
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
        model = Word2Vec(vector_size=vector_size, window=window, min_count=min_count, epochs=epochs, workers=workers)
        model.build_vocab(train_corpus)

    print('Training Word2Vec Model...')
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    print('Training complete!')
    print('Saving Word2Vec file...')
    model.save(save_embeddings)
    print('Saving complete!')
    return model


def train_model_per_directory(txt_dir, update_vocab=False):
    for root, dirs, files in os.walk(txt_dir):
        lang_code = files[0][:env.lang_code_size]
        model_file = lang_code + "_" + env.word_embeddings
        print(f'Training {model_file} model on files: {files}')
        swp_model_name = env.word_embeddings
        env.word_embeddings = model_file
        for filename in [file for file in files if file.endswith('.txt')]:
            lines = [line.strip() for line in read_file_lines(os.path.join(root, filename))]
            train_word2vec(train_corpus=lines, update_vocab=update_vocab)
        env.word_embeddings = swp_model_name


def use_lang_model(lang = 'eng'):
    print('TODO: Fill me out')


from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# english_sentences = read_file_lines(f'../{env.lang_dir}/eng-x-bible-kingjames-v1.txt')
# french_sentences = read_file_lines(f'../{env.lang_dir}/fra-x-bible-kingjames-v1.txt')
# spa_sentences = read_file_lines(f'../{env.lang_dir}/spa_SPNR02.api.txt')
# cmn_sentences = read_file_lines(f'../{env.lang_dir}/cmn-x-bible-sf_ncv-zefania-v1.txt')


# Combine English and French sentences
# combined_sentences = english_sentences + french_sentences+ spa_sentences+ cmn_sentences + read_all_files("../" + env.lang_dir)
combined_sentences = read_all_files(env.lang_dir)
for list_with_none in combined_sentences:
    filtered_list = [x for x in list_with_none if x is not None]

# Tokenize and preprocess combined sentences
tokenized_combined_sentences = [simple_preprocess(sentence) for sentence in combined_sentences]

# Train Word2Vec model
# model = Word2Vec(tokenized_combined_sentences, vector_size=100, window=5, min_count=1, workers=4)
model = train_word2vec(
    tokenized_combined_sentences,
    update_vocab=False,
    vector_size=100,
    window=5,
    min_count=1,
    workers=4
)

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
        most_similar_items = []
        temp_sents = sentences
        sentence_vectors = [get_sentence_vector(sentence) for sentence in sentences]
        for i in range(limit):
            if i > len(sentence_vectors):
                break
            similarities = [cosine_similarity([input_vector], [vec])[0][0] for vec in sentence_vectors]
            most_similar_index = np.argmax(similarities)
            print(f'{most_similar_index} vs {int(most_similar_index)}')
            most_similar_items.append(
                (temp_sents.pop(most_similar_index), round(similarities.pop(most_similar_index), 2))
            )
            sentence_vectors.pop(most_similar_index)

        return most_similar_items  # [sentences[most_similar_index], similarities[most_similar_index]]
    else:
        return None


# Example usage
input_sentence = "于是 ， 地上长出了青草和结种子的蔬菜 ， 各从其类 ； 又长出结果子的树木 ， 各从其类 ， 果子都包着核。 神看这是好的。"
most_similar = most_similar_sentence(input_sentence, combined_sentences, limit=5)
print("Input Sentence:", input_sentence)
print("Most Similar Sentence:", most_similar)
