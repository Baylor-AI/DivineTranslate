from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, T5ForConditionalGeneration

app = FastAPI()
# README - HOW TO RUN
# go into venv like for WordNetAPI
# cd ModelAPI
# uvicorn main:app --reload
# send POST requests to http://localhost:8000/translate/
# {
#   "text": "Hello!",
#   "source_lang_code": "eng",
#   "target_lang_code": "cmn"
# }


padding = "max_length"
truncation = True
max_length = 512

# Load pre-trained model
trained_model = T5ForConditionalGeneration.from_pretrained('./')  # Assuming model files are in the same directory as main.py
# Remove .to('cuda') call
# trained_model.to('cuda')

class TranslationRequest(BaseModel):
    text: str
    source_lang_code: str
    target_lang_code: str

def generate_prefix(source_lang_code, target_lang_code):
    return f"translate {source_lang_code} to {target_lang_code}: "

@app.post("/translate/")
async def translate_text(request: TranslationRequest):
    prefix = generate_prefix(request.source_lang_code, request.target_lang_code)
    prefixed_text = prefix + request.text

    tokenizer = AutoTokenizer.from_pretrained('google/byt5-small')

    encoded_input = tokenizer(prefixed_text, padding=padding, truncation=truncation, max_length=max_length,
                              return_tensors="pt")  # Removed .to('cuda')

    output_tokens = trained_model.generate(**encoded_input, max_length=max_length)  # Removed .to('cuda')
    translated_text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)

    return {"translated_text": translated_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

