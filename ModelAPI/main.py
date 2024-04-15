from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, T5ForConditionalGeneration


# README - HOW TO RUN
# pip install fastapi uvicorn
# uvicorn main:app --reload
# send POST requests to http://localhost:8000/translate/
# {
#   "text": "Hello!",
#   "source_lang_code": "eng",
#   "target_lang_code": "cmn"
# }

#https://gitlab.com/rivas-bible/rivas-bible.gitlab.io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranslationRequest(BaseModel):
    text: str
    source_lang_code: str
    target_lang_code: str

@app.post("/translate/")
async def translate_text(request: TranslationRequest):
    # Define tokenization and model loading within the endpoint function
    padding = "max_length"
    truncation = True
    max_length = 512

    tokenizer = AutoTokenizer.from_pretrained('google/byt5-small')
    trained_model = T5ForConditionalGeneration.from_pretrained('./')
    print(request.source_lang_code)
    print(request.target_lang_code)

    prefix = f"translate {request.source_lang_code} to {request.target_lang_code}: "
    prefixed_text = prefix + request.text
    print(prefixed_text)


    # Tokenize the input text
    encoded_input = tokenizer(prefixed_text, padding=padding, truncation=truncation, max_length=max_length,
                              return_tensors="pt")

    # Generate translation
    output_tokens = trained_model.generate(**encoded_input, max_length=max_length)

    # Decode the generated tokens to text
    translated_text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)

    return {"translated_text": translated_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
