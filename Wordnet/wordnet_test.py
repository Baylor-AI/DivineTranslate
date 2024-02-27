import nltk

nltk.download('perluniprops')
nltk.download('popular')
# set abbreviations for the wordnet items
from nltk.corpus import wordnet as wn, stopwords as sw
from nltk.tokenize import word_tokenize
from nltk.tokenize.nist import NISTTokenizer as nt

nltk.download('stopwords')

# TODO: FIX THIS MAPPING TO CONTAIN THE WHOLE SET OF LANGUAGES
language_mapping = [
    {'english': 'eng'}
]
def synset_program(lang='cmn'):
    syns = wn.synsets("program")
    wn.langs()
    print(f'synonyms for word: programming')
    for syn in syns:
        print(f'=============\nWord: {syn.name()}')
        print(f'Lemmas: {set(syn.lemmas())}')
        print(f'in {lang}: {set(syn.lemmas(lang))}')

        print(f'\nDefinition: {syn.definition()}')
        # synset_choose(syn.name().split('.')[0])
        i = 0
        print(f'Sentence Examples:')
        for ex in syn.examples():
            i += 1
            print(f'\t{++i}. {ex}')
        print("=============")

def synset_choose(choice, lang='eng'):
    synonyms_list = []
    antonyms_list = []
    # synonyms = wn.synonyms(choice)
    antonyms_list = [a.antonyms() for a in wn.lemmas(choice) if a.antonyms()]
    for syn in wn.synsets(str(choice)):
        for l in syn.lemmas():
            synonyms_list.append(l.name())
            if l.antonyms():
                antonyms_list.append(l.antonyms())
    if synonyms_list: print(f'Synonyms: {synonyms_list}')
    if antonyms_list: print(f'Antonyms: {antonyms_list}')

def synset_compare(choice, compare_with, lang1='eng', lang2='cmn',limit=5):
    choice = wn.morphy(choice)
    compare_with = wn.morphy(compare_with)
    similarity = []
    if choice and compare_with:
        choice_set = set(synset_get_exact(choice, lang1))
        compare_set = set(synset_get_exact(compare_with, lang2))
        found=False
        for word in choice_set:
            for comp in compare_set:
                if len(similarity) < limit:
                    found = True
                    break;
                if word.pos() == comp.pos():
                    similarity.append({'word': comp, 'percentage': word.wup_similarity(comp)})
                    print(f'{word} vs {comp}\n'
                          f'\tWu, Palmer == {word.wup_similarity(comp)}\n'
                          f'\tPath Similarity == {word.path_similarity(comp)}\n'
                          f'\tLeacock-Chodorow == {word.lch_similarity(comp)}\n')
            if found:
                break;
        if not found:
            print(
                f'No comparison for different parts of speech: '
                f'{set([s.pos() for s in choice_set])} vs {set(sy.pos() for sy in compare_set)}'
            )
    else:
        print(f'No comparison available for {choice} vs {compare_with}')
    return similarity



def synset_sentence_match(sentence1, sentence2, lang1='eng', lang2='eng'):
    # print(sw.words('english'))
    # print(sw.words('chinese'))
    # nistt = nt()
    # print(nistt.international_tokenize(sentence1))
    # print(nistt.international_tokenize(sentence2))
    sentence1 = list(([w for w in word_tokenize(sentence1)]))  # if not w.lower() in sw.words(lang1)]))
    sentence2 = list(([w for w in word_tokenize(sentence2)]))  # if not w.lower() in sw.words(lang2)]))
    print(f"tokenized s1: {sentence1}\n lemmas: {[wn.lemmas(w, lang=lang1) for w in sentence1]}")
    print(f"tokenized s2: {sentence2}\n lemmas: {[wn.lemmas(w, lang=lang2) for w in sentence2]}")
    # We are comparing the similarity of two sentences, and assuming they are the same length
    checked = []
    for word1 in sentence1:
        prev = ''
        syns = ''
        if synset_get_exact(word1):
            syns1 = synset_get_exact(word1)[0]
            if word1 not in checked:
                prev_sim = 0.0
                for word2 in sentence2:
                    syns2 = ''
                    if synset_get_exact(word2):
                        syns2 = synset_get_exact(word2)[0]
                        if (syns2 not in checked and
                                check_lemmas(wn.lemmas(word1, lang=lang1), wn.lemmas(word2, lang=lang2)) and
                                prev_sim < syns1.wup_similarity(syns2)):
                            prev_sim = syns1.wup_similarity(syns2)
                            prev = word2
                if prev:
                    checked.append(map(word1.split('.')[0],
                                       syns1.wup_similarity(synset_get_exact(prev, lang2)[0])))
    for mapped in checked:
        print(f'values: {mapped}')

# gets only synsets that contain the exact word
def synset_get_exact(to_synset, lang='eng'):
    '''
    Gets only synsets that contain the original word
    :param to_synset: the word to get the exact synsets for
    :return: a set of synsets that only contain the input word
    '''
    to_synset = wn.morphy(to_synset)
    exact_word = []
    if to_synset:
        for syn in wn.synsets(to_synset):
            # print(syn.lemmas('cmn'))
            if to_synset in syn.name():
                exact_word.append(syn)
    return exact_word

def check_lemmas(list1, list2):
    '''
    Checks if the two lists of lemmas have a common element
    :param list1: the first list of lemmas
    :param list2: the second list of lemmas
    :return: Wether or not there was a similar element in the lists
    '''
    if list1 and list2:
        for word1 in list1:
            w1 = word1.name().split('.')[0] + '.'
            for word2 in list2:
                if w1 in word2.name():
                    return True
    return False


def possible_languages():
    return wn.langs()
