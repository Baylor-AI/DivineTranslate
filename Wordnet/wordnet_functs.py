import string
import unicodedata

import nltk

nltk.download('perluniprops')
nltk.download('popular')
# set abbreviations for the wordnet items
from nltk.corpus import wordnet as wn, stopwords as sw
from nltk.tokenize import word_tokenize

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
    antonyms_list = [a.antonyms() for a in wn.lemmas(choice) if a.antonyms()]
    for syn in wn.synsets(str(choice)):
        for l in syn.lemmas():
            synonyms_list.append(l.name())
            if l.antonyms():
                antonyms_list.append(l.antonyms())
    if synonyms_list: print(f'Synonyms: {synonyms_list}')
    if antonyms_list: print(f'Antonyms: {antonyms_list}')


def synset_compare(choice, compare_with, lang1='eng', lang2='cmn', limit=5):
    choice = wn.morphy(choice)
    compare_with = wn.morphy(compare_with)
    similarity = []
    if choice and compare_with:
        choice_set = set(synset_get_exact(choice, lang1))
        compare_set = set(synset_get_exact(compare_with, lang2))
        found = False
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
    sentence1 = remove_stopwords_tokens(
        remove_punct_tokens(list(([w for w in word_tokenize(sentence1)]))))  # if not w.lower() in sw.words(lang1)]))
    sentence2 = remove_stopwords_tokens(
        remove_punct_tokens(list(([w for w in word_tokenize(sentence2)]))))  # if not w.lower() in sw.words(lang2)]))
    # print(f"tokenized s1: {sentence1}\n lemmas: {[wn.lemmas(w, lang=lang1) for w in sentence1]}")
    # print(f"tokenized s2: {sentence2}\n lemmas: {[wn.lemmas(w, lang=lang2) for w in sentence2]}")
    # We are comparing the similarity of two sentences, and assuming they are the same length
    checked = []
    for word1 in sentence1:
        prev = None
        if synset_get_exact(word1):
            syns1 = synset_get_exact(word1)
            synsets2 = [syns2 for syns2 in [synset_get_exact(word2) for word2 in sentence2]]
            if word1 not in checked:
                prev_sim = 0.0
                for word2 in sentence2:
                    for syn1 in syns1:
                        if word1 == word2:
                            prev = word2
                            prev_sim = wn.wup_similarity(syn1, match_lemma(word1, word2, lang1, lang2).synset())
                            break
                        for syns2 in synsets2:
                            for syn2 in syns2:

                                checks = [checker['word'] for checker in checked]
                                if (syn1.name().split('.')[0] not in checks and
                                        match_lemma(word1, word2, lang1, lang2) and
                                        prev_sim < wn.wup_similarity(syn1, syn2)):
                                    check_syn2 = match_lemma(word1, word2, lang1, lang2).synset()
                                    prev_sim = wn.wup_similarity(syn1, check_syn2)
                                    prev = word2
                if prev:
                    # print(f'{word1} map to {lang2}: \n-- comparing {prev} -> {match_lemma(word1, prev, lang1, lang2)}')
                    value = {
                        'word': word1,
                        'percentage': prev_sim
                    }
                    checked.append(value)  # match_lemma(word1, prev, lang1, lang2))
                    # print(f'{match_lemma_list(word1, prev, lang1, lang2)}')
    word_sim = 0.0
    sentence_sim = 0.0
    avg_sen_len = (len(sentence1) + len(sentence2)) / 2
    if len(checked) > 0:
        # for mapped in checked:
        #     print(f'values: {mapped}')
        word_sim = sum(item['percentage'] for item in checked) / len(checked)
        sentence_sim = ((len(sentence1) / avg_sen_len) + (len(sentence2) / avg_sen_len) )/2
    else:
        print(f'No matching synsets found.')

    print(f'Total Sentence Len (approx): {avg_sen_len} \n'
          f'{sentence1} \n'
          f'    vs\n'
          f'{sentence2}')
    print(f'Sentence similarity: \n'
          f'--- Word Similarities: {round(word_sim, 2)}\n'
          f'--- Sentence Length Similarity: {round(sentence_sim,2)}\n'
          f'------ Approximate Similarity: {round((word_sim + sentence_sim) / 2, 2)}')


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


