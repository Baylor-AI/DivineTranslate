import io, logging

def text_tokenize_db(txt, language='', version='', book='', chapter='', verse=''):
    file = io.open("TokenFile", mode="rw", encoding="utf-8")

    ## TODO: grab the verse from the database/file as a token and output it in the form {"lang":"language1", "tl":"string"}
    translations = []
    for line in file.readlines():
        translations.append(line.strip())

    tokens = [{'lang':language, 'tl': t} for t in translations]
    # for line in tokens:
    #     print(line.__str__())

    ##TODO: write token to file
    return tokens

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
