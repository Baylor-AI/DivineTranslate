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
    match = match_lemma_list(initial, compare, lang1,lang2, limit)
    for word in match:
        result.append(word['word'])
        result.append(word['percentage'])
    print(result)
    if not result:
        result = {initial, 0.0}
    return result
    # return {'apple', 0.5, 'banana', 0.65, 'pear', 0.4, 'bat', 0.14}
