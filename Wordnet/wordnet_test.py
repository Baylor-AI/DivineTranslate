import nltk
nltk.download('popular')
from nltk.corpus import wordnet

def synset_program():
    syns = wordnet.synsets("program")
    for syn in syns:
        print(f'=============\nWord: {syn.name()}')
        print(f'Lemmas: {syn.lemmas()}')
        # for l in syn.lemmas():
        #     print(f'{l.name()},'),

        print(f'\nDefinition: {syn.definition()}')
        i=0
        print(f'Sentence Examples:')
        for ex in syn.examples():
            print(f'\t{++i}. {ex}')
        print("=============")


def synset_choose(choice):
    synonyms=[]
    antonyms=[]

    for syn in wordnet.synsets(str(choice)):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    if synonyms: print(f'Synonyms: {set(synonyms)}')
    if antonyms: print(f'Antonyms: {set(antonyms)}')

def synset_compare(choice, compare_with):
    print(f'{wordnet.synsets(choice)[0]} v {wordnet.synsets(compare_with)[0]}')
    if wordnet.synsets(choice) and wordnet.synsets(compare_with):
        print(wordnet.synsets(choice)[0].wup_similarity(wordnet.synsets(compare_with)[0]))