def match_lemma(word1, word2, lang1, lang2):
    '''
    Gets the common element in two lists of lemmas
    :param word1:
    :param lang1:
    :param word2:
    :param lang2:
    :return:
    '''
    lems1 = wn.lemmas(wn.morphy(remove_punct(word1).lower()), lang=lang1)
    lems2 = wn.lemmas(wn.morphy(remove_punct(word1).lower()), lang=lang2)
    # print(f'{lems1} v {lems2}')
    match = None
    sim = 0.0
    for lem1 in lems1:
        if lem1.synset():
            for lem2 in lems2:
                if lem2.synset():
                    # print(f'{lem1.synset()} vs {lem2.synset()} ====> {sim}')
                    if lem1.synset() == lem2.synset() and wn.wup_similarity(lem1.synset(), lem2.synset()) > sim:
                        # print(f'{lem1.synset()} vs {lem2.synset()}')
                        match = lem1
                        sim = wn.wup_similarity(lem1.synset(), lem2.synset())
                        # print(f'{lem1.synset()} vs {lem2.synset()} ====> {sim}')
    return match


def match_lemma_list(word1, word2, lang1, lang2, limit=5):
    '''
    Gets the common element in two lists of lemmas
    :param word1:
    :param lang1:
    :param word2:
    :param lang2:
    :return:
    '''
    match = []
    if word1 and word2:
        # print(f'{word1} vs {word2}')
        word1 = remove_punct(word1).lower()
        word2 = remove_punct(word2).lower()
        lems1 = wn.lemmas(word1, lang=lang1) if not wn.morphy(word1) \
            else wn.lemmas(wn.morphy(word1))
        lems2 = wn.lemmas(word2, lang=lang2) if not wn.morphy(word2) \
            else wn.lemmas(wn.morphy(word2))

        for lem1 in lems1:
            if lem1.synset():
                for lem2 in lems2:
                    if lem2.synset():
                        # print(f'{lem1.synset()} vs {lem2.synset()} ====> {sim}')
                        if wn.wup_similarity(lem1.synset(), lem2.synset()):
                            # print(f'{lem1} vs {lem2}')
                            sim = wn.wup_similarity(lem1.synset(), lem2.synset())
                            # print(f'{lem1.synset()} vs {lem2.synset()} ====> {sim}')
                            match.append((lem1.synset(), lem2.synset(), sim))

    results = []
    for pair in match:
        for item in pair[0].lemmas():
            if pair[1].name() != item.synset().name():
                # print(f'{item.synset()} vs {pair[1]}')
                # results.add(tuple({'word': f'{item.synset().name()} match {pair[1].name()}',
                #                    'percentage': pair[2] * wn.wup_similarity(pair[0], item.synset()) * 100}.items()
                #                   ))
                # print(f'{word2} matches {pair[1].name().split(".")[0]}' if f'{word2} matches {pair[1].name().split(".")[0]}' not in [synonyms['word'] for synonyms in results] else '')
                if f'{word2} matches {pair[1].name().split(".")[0]}' \
                        not in [synonyms['word'] for synonyms in results] \
                        and f'{pair[1].name().split(".")[0]} matches {word2}' \
                        not in [synonyms['word'] for synonyms in results]:
                    results.append({
                        'word': f'{word2} matches {pair[1].name().split(".")[0]}',
                        'percentage': pair[2] * wn.wup_similarity(pair[0], item.synset()) * 100,
                        'empty': False
                    })
    if not results:
        results.append({
            'word': '',
            'percentage': 0.0,
            'empty': True
        })

    sorted_results = sorted(results, key=lambda x: x['percentage'], reverse=True)
    return sorted_results[:limit]


def possible_languages():
    return wn.langs()


def remove_stopwords_tokens(text, lang='english'):
    stop_words = set(sw.words(lang))

    filtered_text = [word for word in text if word.lower() not in stop_words]

    return filtered_text


def remove_punct_tokens(text):
    punctuations = string.punctuation
    no_puncts = [remove_punct(word) for word in text if word not in punctuations]

    return no_puncts


def remove_punct(text):
    # punctuations = re.compile(r'[\p{P}\p{S}]')
    no_puncts = ''.join(char.lower() for char in text if not unicodedata.category(char).startswith('P'))
    # no_puncts = punctuations.sub('', text)

    return no_puncts


def to_lang(text, lang):
    lang_words = []

    return lang_words
