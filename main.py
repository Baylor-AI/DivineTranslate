import io

from LanguageTokenizer.TxtToToken import text_tokenize

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ## TODO send this stuff to a function and run it
    print_hi('PyCharm')
    file = io.open("DBTextFiles/eng_ENGESV.api.txt", mode="r", encoding="utf-8")
    tokens = []
    tokens.append(text_tokenize(file, "eng"))
    file = io.open("DBTextFiles/cmn_CHNNCT.cloud.txt", mode="r", encoding="utf-8")
    tokens.append(text_tokenize(file,"cmn"))

    length = len(tokens)
    mapping = []
    for i in range(length):
        for j in range(len(tokens[i])):
            mapping.append(
                {tokens[i][j].get('lang') : tokens[i][j].get('tl'),
                 tokens[(i+1) % length][j].get('lang') : tokens[(i+1) % length][j].get('tl')}
            )

    for mapped in mapping:
        print(mapped.__str__())

    file.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
