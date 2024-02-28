import sys
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from Wordnet.wordnet_test import synset_compare

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
    result = synset_compare(initial, compare, lang1, lang2)
    result = result[:limit]
    result = [{'word': 'apple', 'percentage': 0.5}, {'word': 'banana', 'percentage': 0.65},
              {'word': 'pear', 'percentage': 0.4}, {'word': 'bat', 'percentage': 0.14}]

    print(result)

    return result
    # return {'apple', 0.5, 'banana', 0.65, 'pear', 0.4, 'bat', 0.14}
