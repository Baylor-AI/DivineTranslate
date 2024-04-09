from Gensim.gensim_functs import sentence_sim, model_training_sentence_sim
from LanguageTokenizer.TxtToToken import text_tokenize

import os, glob, json

###TODO: put the tokenizer functions in a class/module
# This is the directory where all the txt files should go for tokenization.
lang_dir = 'DBTextFiles'
tokenized_dir = 'TokenizedDB'
lang_code_size = 3
bible_size = 43905  # number of lines of text in the bible

### TODO: make compatible with other file formats?
def serialize_tokens(token_directory, lang_prefix, data, train_format='.json', readable='.txt'):
    """
    serializes the tokens in the specified format and also in a human readable format

    :param token_directory:
    :param lang_prefix:
    :param data:
    :param train_format:
    :param readable:
    :return:
    """
    print(token_directory)
    if not os.path.exists(token_directory):
        os.makedirs(token_directory)

    language_file = os.path.join(token_directory, f'{lang_prefix}_mapping{train_format}')
    if 'json' in train_format:
        with open(language_file, mode='w', encoding='utf-8') as output:
            # dump the json dictionary
            json.dump(data, output)
    # elif format == 'other file format':
    #    do stuff

    language_file = os.path.join(token_directory, f'{lang_prefix}_mapping{readable}')
    with open(language_file, mode='w', encoding='utf-8') as output:
        # outputting text version of the dictionary
        for mapped in data:
            temp = (mapped.__str__()).replace("\u3000", " ").replace("\xa0", " ")
            output.write(f"{temp}\n")


def train_all_files(filetype='.txt'):
    tokens = []
    # grabs all translation files from the directory
    cur_dir = os.path.join(os.getcwd(), lang_dir)
    for root, dirs, files in os.walk(cur_dir):
        for filename in [file for file in files if file.endswith(f'{filetype}')]:
            if train_doc2vec(os.path.join(root, filename)) is None:
                exit(1)


## TODO: make db version of this
def get_all_tokened(txt_directory, token_directory, one_way=False, limit=None, offset=0, filetype='.txt'):
    """
    gets all translation files from the specified txt_directory and puts them into their tokenized format in the
    token_directory. It tokenizes languages in the format:

    { 'lang1':'text1', 'lang2':'text2'}

    where lang 1 is the iso-639-2 language code for text1, and text1 is the text being labeled.
        lang2 is the iso-639-2 language code for text2, and text2 is the corresponding lang2 translation of text1.

    :param txt_directory: the directory of the text files, where each file is named with their 3 letter iso-639-2
        language code prepended to the file
    :param token_directory: the directory that the tokenized files will be stored at
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
            with open(os.path.join(root, filename), mode='r', encoding='utf-8') as file:
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
    limit_reached = False

    ### TODO: Create a proper limit-per-language algorithm/function
    # langs = set()
    # for lang in tokens:
    #     langs.add(lang[0].get(lang_key))
    # num_tokens = len(langs)

    if not one_way:
        # maps each language to their respective translation in another language
        language_from = tokens[0]
        mapping = []
        fsize = 0
        for language_to in tokens:
            # checks of the target and source language are different
            if language_from[0].get(lang_key) == language_to[0].get(lang_key):
                num_tokens-=1
            else:
                print(f'{language_from[0].get(lang_key)} -> {language_to[0].get(lang_key)}')
                per_language = limit / num_tokens if limit and limit / num_tokens > 0 else len(language_from) if len(
                    language_from) <= len(language_to) else len(language_to)
                print(int(per_language))
                temp_off = offset
                # Maps source language to their translation
                for i in range(int(per_language)):
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
        ### TODO: fix file name generation scheme
        print(f'File Size: {fsize}')
        serialize_tokens(token_directory, language_from[0].get(lang_key), mapping)

    else:
        # maps each language to their respective translation in another language
        for language_from in tokens:
            mapping = []
            for language_to in tokens:
                # checks of the target and source language are different
                if language_from[0].get(lang_key) is not language_to[0].get(lang_key):
                    # Maps source language to their translation
                    per_language = limit / num_tokens if limit and limit / num_tokens > 0 else len(
                        language_from) if len(language_from) <= len(language_to) else len(language_to)
                    print(int(per_language))
                    temp_off = offset
                    for i in range(int(per_language)):
                        if i + temp_off < len(language_from) and i + temp_off < len(language_to):
                            line1 = language_from[i + temp_off]
                            line2 = language_to[i + temp_off]
                            if not line1.get(tl_key) or not line2.get(tl_key):
                                continue
                            if i + temp_off > len(language_from):
                                print(f'{i} + {temp_off} == {i + temp_off} > {len(language_from)}')
                                break
                            lang1 = line1.get(lang_key)
                            value1 = line1.get(tl_key)
                            lang2 = line2.get(lang_key)
                            value2 = line2.get(tl_key)
                            if lang1 == lang2:
                                break
                            next_val = {
                                lang1: value1,
                                lang2: value2
                            }
                            mapping.append(
                                next_val
                            )
                            if len(mapping) >= limit:
                                limit_reached = True
                                break
                    if limit_reached:
                        break
                if limit_reached:
                    break

            ### TODO: fix file name generation scheme
            serialize_tokens(language_from[0].get(lang_key), token_directory, mapping)


### TODO: Run manual and Automatic testing for each function in main
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ### tokenizer stuff
    # get_all_tokened(txt_directory=lang_dir, token_directory=tokenized_dir, one_way=False, limit=300000, offset=0)

    # print(match_lemma_list('prueba', 'test', 'spa', 'eng'))

    # ### fun lil cli for wordnet stuff
    # ### SynSetter Stuff
    # from Wordnet.wordnet_functs import synset_program, synset_choose, synset_compare, synset_sentence_match, \
    #     possible_languages, match_lemma_list, match_lemma
    # print(f"wordnet possible languages: {possible_languages()}")
    # synset_program()
    # print(f"wordnet possible languages: {possible_languages()}")
    # type = 1;
    # while type == 1 or type == 2:
    #     while True:
    #         type = input("what would you like to compare?\n\t1.words\n\t2.sentences\n\t0.exit")
    #         if type and int(type) in [0,1,2]:
    #             type = int(type)
    #             break;
    #
    #     if type == 1:
    #         choice = str(input("What Word would you like the synonyms and antonyms for?"))
    #         synset_choose(choice)
    #         compare=input("What word would you like to commpare your word/sentence with?")
    #         if compare == "stop":
    #             break
    #         synset_compare(choice.strip(), compare.strip())
    #
    #     elif type == 2:
    #         choice = str(input("What is the first sentence you would like to compare?"))
    #         lang1 = str(input("What is that sentence's language?"))
    #         compare=str(input("What is the second sentence you would like to compare?"))
    #         lang2 = str(input("What is that sentence's language?"))
    #         synset_sentence_match(choice.strip(), compare.strip(),
    #                               lang1.strip(), lang2.strip())

    # ### Gensim
    from Gensim.gensim_functs import sentence_sim, train_doc2vec, word_sim
    try:
        sentence_sim('eng-x-bible-kingjames-v1.txt')
        word_sim("And")
    except FileNotFoundError as f:
        print(f)
        train_all_files()
        sentence_sim('eng-x-bible-kingjames-v1.txt')

    # model_training_sentence_sim(lang_dir)

