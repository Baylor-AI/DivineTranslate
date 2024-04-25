import random
import env_vars as env

from Gensim.gensim_functs import sentence_sim, model_training_sentence_sim
from LanguageTokenizer.TxtToToken import text_tokenize

import os, glob, json

###TODO: put the tokenizer functions in a class/module
# This is the directory where all the txt files should go for tokenization.
lang_dir = env.lang_dir
tokenized_dir = env.tokenized_dir
lang_code_size = env.lang_code_size
ENCODING = env.f_enc
bible_size = 43905  # number of lines of text in the bible
ARBITRARY_CHUNK_SIZE = 270000  # change this so that it makes sense later


### TODO: make compatible with other file formats?
def serialize_tokens(filename, token_directory, data, train_format='.json', readable='.txt'):
    """
    serializes the tokens in the specified format and also in a human readable format

    :param filename:
    :param token_directory:
    :param data:
    :param train_format:
    :param readable:
    :return:
    """
    # print(token_directory)
    if not os.path.exists(token_directory):
        os.makedirs(token_directory)

    language_file = os.path.join(token_directory, f'{filename}_mapping{train_format}')
    if 'json' in train_format:
        with open(language_file, mode='w', encoding=ENCODING) as output:
            # dump the json dictionary
            json.dump(data, output)
    # elif format == 'other file format':
    #    do stuff

    language_file = os.path.join(token_directory, f'{filename}_mapping{readable}')
    with open(language_file, mode='w', encoding=ENCODING) as output:
        # outputting text version of the dictionary
        for mapped in data:
            temp = (mapped.__str__())
            output.write(f"{temp}\n")


