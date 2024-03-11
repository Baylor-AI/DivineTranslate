from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from Wordnet.wordnet_functs import wn, match_lemma_list

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/word_similarity/")
def comparison_endpoint(
        initial: str = '',
        compare: str = '',
        lang1: str = 'spa',
        lang2: str = 'eng',
        limit: int = 5
):
    result = []
    first = None
    second = None
    match = []
    # for lem in wn.lemmas(initial,lang=lang1):
    #     for lem2 in wn.lemmas(compare, lang=lang2):
    #         match.append(match_lemma())
    # if first and second:
    #     for syn in wn.synsets(compare, lang=lang2):
    #         result[syn.name()] ={
    #             'word': syn.name(),
    #             'percentage': syn.wup_similarity(initial)
    #         }
    # result = [{'word': 'apple', 'percentage': 0.5}, {'word': 'banana', 'percentage': 0.65},
    #           {'word': 'pear', 'percentage': 0.4}, {'word': 'bat', 'percentage': 0.14}]
    match = match_lemma_list(initial, compare, lang1,lang2, limit)
    for word in match:
        result.append(word['word'])
        result.append(word['percentage'])
    print(result)
    return result[:limit]
    # return {'apple', 0.5, 'banana', 0.65, 'pear', 0.4, 'bat', 0.14}
