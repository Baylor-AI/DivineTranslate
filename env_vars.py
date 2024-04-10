# This is the directory where all the txt files should go for tokenization.
# important directories
lang_dir = 'DBTextFiles' # directory where all the text files are stored. Can be removed when DB has all file contents inserted
tokenized_dir = 'TokenizedDB' # directory where all the mappings are stored

lang_code_size = 3 # predicted size of the language code for ISO-639-2

lang_key = 'lang' # the key for language codes
tl_key = 'tl' # the key for versions of a verse in the bible in the given language

tmp_model = 'model\Doc2Vec.model' # the expected trained sentence comparison model location
word_embeddings = 'model\Word2Vec.model' # the expected trained word comparison model location

f_enc = 'utf-8' # the encoding to be used for file stuff