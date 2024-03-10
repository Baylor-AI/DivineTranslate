import jieba

def tokenize_chinese(text):
    # Tokenize the Chinese text
    words = jieba.cut(text)

    # Join the words back into a sentence
    chinese_text = ' '.join(words)

    return chinese_text


# chinese_sentence = "你好，今天天气很好！"
# tokenized_chinese = tokenize_chinese(chinese_sentence)
# print(tokenized_chinese)
