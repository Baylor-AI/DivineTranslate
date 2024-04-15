import os
import env_vars as env
from Gensim.gensim_functs import train_word2vec


def training_word2vec(filetype='.txt'):
    cur_dir = os.path.join(os.getcwd(), '../' + env.lang_dir)
    for root, dirs, files in os.walk(cur_dir):
        for filename in [file for file in files if file.endswith(f'{filetype}')]:
            print(f'{filename} -> {os.path.join(root, filename)}')
            try:
                if train_word2vec(os.path.join(root, filename), 300, 10, 100) is None:
                    exit(1)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    training_word2vec()
