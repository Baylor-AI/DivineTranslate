from transformers import AutoTokenizer, T5ForConditionalGeneration
import os

padding = "max_length"
truncation = True
# you can let use to set the max length of the translation, should be an int
max_length = 512

input_data = "Hello!" # user input

# the path of model should be like "/data/tianx/Wang_byt5_10K_50"
trained_model = T5ForConditionalGeneration.from_pretrained('***** PATH TO MODEL *****')
# you can change all ".to('cuda')" to ".to('cpu')"
trained_model.to('cuda')

source_lang_code = "eng" # user input source_lang_code
target_lang_code = "cmn" # user input target_lang_code
def generate_prefix(source_lang_code, target_lang_code):
    return f"translate {source_lang_code} to {target_lang_code}: "
prefix = generate_prefix(source_lang_code, target_lang_code)
prefixed_text = prefix + input_data

tokenizer = AutoTokenizer.from_pretrained('google/byt5-small')
# the prefixed_text should be "translate {source_lang_tag} to {target_lang_tag: {input_sentence}"
# example:
# translate eng to cmn: Hello!
# user should select source and target lang tags, which are "eng" and "cmn". And then write the input data
encoded_input = tokenizer(prefixed_text, padding=padding, truncation=truncation, max_length=max_length,
                          return_tensors="pt").to('cuda')

# generate translation
output_tokens = trained_model.generate(**encoded_input, max_length=max_length).to('cuda')
# decode translation to readable sentences
translated_text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)

# this is translated_text, it should be showed on the right side of website (assume our website looks like google translate)
print(translated_text)

