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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_methods=["*"],
    allow_headers=["*"],
)




app = FastAPI()

padding = "max_length"
truncation = True
max_length = 512

# Load pre-trained model
trained_model = T5ForConditionalGeneration.from_pretrained('./')
trained_model.to('cuda')

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
                              return_tensors="pt").to('cuda')

    output_tokens = trained_model.generate(**encoded_input, max_length=max_length).to('cuda')
    translated_text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)

    return {"translated_text": translated_text}