## TODO: make db version of this
def get_all_tokened(txt_directory, token_directory, file_name='', one_way=False, limit=None, offset=0, filetype='.txt'):
    """
    gets all translation files from the specified txt_directory and puts them into their tokenized format in the
    token_directory. It tokenizes languages in the format:

    { 'lang1':'text1', 'lang2':'text2'}

    where lang 1 is the iso-639-2 language code for text1, and text1 is the text being labeled.
        lang2 is the iso-639-2 language code for text2, and text2 is the corresponding lang2 translation of text1.

    :param txt_directory: the directory of the text files, where each file is named with their 3 letter iso-639-2
        language code prepended to the file
    :param token_directory: the directory that the tokenized files will be stored at
    :param file_name:
    :param one_way: denotes whether each translation should only go in one direction
    :param limit: limit on file size
    :param offset: how many lines deep into the file to start parsing from
    :param filetype:
    :return:
    """

    tokens = []

    # creates the directory if it doesn't exist
    if not os.path.exists(os.path.join(os.getcwd(), txt_directory)):
        os.makedirs(txt_directory)
        print(f'Directory Not Found: {txt_directory}')
        raise Exception(f"Directory Not Found: {txt_directory}")

    # grabs all translation files from the directory
    cur_dir = os.path.join(os.getcwd(), txt_directory)
    for root, dirs, files in os.walk(cur_dir):
        for filename in [file for file in files if file.endswith(f'{filetype}')]:
            with open(os.path.join(root, filename), mode='r', encoding=ENCODING) as file:
                # tokenizes the contents of each file
                if not one_way:
                    # print(filename.split('_')[0][:lang_code_size])
                    content = text_tokenize(
                        file,
                        filename.split('_')[0][:lang_code_size]
                    )
                else:
                    # print(filename[:lang_code_size])
                    content = text_tokenize(file, filename[:lang_code_size])
                tokens.append(content)

    if not tokens:
        print(f'Empty Directory: {txt_directory}')
        raise Exception(f'Empty Directory: {txt_directory}')

    # checks the number of files tokenized
    num_tokens = len(tokens)
    # Error if not enough files
    if len(tokens) < 2:
        print(f'Not enough files in directory: must have at least 2 different translations!')
        raise Exception(f'Not enough files in directory: must have at least 2 different translations!')

    print(f"Tokenizing: {num_tokens} files...")
    lang_key = 'lang'
    tl_key = 'tl'

    ### TODO: Create a proper limit-per-language algorithm/function
    langs = set()
    for lang in tokens:
        langs.add(lang[0].get(lang_key))
    num_langs = len(langs)

    if not one_way:
        # maps each language to their respective translation in another language
        fsize = 0
        final_offsets = []
        mapping = []
        for language_from in tokens:
            for language_to in tokens:
                # checks of the target and source language are different
                if language_from[0].get(lang_key) == language_to[0].get(lang_key):
                    # num_tokens -= 1
                    continue
                else:
                    per_language = limit / num_tokens if limit and limit / num_tokens > 0 else len(
                        language_from) if len(
                        language_from) <= len(language_to) else len(language_to)
                    temp_off = offset
                    print(f'{per_language} Lines {language_from[0].get(lang_key)} -> {language_to[0].get(lang_key)}')
                    # Maps source language to their translation
                    for i in range(int(per_language)):
                        limit_reached = False
                        if i + temp_off < len(language_from) and i + temp_off < len(language_to):
                            line1 = language_from[i + temp_off]
                            line2 = language_to[i + temp_off]
                            lang1 = line1.get(lang_key)
                            lang2 = line2.get(lang_key)
                            value1 = line1.get(tl_key)
                            value2 = line2.get(tl_key)
                            if not value1 or not value2:
                                i -= 1
                                temp_off += 1
                                continue
                            if i + temp_off > len(language_from):
                                print(f'{i} + {temp_off} == {i + temp_off} > {len(language_from)}')
                                break
                            dict_next = {
                                lang1: value1,
                                lang2: value2
                            }
                            mapping.append(
                                dict_next
                            )
                            dict_next = {
                                lang2: value2,
                                lang1: value1
                            }
                            mapping.append(
                                dict_next
                            )
                            fsize += 2
                            if len(mapping) >= limit:
                                limit_reached = True
                                break
                            # print(f'{mapping[len(mapping) - 1]} from\n\t{lang1} : {value1}\n\t{lang2} : {value2}')
                        if limit_reached:
                            break
                    final_offsets.append(temp_off + per_language)

            print(f'File Lines: {fsize}')
            print(f'Final Offset: {final_offsets}')
            # print(file_name)
        ### TODO: fix file name generation scheme
        serialize_tokens(tokens[0][0].get(tl_key) if not file_name else file_name, token_directory, mapping)
        return int(min(final_offsets))
    else:
        # maps each language to their respective translation in another language
        per_file = limit / num_langs
        MIN_LINES = limit
        fsize = 0
        for language_from in tokens:
            mapping = []
            per_pair = per_file / (num_langs - 1)
            num_check = len([x[0] for x in tokens if x[0].get(lang_key) != language_from[0].get(lang_key)])
            # print(sum([len(x) for x in tokens if x[0].get(lang_key) != language_from[0].get(lang_key)]) / num_check)
            print(f'{num_check} of {per_pair} of {per_file}')
            for language_to in tokens:
                limit_reached = False
                per_trans = per_pair/num_langs if 0 <= per_pair/num_langs <= len(language_from) \
                    else len(language_from) if len(language_from) <= len(language_to) \
                    else len(language_to)
                # checks of the target and source language are different
                if language_from[0].get(lang_key) is not language_to[0].get(lang_key) and per_trans > 0:
                    if per_trans < MIN_LINES:
                        MIN_LINES = per_trans
                    # Maps source language to their translation
                    # print(f'{per_trans} for {language_from[0].get(lang_key)} -> {language_to[0].get(lang_key)}')
                    temp_off = offset
                    for i in range(int(per_trans)):
                        if i + temp_off < len(language_from) and i + temp_off < len(language_to) and per_trans:
                            while i + temp_off < len(language_from) and i + temp_off < len(language_to)\
                                    and (not language_from[i + temp_off].get(tl_key) or
                                         not language_to[i + temp_off].get(tl_key)):
                                temp_off += 1
                            if i + temp_off >= len(language_from) or \
                                    language_from[i + temp_off].get(lang_key) == language_to[i + temp_off].get(lang_key) :
                                # print(f'{i} + {temp_off} == {i + temp_off} > {len(language_from)}')
                                break
                            line1 = language_from[i + temp_off]
                            line2 = language_to[i + temp_off]
                            lang1 = line1.get(lang_key)
                            value1 = line1.get(tl_key)
                            lang2 = line2.get(lang_key)
                            value2 = line2.get(tl_key)

                            next_val = {
                                lang1: value1,
                                lang2: value2
                            }
                            mapping.append(
                                next_val
                            )
                            per_trans -= 1
                            fsize += 1
                            if len(mapping) >= per_file:
                                limit_reached = True
                                break
                    if limit_reached:
                        break
                if limit_reached:
                    break
            # print(per_trans)
            ### TODO: fix file name generation scheme
            serialize_tokens(language_from[0].get(lang_key), token_directory, mapping)
        print(fsize)
        return MIN_LINES



