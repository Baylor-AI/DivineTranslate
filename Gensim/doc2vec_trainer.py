import os
import env_vars as env
from Gensim.gensim_functs import train_doc2vec

def training_doc2vec(filetype='.txt'):
    cur_dir = os.path.join(os.getcwd(), '../' + env.lang_dir)
    print(cur_dir)
    for root, dirs, files in os.walk(cur_dir):
        for filename in [file for file in files if file.endswith(f'{filetype}')]:
            if train_doc2vec(os.path.join(root, filename)) is None:
                exit(1)

if __name__ == '__main__':
    training_doc2vec()