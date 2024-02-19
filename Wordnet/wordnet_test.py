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
    similarity=None
    if choice and compare_with:
        print(f"after lemma: {choice} v {compare_with}")
        choice_set = set(synset_get_exact(choice))
        compare_set = set(synset_get_exact(compare_with))
        print(f'{choice_set}\n v \n{compare_set}')
        for word in choice_set:
            for comp in compare_set:
                if word.pos() == comp.pos():
                    found = True
                    print(f'{word} v {comp} == {word.wup_similarity(comp)}')
                    similarity=word.wup_similarity(comp)
                    break;
            if found:
                break;
    else:
        print(f'No comparison available for {choice} v {compare_with }')
    return similarity

def synset_speech_match(sentence1, sentence2):
    prob_set=[]

    # We are comparing the similarity of two sentences, and assuming they are the same length
    for i in range(len(sentence1)):
        if sentence2[i] and sentence1[i]:
            temp = synset_compare(sentence1[i], sentence2[i])




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