## TODO: RE-CODE THIS FUNCTION. or Optimize to allow for tokenizing of 1600+ languages
def tokenize_selected(
        files_to_tokenize, txt_directory=lang_dir, token_directory=tokenized_dir, file_name='',
        limit=None, offset=0, filetype='.txt'):
    tokens = []

    # creates the directory if it doesn't exist
    if not os.path.exists(os.path.join(os.getcwd(), txt_directory)):
        os.makedirs(txt_directory)
        print(f'Directory Not Found: {txt_directory}')
        raise Exception(f"Directory Not Found: {txt_directory}")

    # grabs all translation files from the directory
    cur_dir = os.getcwd()
    for root, dirs, files in os.walk(cur_dir):
        for filename in [file for file in files if file.endswith(f'{filetype}')]:
            if filename in files_to_tokenize:
                with open(os.path.join(root, filename), mode='r', encoding=ENCODING) as file:
                    # tokenizes the contents of each file
                    # print(filename[:lang_code_size])
                    content = text_tokenize(file, filename[:lang_code_size])
                    tokens.append(content)

    if not tokens:
        print(f'Empty Directory: {txt_directory}')
        raise Exception(f'Empty Directory: {txt_directory}')

    # checks the number of files tokenized
    num_tokens = len(tokens)
    # Error if not enough files
    if len(tokens) < 2:
        print(f'Not enough files in directory: must have at least 2 different translations!')
        raise Exception(f'Not enough files in directory: must have at least 2 different translations!')

    print(f"Tokenizing: {num_tokens} files...")
    lang_key = 'lang'
    tl_key = 'tl'

    ### TODO: Create a proper limit-per-language algorithm/function
    langs = set()
    for lang in tokens:
        langs.add(lang[0].get(lang_key))
    num_langs = len(langs)

    # maps each language to their respective translation in another language
    per_file = limit / num_langs
    MIN_LINES = limit
    fsize = 0
    for language_from in tokens:
        mapping = []
        per_pair = per_file / (num_langs - 1)
        num_check = len([x[0] for x in tokens if x[0].get(lang_key) != language_from[0].get(lang_key)])
        # print(sum([len(x) for x in tokens if x[0].get(lang_key) != language_from[0].get(lang_key)]) / num_check)
        print(f'{num_check} of {per_pair} of {per_file}')
        for language_to in tokens:
            limit_reached = False
            per_trans = per_pair / num_langs if 0 <= per_pair / num_langs <= len(language_from) \
                else len(language_from) if len(language_from) <= len(language_to) \
                else len(language_to)
            # checks of the target and source language are different
            if language_from[0].get(lang_key) is not language_to[0].get(lang_key) and per_trans > 0:
                if per_trans < MIN_LINES:
                    MIN_LINES = per_trans
                # Maps source language to their translation
                # print(f'{per_trans} for {language_from[0].get(lang_key)} -> {language_to[0].get(lang_key)}')
                temp_off = offset
                for i in range(int(per_trans)):
                    if i + temp_off < len(language_from) and i + temp_off < len(language_to) and per_trans:
                        while i + temp_off < len(language_from) and i + temp_off < len(language_to) \
                                and (not language_from[i + temp_off].get(tl_key) or
                                     not language_to[i + temp_off].get(tl_key)):
                            temp_off += 1
                        if i + temp_off >= len(language_from) or \
                                language_from[i + temp_off].get(lang_key) == language_to[i + temp_off].get(lang_key):
                            # print(f'{i} + {temp_off} == {i + temp_off} > {len(language_from)}')
                            break
                        line1 = language_from[i + temp_off]
                        line2 = language_to[i + temp_off]
                        lang1 = line1.get(lang_key)
                        value1 = line1.get(tl_key)
                        lang2 = line2.get(lang_key)
                        value2 = line2.get(tl_key)

                        next_val = {
                            lang1: value1,
                            lang2: value2
                        }
                        mapping.append(
                            next_val
                        )
                        per_trans -= 1
                        fsize += 1
                        if len(mapping) >= per_file:
                            limit_reached = True
                            break
                if limit_reached:
                    break
            if limit_reached:
                break
        # print(per_trans)
        ### TODO: fix file name generation scheme
        serialize_tokens(language_from[0].get(lang_key), token_directory, mapping)
    print(fsize)
    return MIN_LINES


