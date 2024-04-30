from LanguageTokenizer.TxtToToken import text_tokenize

import os, json
import env_vars as env

### TODO: Run manual and Automatic testing for each function in main
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # ### Gensim
    # from Gensim.gensim_functs import train_model
    # train_model()
    # try:
    #     # sentence_sim(f'cmn-x-bible-sf_ncv-zefania-v1.txt', infer_val="神说 ： “要有光 ！ ”就有了光。")
    #     sentence_sim(f'eng-x-bible-kingjames-v1.txt', infer_val="And God said , Let there be light : and there was light .")
    #     word_sim("said")
    #     # word_sim("神说")
    # except FileNotFoundError as f:
    #     # sentence_sim(f'cmn-x-bible-sf_ncv-zefania-v1.txt', infer_val="神说 ： “要有光 ！ ”就有了光。")
    #     sentence_sim(f'eng-x-bible-kingjames-v1.txt', infer_val="And God said , Let there be light : and there was light .")
    #     # word_sim("神说")
    #     word_sim("said")

    # model_training_sentence_sim(lang_dir)
    from Gensim.gensim_word2vec import train_model_per_directory, gensim_sentence_sim

    arb_lim = 5
    # gensim_sentence_sim(
    #     input_sentence="于是 ， 地上长出了青草和结种子的蔬菜 ， 各从其类 ； 又长出结果子的树木 ， 各从其类 ， 果子都包着核。 神看这是好的。",
    #     chosen_lang='cmn',
    #     limit=arb_lim
    # )

    # gensim_sentence_sim(
    #     input_sentence="first, god made the heavens and earth",
    #     chosen_lang='eng',
    #     limit=arb_lim
    # )

    ## tokenizer stuff
    # from LanguageTokenizer.FileTokenizerAggregator import get_all_tokened
    #
    # get_all_tokened(txt_directory=env.lang_dir, token_directory=env.tokenized_dir, one_way=True, one_file=True,
    #                 limit=30000, offset=0)

    ### fun lil cli for wordnet/gensim stuff
    ### SynSetter Stuff
    from Wordnet.wordnet_functs import synset_program, synset_choose, synset_compare, synset_sentence_match, \
        possible_languages, match_lemma_list, match_lemma

    # print(match_lemma_list('dios', 'god ', 'spa', 'eng'))
    # print(f"wordnet possible languages: {possible_languages()}")
    # synset_program()
    # print(f"wordnet possible languages: {possible_languages()}")
    type = "1";
    allowed_types = ['0','1','2','3']
    type_values = [
        'exit',
        'words with Wordnet',
        'sentences with Wordnet',
        'single sentence with bible verses'
    ]
    while type.isdigit() and int(type) != 0:
        while True:
            type = input(f"what would you like to compare?" +
                         ''.join(f'\n\t{item}. {type_values[index]}'
                                 for index, item in enumerate(sorted(allowed_types, reverse = False))
                     )
                    )
            if type.strip() and type in allowed_types:
                break

        if type == '1':
            choice = str(input("What Word would you like the synonyms and antonyms for?"))
            synset_choose(choice)
            compare=input("What word would you like to commpare your word/sentence with?")
            if compare == "stop":
                break
            synset_compare(choice.strip(), compare.strip())

        elif type == '2':
            choice = str(input("What is the first sentence you would like to compare?"))
            lang1 = str(input("What is that sentence's language?"))
            compare=str(input("What is the second sentence you would like to compare?"))
            lang2 = str(input("What is that sentence's language?"))
            synset_sentence_match(choice.strip(), compare.strip(),
                                  lang1.strip(), lang2.strip())

        elif type == '3':
            choice = str(input("What is the sentence you would like to compare?"))
            lang1 = str(input("What is that sentence's language?"))
            arb_lim = input("How many examples would you like?")
            while not arb_lim.isdigit():
                arb_lim = input("How many examples would you like?")

            gensim_sentence_sim(
                input_sentence=choice,
                chosen_lang=lang1,
                limit=int(arb_lim)
            )




