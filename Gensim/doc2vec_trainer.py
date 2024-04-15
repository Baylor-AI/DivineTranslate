import os

import gensim.utils

import env_vars as env
from Gensim.gensim_functs import train_doc2vec


def training_doc2vec(filetype='.txt'):
    print(gensim.utils.simple_preprocess('And God said , Let there be light : and there was light .'))
    cur_dir = os.path.join(os.getcwd(), '../' + env.lang_dir)
    print(cur_dir)
    for root, dirs, files in os.walk(cur_dir):
        print(files)
        for filename in [file for file in files if file.endswith(f'{filetype}')]:
            # try:
                if train_doc2vec(os.path.join(root, filename), 300, 10, 58) is None:
                    exit(1)
            # except Exception as e:
            #     print(e)


if __name__ == '__main__':
    training_doc2vec()
