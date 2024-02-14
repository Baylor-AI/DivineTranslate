from nltk.corpus import wordnet

def synset_program():
    syns = wordnet.synsets("program")
    print(syns[0].name())
    print(syns[0].lemmas()[0].name())
    print(syns[0].definition())
    print(syns[0].examples())

def synset_choose(choice):
    synonyms=[]
    antonyms=[]

    for syn in wordnet.synsets(choice):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].na)