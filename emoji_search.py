#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 13:11:32 2018

@author: benjaminlucas
"""
import numpy as np
import io


def LoadWordVecs(corpus_file, n_words = 10000):
    data = LoadWordVecRaw(n_words, corpus_file)
    word_mat = np.zeros([len(data), 300])
    word_dict = {}
    row_ind = 0
    for row in data:
        entries = row.split(' ')
        word_dict[entries[0]] = row_ind
        vec = [float(entries[i]) for i in range(1,301)]
        word_mat[row_ind,:] = vec
        row_ind += 1
    return [word_dict, word_mat]

def LoadWordVecRaw(n_tokens, root_directory):
    f = open(corpus_file,'r')
    f.readline()
    f.readline() # Remove first two lines of header data
    data = []
    for i in range(n_tokens):
        data.append(f.readline())
    f.close()
    return data


def FindEmoji(search_phrase, emoji_mat):
    search_vector = MakePhraseVec(search_phrase, word_dict, word_mat)
    similarity = np.matmul(emoji_mat, search_vector)
    sort_inds = np.flipud(np.argsort(similarity))
    #print(emoji_description[sort_inds[1]])
    return list(sort_inds[1:5])


def GenerateEmojiMat(emoji_description, word_dict, word_mat):
    emoji_mat = np.zeros([len(emoji_description), 300])
    for i, emoji in enumerate(emoji_description):
        vec = MakePhraseVec(emoji, word_dict, word_mat)
        emoji_mat[i,:] = vec
    return emoji_mat


def MakePhraseVec(phrase, word_dict, word_mat):
    stop_chars = [':', ';', '-',',']
    for c in stop_chars:
        phrase = phrase.replace(c,' ')
    words = phrase.lower().split(' ')
    words = [w for w in words if len(w) > 1]
    try:
        word_inds = [word_dict[w] for w in words]
        phrase_mat = word_mat[word_inds,:]
        phrase_vec = np.sum(phrase_mat, axis=0)
        phrase_vec_norm = phrase_vec/(np.linalg.norm(phrase_vec))
        return phrase_vec_norm
    except:
        return np.zeros([1,300])





def Get_Emoji_Data(root_directory):
    with open(root_directory + 'emoji-test.txt', 'r') as f:
        raw_txt_data = f.readlines()
    raw_emoji_data = [x for x in raw_txt_data if(x[0] != '\n' and x[0] != '#')]
    unicode_rep = []
    description = []
    k = -1
    for row in raw_emoji_data:
        k += 1
        unicode_section = row.split(';')[0]
        i = len(unicode_section) - 1
        while(i > 0 and unicode_section[i] == ' '):
            i -= 1
        unicode_rep_row = unicode_section[1:(i+1)]
       
        if (len(row.split('#')[1]) > 1):
            description_section = row.split('#')[1]
        else:
            description_section = row.split('#')[2]
        description_section_text = description_section.split(' ')[2:]
        description_section_text = ' '.join(description_section_text)
        remove_chars = ['\n', ';',':']
        for c in remove_chars:
            description_section_text = description_section_text.replace(c, '')
        
        if(description_section_text not in description):
            unicode_rep.append(unicode_rep_row)
            description.append(description_section_text)
    return [unicode_rep, description]

root_directory = '/Users/benjaminlucas/Documents/EmojiSearch/'
corpus_file = root_directory + 'crawl-300d-2M.vec'
[unicode_rep, emoji_description] = Get_Emoji_Data(root_directory)
[word_dict, word_mat] = LoadWordVecs(root_directory, 10000)

emoji_mat = GenerateEmojiMat(emoji_description, word_dict, word_mat)

test_phrase = 'experiment'
emoji_inds = FindEmoji(test_phrase, emoji_mat)
print('Search phrase: "' + test_phrase + '"\n' + 'option 1: ' + emoji_description[emoji_inds[0]] + '\noption 2:' + emoji_description[emoji_inds[1]] + '\noption 3:' + emoji_description[emoji_inds[2]])
