from LanguageTokenizer.TxtToToken import text_tokenize

import os, json
import env_vars as env

### TODO: Run manual and Automatic testing for each function in main
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ## tokenizer stuff
    # from LanguageTokenizer.FileTokenizerAggregator import get_all_tokened
    #
    # get_all_tokened(txt_directory=env.lang_dir, token_directory=env.tokenized_dir, one_way=True, one_file=True,
    #                 limit=30000, offset=0)

    # print(match_lemma_list('prueba', 'test', 'spa', 'eng'))

    # ### fun lil cli for wordnet stuff
    # ### SynSetter Stuff
    # from Wordnet.wordnet_functs import synset_program, synset_choose, synset_compare, synset_sentence_match, \
    #     possible_languages, match_lemma_list, match_lemma
    # print(f"wordnet possible languages: {possible_languages()}")
    # synset_program()
    # print(f"wordnet possible languages: {possible_languages()}")
    # type = 1;
    # while type == 1 or type == 2:
    #     while True:
    #         type = input("what would you like to compare?\n\t1.words\n\t2.sentences\n\t0.exit")
    #         if type and int(type) in [0,1,2]:
    #             type = int(type)
    #             break;
    #
    #     if type == 1:
    #         choice = str(input("What Word would you like the synonyms and antonyms for?"))
    #         synset_choose(choice)
    #         compare=input("What word would you like to commpare your word/sentence with?")
    #         if compare == "stop":
    #             break
    #         synset_compare(choice.strip(), compare.strip())
    #
    #     elif type == 2:
    #         choice = str(input("What is the first sentence you would like to compare?"))
    #         lang1 = str(input("What is that sentence's language?"))
    #         compare=str(input("What is the second sentence you would like to compare?"))
    #         lang2 = str(input("What is that sentence's language?"))
    #         synset_sentence_match(choice.strip(), compare.strip(),
    #                               lang1.strip(), lang2.strip())

    # ### Gensim
    from Gensim.gensim_functs import sentence_sim, word_sim
    try:
        sentence_sim(f'eng\\eng-x-bible-kingjames-v1.txt')
        word_sim("said")
    except FileNotFoundError as f:
        sentence_sim('eng-x-bible-kingjames-v1.txt')
        word_sim("said")

    # model_training_sentence_sim(lang_dir)