def tokenize_unique_languages(txt_dir=lang_dir, token_dir=tokenized_dir, one_way=True, limit=3000, offset=0):
    seen = set()
    to_tokenize = []
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), lang_dir)):
        for filename in [file for file in files if file[:lang_code_size] not in seen]:
            seen.add(filename[:lang_code_size])
            to_tokenize.append(filename)

    tokenize_selected(to_tokenize)


def parallelized_tokenizing(txt_directory, token_directory, one_way=False, limit=2700000, offset=0):
    num_tries = int(limit / ARBITRARY_CHUNK_SIZE) + 1
    ### TODO: parellelize task splitting function
    # import multiprocessing
    # pool = multiprocessing.Pool(processes=num_tries)
    # args = [(txt_directory, os.path.join(token_directory, f"part-{i}"), one_way,limit,offset) for i in range(num_tries)]
    temp_off = offset
    for i in range(num_tries):
        print(os.path.join(token_directory, f"part-{i}"))
        temp_off = get_all_tokened(
            file_name=f"part-{i}",
            txt_directory=txt_directory,
            token_directory=token_directory,
            one_way=one_way,
            limit=ARBITRARY_CHUNK_SIZE,
            offset=temp_off
        ) + 1


def tokenized_file_splitter(input_file, token_dir):
    line_count = 0
    file_count = 1
    with open(os.path.join(token_dir, input_file), 'r', encoding=ENCODING) as f_in:
        for line in f_in:
            if line_count % ARBITRARY_CHUNK_SIZE == 0:
                # if file_count > 1:
                #     break
                # names output file assuming that the input file has an extension
                output_file = os.path.join(token_dir,
                                           f'{input_file}_split_{file_count}{os.path.splitext(input_file)[1]}')
                with open(output_file, 'w', encoding=ENCODING) as f_out:
                    f_out.write(line)
                file_count += 1
            else:
                with open(output_file, 'a', encoding=ENCODING) as f_out:
                    f_out.write(line)
            line_count += 1

def file_checker(input_file):
    with open(os.path.join(tokenized_dir, input_file), 'r', encoding=ENCODING) as f_in:
        contents = f_in.readlines()
        for i in range(10):
            print(random.choice(contents))

### TODO: Run manual and Automatic testing for each function in main
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ### tokenizer stuff
    # print(get_all_tokened(txt_directory=lang_dir, token_directory=tokenized_dir, one_way=True, limit=3000000, offset=0))
    tokenize_unique_languages()
    # separate_tokenizing(txt_directory=lang_dir, token_directory=tokenized_dir, one_way=False, limit=2700000, offset=0)
    # tokenized_file_splitter('cmn_mapping.txt', tokenized_dir)
    # tokenized_file_splitter('cmn_mapping.json', tokenized_dir)
    print("------------------------")
    file_checker("cmn_mapping.txt")
    print("------------------------")
    file_checker("spa_mapping.txt")
    print("------------------------")
    file_checker("eng_mapping.txt")
