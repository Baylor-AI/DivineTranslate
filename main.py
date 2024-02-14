from LanguageTokenizer.TxtToToken import text_tokenize
import os, glob, json

# This is the directory where all the txt files should go for tokenization.
lang_dir = 'DBTextFiles'
tokenized_dir = 'TokenizedDB'

"""
gets all translation files from the specified txt_directory and puts them into their tokenized format in the 
token_directory
"""
## TODO: make db version of this
def get_all_tokened(txt_directory, token_directory):
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
    if num_tokens < 2: # Error if not enough files
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
            # checks of the target and source laguage are different
            if language_to is not language_from:
                print(f'{language_from[0].get(lang_key)} -> {language_to[0].get(lang_key)}')
                # TODO: Assume all files are same length
                # Maps source language to their translation
                for i in range(len(language_from)):
                    line1 = language_from[i]
                    line2 = language_to[i]
                    if not line1.get(tl_key) or not line2.get(tl_key):
                        continue
                    mapping.append(
                        {line1.get(lang_key): line1.get(tl_key),
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
            # outputting text version of the dictionary
            # for mapped in mapping:
            #     # print(mapped.__str__())
            #     output.write(f'{mapped.__str__()}\n')

from Wordnet.wordnet_test import synset_program, synset_choose, synset_compare

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #tokenizer function
    # get_all_tokened(lang_dir, tokenized_dir)
    # synset_program()
    choice = str(input("What Word would you like the synonyms and antonyms for?"))
    synset_choose(choice)
    while True:
        compare=input("What word would you like to commpare your word with?")
        if compare == "stop":
            break
        synset_compare(choice, compare)