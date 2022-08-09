# -*- coding: utf-8 -*-
import json
import re


def recommand_words(words:dict):
    score = {}
    for word in words:
        repeat = {}
        s = 0
        for i in word:
            repeat[i] = word.count(i)
            for j in repeat:
                s += repeat[j]
        if s in score:
            score[s][word] = words[word]
        else:
            score[s] = {word:words[word]}
    min_repeat = 1000
    for s in score:
        if s < min_repeat:
            min_repeat = s
    print(score[s])
    return score[min_repeat]
    
def letter_in_word(words:dict,letter:str,istrue:bool) -> list:
    count = 0
    letters = set()
    copy_words = words.copy()
    for i in letter:
        if i not in letters:
            letters.add(i)
    for word in words:
        for i in letters:
            if (i in word) != istrue:
                count += 1
                copy_words.pop(word)
                break
    log = '移除了%d个%s包含%s的单词' % (count,('不' if istrue else ''),letter)
    return copy_words,log

            
def right_index(words:dict,indexs:list,istrue:bool) -> list:
    count = 0
    rounds = 0
    copy_words = words.copy()
    for word in words:
        for i in indexs:
            if (word[int(i[1])-1] != i[0] ) == istrue:
                count += 1
                copy_words.pop(word)
                break
    
    log = '移除了%s个%s满足%s的单词' % (count,('不' if istrue else ''),indexs)
    return copy_words,log

f = open('dicts.json','r')
words = json.load(f)





if __name__ == '__main__':
    word_len = input('输入单词长度:')
    if not word_len.isdigit():
        print('请输入数字')
        exit()
    word_len = int(word_len)
    words = [word for word in words if len(word) == word_len]
    print('剩余单词数量：%s'%len(words))
    recommand_words(words)
    rounds = word_len + 1
    while(rounds > 0):
        rounds -= 1
        letter_in_words = input('输入在单词中的字母：')
        letter_not_in_word = input('输入不在单词中的字母：')
        letter_in_right_index = input('输入在单词中的字母的正确位置(格式 a=1,b=2):')
        letter_in_wrong_index = input('输入在单词中的字母的错误位置(格式 a=1,b=2):')
        
        if letter_in_words:
            words = letter_in_word(words,letter_in_words,True)
        if letter_not_in_word:
            words = letter_in_word(words,letter_not_in_word,False)
        
        parse_re = r'\,?([a-z])=(\d)\.*?'
        if letter_in_wrong_index:
            indexs = re.findall(parse_re,letter_in_wrong_index)
            words = right_index(words,indexs,False)
        if letter_in_right_index:
            indexs = re.findall(parse_re,letter_in_right_index)
            words = right_index(words,indexs,True)

        recommand_words(words)
        print('剩余单词数量：%s'%len(words))
        print(words)
        

