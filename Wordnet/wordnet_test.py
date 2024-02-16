import nltk
nltk.download('popular')
# set abbreviations for the wordnet items
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer as wnl

def synset_program():
    syns = wn.synsets("program")
    for syn in syns:
        print(f'=============\nWord: {syn.name()}')
        print(f'Lemmas: {set(syn.lemmas())}')
        print(f'\nDefinition: {syn.definition()}')
        i=0
        print(f'Sentence Examples:')
        for ex in syn.examples():
            print(f'\t{++i}. {ex}')
        print("=============")

def synset_choose(choice):
    synonyms=[]
    antonyms=[]
    for syn in wn.synsets(str(choice)):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    if synonyms: print(f'Synonyms: {set(synonyms)}')
    if antonyms: print(f'Antonyms: {set(antonyms)}')

def synset_compare(choice, compare_with, pos=None):
    lem = wnl()
    # choice = lem.lemmatize(choice)
    # compare_with = lem.lemmatize(compare_with)
    choice = wn.morphy(choice)
    compare_with = wn.morphy(compare_with)
    print(f"after lemma: {choice} v {compare_with}")
    print(f'{set(wn.synsets(choice))}\n v \n{set(wn.synsets(compare_with))}')
    if wn.synsets(choice) and wn.synsets(compare_with):
        print(wn.synsets(choice)[0].wup_similarity(wn.synsets(compare_with)[0]))

def synset_speech_match(choice, compare_with):
    lem = wnl()

# gets only synsets that contain the exact word
def synset_get_exact(to_synset):
    '''
    Gets only synsets that contain the original word
    :param to_synset: the word to get the exact synsets for
    :return: a set of synsets that only contain the input word
    '''
    lem=wnl()
    to_synset=wn.morphy(to_synset)
    exact_word = []
    for syn in wn.synsets(to_synset):
        if to_synset in syn.name():
            exact_word.append(syn)
    return exact_word
