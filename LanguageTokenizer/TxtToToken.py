import io
import threading
import time
import logging


#
# def text_tokenize(book, chapter, verse, language1, language2):
#     file = io.open("TokenFile", mode="rw", encoding="utf-8")
#
#     ## TODO: grab the verse from the database as a token and output it in the form {"language1":"string", "language2","string_translation"}
#     token = []
#     for
#
#     ##TODO: write token to file

def text_tokenize(file, language1, book='', chapter='', verse=''):
    # file = io.open(file + "TokenFile", mode="rw", encoding="utf-8")

    ## TODO: grab the verse from the database/file as a token and output it in the form {"lang":"language1", "tl":"string"}
    translations = []
    for line in file.readlines():
        translations.append(line.strip())

    tokens = [{'lang':language1, 'tl': t} for t in translations]
    # for line in tokens:
    #     print(line.__str__())

    ##TODO: write token to file
    return tokens
