
# TODO: Replace all of these with an os.environ implementation and update security

# This is the directory where all the txt files should go for tokenization.
# important directories
lang_dir = 'DBTextFiles' # directory where all the text files are stored. Can be removed when DB has all file contents inserted
tokenized_dir = 'TokenizedDB' # directory where all the mappings are stored
model_dir = 'model' # directory where all the models are stored


### Tokenization Information
lang_code_size = 3 # predicted size of the language code for ISO-639-2
lang_key = 'lang' # the key for language codes
tl_key = 'tl' # the key for versions of a verse in the bible in the given language


### Models Storage
tmp_model = 'Doc2Vec.model' # the expected trained sentence comparison model location
word_embeddings = 'Word2Vec.model' # the expected trained word comparison model location
train_sents = 'trained.dat'

f_enc = 'utf-8' # the encoding to be used for file stuff

# TODO: FIX THIS MAPPING TO CONTAIN THE WHOLE SET OF LANGUAGES
# may want to use some ai to generate this
lang_map = {
    ## a
    ## b
    ## c
    'cmn': 'chinese',
    ## d
    'deu': 'german',
    ## e
    'eng': 'english',
    ## f
    'fra': 'french',
    ## g
    ## h
    'hai': 'haida',
    ## i
    ## j
    'jpn': 'japanese',
    ## k
    ## l
    ## m
    ## n
    'nse': 'nsenga',
    ## o
    ## p
    ## q
    ## r
    ## s
    'spa': 'spanish',
    ## t
    ## u
    ## v
    ## w
    ## x
    ## y
    ## z
}
