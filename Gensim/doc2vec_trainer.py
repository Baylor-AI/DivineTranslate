import os

import gensim.utils

import env_vars as env
from Gensim.gensim_functs import train_doc2vec


def training_doc2vec(filetype='.txt'):
    cur_dir = os.path.join(os.getcwd(), '../' + env.lang_dir)
    print(cur_dir)
    train_order = []
    for root, dirs, files in os.walk(cur_dir):
        print(f'{root} -- {dirs} -- {files}')
        # if dirs:
        #     for dir in dirs:
        #         for root1, dirs1, files1 in os.walk(os.path.join(cur_dir, dir)):
        #             for file in files1:
        #                 if file.endswith(f'{filetype}') and file not in train_order:
        #                     train_order.append(file)
        #                     print(file)
        #                     break
        #             print(train_order[-1])
        #             if train_doc2vec(os.path.join(root1, train_order[-1]), 300, 1, 100) is None:
        #                 exit(1)
        for filename in [file for file in files if file.endswith(f'{filetype}')]:
            try:
                if train_doc2vec(os.path.join(root, filename), 300, 1, 100) is None:
                    exit(1)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    training_doc2vec()
