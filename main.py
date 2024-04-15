from LanguageTokenizer.TxtToToken import text_tokenize

import os, json
import env_vars as env


###TODO: put the tokenizer functions in a class/module
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
        with open(language_file, mode='w', encoding=env.f_enc) as output:
            # dump the json dictionary
            json.dump(data, output)
    # elif format == 'other file format':
    #    do stuff

    language_file = os.path.join(token_directory, f'{lang_prefix}_mapping{readable}')
    with open(language_file, mode='w', encoding=env.f_enc) as output:
        # outputting text version of the dictionary
        for mapped in data:
            temp = (mapped.__str__()).replace("\u3000", " ").replace("\xa0", " ")
            output.write(f"{temp}\n")


## TODO: make db version of this
def get_all_tokened(txt_directory, token_directory, one_way=False, one_file=True, limit=None, offset=0,
                    filetype='.txt'):
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
            with open(os.path.join(root, filename), mode='r', encoding=env.f_enc) as file:
                # tokenizes the contents of each file
                if not one_way:
                    # print(filename.split('_')[0][:env.lang_code_size])
                    content = text_tokenize(
                        file,
                        filename.split('_')[0][:env.lang_code_size]
                    )
                else:
                    # print(filename[:env.lang_code_size])
                    content = text_tokenize(file, filename[:env.lang_code_size])
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
    limit_reached = False

    ### TODO: Create a proper limit-per-language algorithm/function
    # langs = set()
    # for lang in tokens:
    #     langs.add(lang[0].get(env.lang_key))
    # num_tokens = len(langs)

    ### TODO: Fix the 4-times repeated code
    if one_way and one_file:
        # maps each language to their respective translation in another language
        language_from = tokens[0]
        mapping = []
        fsize = 0
        for language_to in tokens:
            # checks of the target and source language are different
            if language_from[0].get(env.lang_key) == language_to[0].get(env.lang_key):
                num_tokens -= 1
            else:
                print(f'{language_from[0].get(env.lang_key)} -> {language_to[0].get(env.lang_key)}')
                per_language = limit / num_tokens if limit and limit / num_tokens > 0 else len(language_from) if len(
                    language_from) <= len(language_to) else len(language_to)
                # print(int(per_language))
                temp_off = offset
                # Maps source language to their translation
                for i in range(int(per_language)):
                    if i + temp_off < len(language_from) and i + temp_off < len(language_to):
                        line1 = language_from[i + temp_off]
                        line2 = language_to[i + temp_off]
                        lang1 = line1.get(env.lang_key)
                        lang2 = line2.get(env.lang_key)
                        value1 = line1.get(env.tl_key)
                        value2 = line2.get(env.tl_key)
                        if not value1 or not value2:
                            i -= 1
                            temp_off += 1
                            continue
                        if i + temp_off > len(language_from):
                            print(f'{i} + {temp_off} == {i + temp_off} > {len(language_from)}')
                            break
                        next_val = {
                            lang1: value1,
                            lang2: value2
                        }
                        mapping.append(
                            next_val
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
        serialize_tokens(
            token_directory,
            f'{language_from[0].get(env.lang_key)}_'
            f'{[lang for lang in [language[0].get(env.lang_key) for language in tokens]]}'
            , mapping
        )
    elif not one_way and one_file:
        # maps each language to their respective translation in another language
        mapping = []
        fsize = 0
        for language_from in tokens:
            print(language_from[0].get(env.lang_key))
            for language_to in tokens:
                # checks of the target and source language are different
                if language_from[0].get(env.lang_key) is not language_to[0].get(env.lang_key):
                    # Maps source language to their translation
                    per_language = limit / num_tokens if limit and limit / num_tokens > 0 \
                        else len(language_from) if len(language_from) <= len(language_to) \
                        else len(language_to)
                    print(int(per_language))
                    temp_off = offset
                    for i in range(int(per_language)):
                        if i + temp_off < len(language_from) and i + temp_off < len(language_to):
                            line1 = language_from[i + temp_off]
                            line2 = language_to[i + temp_off]
                            lang1 = line1.get(env.lang_key)
                            value1 = line1.get(env.tl_key)
                            lang2 = line2.get(env.lang_key)
                            value2 = line2.get(env.tl_key)
                            if not lang1 or not lang2:
                                continue
                            if i + temp_off > len(language_from):
                                print(f'{i} + {temp_off} == {i + temp_off} > {len(language_from)}')
                                break

                            if lang1 == lang2:
                                break
                            next_val = {
                                lang1: value1,
                                lang2: value2
                            }
                            mapping.append(
                                next_val
                            )
                            # next_val = {
                            #     lang2: value2,
                            #     lang1: value1
                            # }
                            # mapping.append(
                            #     next_val
                            # )
                            fsize += 2
                            if len(mapping) >= limit:
                                limit_reached = True
                                break
                    if limit_reached:
                        break
                if limit_reached:
                    break
        ### TODO: fix file name generation scheme
        print(f'File Size: {fsize}')
        serialize_tokens(
            token_directory,
            f'{"".join(str(lang+"_") for lang in set(language[0].get(env.lang_key) for language in tokens))}',
            mapping
        )
    elif one_way and not one_file:
            # maps each language to their respective translation in another language
            langs = set(lang[0].get(env.lang_key) for lang in tokens)
            num_tokens = len(langs)
            language_from = tokens[0]
            fsize = 0
            for language_to in tokens:
                mapping = []
                # checks of the target and source language are different
                if language_from[0].get(env.lang_key) == language_to[0].get(env.lang_key):
                    num_tokens -= 1
                else:
                    print(f'{language_from[0].get(env.lang_key)} -> {language_to[0].get(env.lang_key)}')
                    per_language = limit / num_tokens if limit and limit / num_tokens > 0 else len(
                        language_from) if len(
                        language_from) <= len(language_to) else len(language_to)
                    # print(int(per_language))
                    temp_off = offset
                    # Maps source language to their translation
                    for i in range(int(per_language)):
                        if i + temp_off < len(language_from) and i + temp_off < len(language_to):
                            line1 = language_from[i + temp_off]
                            line2 = language_to[i + temp_off]
                            lang1 = line1.get(env.lang_key)
                            lang2 = line2.get(env.lang_key)
                            value1 = line1.get(env.tl_key)
                            value2 = line2.get(env.tl_key)
                            if not value1 or not value2:
                                i -= 1
                                temp_off += 1
                                continue
                            if i + temp_off > len(language_from):
                                print(f'{i} + {temp_off} == {i + temp_off} > {len(language_from)}')
                                break
                            next_val = {
                                lang1: value1,
                                lang2: value2
                            }
                            mapping.append(
                                next_val
                            )
                            fsize += 2
                            if len(mapping) >= limit:
                                limit_reached = True
                                break
                            # print(f'{mapping[len(mapping) - 1]} from\n\t{lang1} : {value1}\n\t{lang2} : {value2}')
                        if limit_reached:
                            break
                print(f'File Size: {fsize}')
                serialize_tokens(
                    token_directory,
                    f'{language_from[0].get(env.lang_key)}_'
                    f'{"".join(lang for lang in set(language[0].get(env.lang_key) for language in tokens))}'
                    , mapping
                )
    elif not one_way and not one_file:
        # maps each language to their respective translation in another language
        finish_set = set()
        for language_from in tokens:
            mapping = []
            limit_reached = False
            fsize = 0
            for language_to in tokens:
                # checks of the target and source language are different
                if language_from[0].get(env.lang_key) != language_to[0].get(env.lang_key)\
                        and language_from[0].get(env.lang_key) and language_to[0].get(env.lang_key):
                    # Maps source language to their translation
                    per_language = limit / num_tokens if limit and limit / num_tokens > 0 else len(
                        language_from) if len(language_from) <= len(language_to) else len(language_to)
                    # print(int(per_language))
                    temp_off = offset
                    for i in range(int(per_language)):
                        if i + temp_off < len(language_from) and i + temp_off < len(language_to):
                            line1 = language_from[i + temp_off]
                            line2 = language_to[i + temp_off]
                            if line1.get(env.tl_key) == 'eng':
                                print(f'{i} vs {temp_off}')
                            if not line1.get(env.tl_key) or not line2.get(env.tl_key):
                                i -= 1
                                temp_off += 1
                                continue
                            if i + temp_off > len(language_from):
                                print(f'{i} + {temp_off} == {i + temp_off} > {len(language_from)}')
                                break
                            lang1 = line1.get(env.lang_key)
                            value1 = line1.get(env.tl_key)
                            lang2 = line2.get(env.lang_key)
                            value2 = line2.get(env.tl_key)
                            if lang1 == lang2:
                                break
                            next_val = {
                                lang1: value1,
                                lang2: value2
                            }
                            mapping.append(
                                next_val
                            )
                            fsize += 2
                            if len(mapping) >= limit:
                                limit_reached = True
                                break
                    if limit_reached:
                        break
                if limit_reached:
                    break
            finish_set.add(language_from[0].get(env.lang_key) + "_")
            print(finish_set)
            print(f'{language_from[0].get(env.lang_key) not in finish_set} {fsize} for {language_from[0].get(env.lang_key)} ')
            print(f'{language_from[0].get(env.lang_key)} vs {finish_set}')
            if language_from[0].get(env.lang_key) not in finish_set:
                serialize_tokens(
                    token_directory,
                    f'{language_from[0].get(env.lang_key)}_'
                    f'{"".join(str(lang+"_") for lang in set(language[0].get(env.lang_key) for language in tokens if language[0].get(env.lang_key) != language_from[0].get(env.lang_key)))}',
                    mapping
                )


### TODO: Run manual and Automatic testing for each function in main
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ## tokenizer stuff
    # get_all_tokened(txt_directory=env.lang_dir, token_directory=env.tokenized_dir, one_way=True, one_file=True,
    #                 limit=30000, offset=0)

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
    from Gensim.gensim_functs import sentence_sim, word_sim
    try:
        sentence_sim(f'eng\\eng-x-bible-kingjames-v1.txt')
        word_sim("said")
    except FileNotFoundError as f:
        sentence_sim('eng-x-bible-kingjames-v1.txt')
        word_sim("said")

    # model_training_sentence_sim(lang_dir)
