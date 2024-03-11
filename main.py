from LanguageTokenizer.TxtToToken import text_tokenize
import os, glob, json, unicodedata
# This is the directory where all the txt files should go for tokenization.
lang_dir = 'DBTextFiles'
tokenized_dir = 'TokenizedDB'

## TODO: make db version of this
def get_all_tokened(txt_directory, token_directory, limit=None, offset=0):
    '''
    gets all translation files from the specified txt_directory and puts them into their tokenized format in the
    token_directory
    :param txt_directory:
    :param token_directory:
    :param limit:
    :param offset:
    :return:
    '''
    tokens = []
    txt_directory_size = len(lang_dir) + 1
    # creates the directory if it doesn't exist
    if not os.path.exists(os.path.join(os.getcwd(), txt_directory)):
        os.makedirs(txt_directory)
        print(f'Directory Not Found: {txt_directory}')
        raise Exception(f"Directory Not Found: {txt_directory}");

    # grabs all translation files from the directory
    for filename in glob.glob(os.path.join(txt_directory, '*.txt')):
        with open(os.path.join(os.getcwd(), filename), mode='r', encoding='utf-8') as file:
            print(filename.split('_')[0][txt_directory_size:])
            content = text_tokenize(file, filename.split('_')[0][txt_directory_size:])
            tokens.append(content)
    if not tokens:
        print(f'Empty Directory: {txt_directory}')
        raise Exception(f'Empty Directory: {txt_directory}')

    # checks the number of files to tokenize
    num_tokens = len(tokens)
    if num_tokens < 2:  # Error if not enough files
        print(f'Not enough files in directory: must have at least 2 different translations!')
        raise Exception(f'Not enough files in directory: must have at least 2 different translations!')

    lang_key = 'lang'
    tl_key = 'tl'
    # maps each language to their respective translation in another language
    for language_from in tokens:
        mapping = []
        for language_to in tokens:
            # TODO: determine if english1 to english2 translations should be in the same file?
            # TODO: discriminate between different versions of the bible
            # checks of the target and source language are different
            if language_to is not language_from:
                print(f'{language_from[0].get(lang_key)} -> {language_to[0].get(lang_key)}')
                # TODO: Assume all files are same length
                # Maps source language to their translation
                per_language = limit / len(tokens) if limit and limit / len(tokens) > 0 else len(language_from)
                print(int(per_language))
                for i in range(int(per_language)):
                    line1 = language_from[i+offset]
                    line2 = language_to[i+offset]
                    if not line1.get(tl_key) or not line2.get(tl_key):
                        i -= 1
                        offset += 1
                        continue
                    if i + offset > len(language_from):
                        print(f'{i} + {offset} == {i + offset} > {len(language_from)}')
                        break
                    mapping.append(
                        {
                            line1.get(lang_key): line1.get(tl_key),
                            line2.get(lang_key): line2.get(tl_key)
                        }
                    )
        if not os.path.exists(txt_directory):
            os.makedirs(txt_directory)
        # TODO: discriminate between different versions of the bible as well
        language_file = os.path.join(token_directory, f'{language_from[0].get(lang_key)}_mapping.json')
        with open(language_file, mode='w', encoding='utf-8') as output:
            # dump the json dictionary
            json.dump(mapping, output)
        language_file = os.path.join(token_directory, f'{language_from[0].get(lang_key)}_mapping.txt')
        with open(language_file, mode='w', encoding='utf-8') as output:

            # outputting text version of the dictionary
            for mapped in mapping:
                # print(mapped.__str__())
                temp = (mapped.__str__()).replace("\u3000", " ").replace("\xa0", " ")
                output.write(f"{temp}\n")


from Wordnet.wordnet_functs import synset_program, synset_choose, synset_compare, synset_sentence_match, \
    possible_languages

# from regex_utilities import remove_punct
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ### tokenizer stuff
    # get_all_tokened(lang_dir, tokenized_dir, 2000, 30254)

    # ### SynSetter Stuff
    print(f"wordnet possible languages: {possible_languages()}")
    synset_program()
    print(f"wordnet possible languages: {possible_languages()}")
    type = 1;
    while type == 1 or type == 2:
        while True:
            type = input("what would you like to compare?\n\t1.words\n\t2.sentences\n\t0.exit")
            if type and int(type) in [0,1,2]:
                break;

        if type == 1:
            choice = str(input("What Word would you like the synonyms and antonyms for?"))
            synset_choose(choice)
            compare=input("What word would you like to commpare your word/sentence with?")
            if compare == "stop":
                break
            synset_compare(choice.strip(), compare.strip())

        elif type == 2:
            choice = str(input("What is the first sentence you would like to compare?"))
            lang1 = str(input("What is that sentence's language?"))
            compare=str(input("What is the second sentence you would like to compare?"))
            lang2 = str(input("What is that sentence's language?"))
            synset_sentence_match(choice.strip(), compare.strip(),
                                  lang1.strip(), lang2.strip())

    ### Lemma Checking

    #loading PYTHONPATH
    # ad('bible-backend-fastapi')
    # ad('Wordnet')