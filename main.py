import os, glob

# This is the directory where all the txt files should go for tokenization.
txt_directory='DBTextFiles'
txt_directory_size=len(txt_directory)+1
token_directory='TokenizedDB'

def get_all_tokened():
    tokens = []
    extension_len=4
    lang_len=3
    for filename in glob.glob(os.path.join(txt_directory, '*.txt')):
        with io.open(os.path.join(os.getcwd(), filename), mode='r', encoding='utf-8') as file:
            print(filename[txt_directory_size:txt_directory_size+lang_len])
            content = text_tokenize(file, filename[txt_directory_size:txt_directory_size+lang_len])
            content.append(filename[txt_directory_size:-extension_len])
            tokens.append(content)

    num_tokens = len(tokens)
    list_len = len(tokens[0]) - 1
    for i in range(num_tokens):
        mapping = []
        for k in range(num_tokens):
            if i != k:
                with io.open(os.path.join(os.path.join(os.getcwd()),token_directory,f'{tokens[i][list_len]}_to_{tokens[k][list_len]}.txt'),
                             mode='w', encoding='utf-8') as output:
                    # mapping.append({'langTolang':f'{tokens[i][list_len]}_to_{tokens[k][list_len]}'})
                    for j in range(list_len):
                        mapping.append(
                            {tokens[i][j].get('lang'): tokens[i][j].get('tl'),
                             tokens[k][j].get('lang'): tokens[k][j].get('tl')}
                        )
                    for mapped in mapping:
                        # print(mapped.__str__())
                        output.write(f'{mapped.__str__()}\n')

import io
from LanguageTokenizer.TxtToToken import text_tokenize

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_all_tokened()
    print_hi('PyCharm')



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
