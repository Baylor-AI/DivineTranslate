import io
from LanguageTokenizer.TxtToToken import text_tokenize
import os, glob
from pathlib import Path

# This is the directory where all the txt files should go for tokenization.
lang_directory = 'DBTextFiles'
token_directory = 'TokenizedDB'
txt_directory_size = len(lang_directory) + 1

# global values TODO: remove and redesign
extension_len = 4
lang_len = 3


def get_all_tokened(txt_directory):
    tokens = []

    if not os.path.exists(os.path.join(os.getcwd(), txt_directory)):
        os.makedirs(txt_directory)

    for filename in glob.glob(os.path.join(txt_directory, '*.txt')):
        with io.open(os.path.join(os.getcwd(), filename), mode='r', encoding='utf-8') as file:
            print(filename[txt_directory_size:txt_directory_size + lang_len])
            content = text_tokenize(file, filename[txt_directory_size:txt_directory_size + lang_len])
            # content.append(filename[txt_directory_size:-extension_len])
            tokens.append(content)

    if not tokens:
        print(f'Empty Directory: {txt_directory}')
        return

    num_tokens = len(tokens)
    if num_tokens < 2:
        print(f'Not enough files in directory: must have at least 2 different translations!')
        return

    for language_from in tokens:
        mapping = []
        language_file = os.path.join(token_directory, f'{language_from[0].get("lang")}_mapping.txt')

        for language_to in tokens:
            if language_to is not language_from:
                print(f'{language_from[0].get("lang")} -> {language_to[0].get("lang")}')
                for i in range(len(language_from)):

                        line1 = language_from[i]
                        line2 = language_to[i]
                        if not line1.get('tl') or not line2.get('tl'):
                            continue

                        mapping.append(
                            {line1.get('lang'): line1.get('tl'),
                             line2.get('lang'): line2.get('tl')
                             }
                        )
                        mapping.append(
                            {line2.get('lang'): line2.get('tl'),
                             line1.get('lang'): line1.get('tl')
                             }
                        )
        with io.open(language_file, mode='w', encoding='utf-8') as output:
            for mapped in mapping:
                # print(mapped.__str__())
                output.write(f'{mapped.__str__()}\n')


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_all_tokened(lang_directory)
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
