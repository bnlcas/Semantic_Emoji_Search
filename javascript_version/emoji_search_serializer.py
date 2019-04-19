"""
Created on Monday October 22 11 13:11:32 2018

@author: benjaminlucas
"""
import numpy as np
import io
import json
import MathJS_Serializer

def LoadWordVecs(corpus_file, n_words = 20000):
    data = LoadWordVecRaw(n_words, corpus_file)
    data = [row for row in data if not IsStopWord(row.split(' ')[0])]
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


def LoadWordVecRaw(n_tokens, corpus_file):
    f = open(corpus_file,'r')
    f.readline()
    f.readline() # Remove first two lines of header data
    data = []
    for i in range(n_tokens):
        data.append(f.readline())
    f.close()
    return data


def GenerateEmojiMat(emoji_description, word_dict, word_mat):
    emoji_mat = np.zeros([len(emoji_description), 300])
    for i, emoji in enumerate(emoji_description):
        vec = MakePhraseVec(emoji, word_dict, word_mat)
        emoji_mat[i,:] = vec
    return emoji_mat

def IsStopWord(word):
    stop_words = ["\"", "\\", "/", ":", ";", "-", ",", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "its", "itself", "what", "which", "who", "whom", "this", "that", "these", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "to", "so", "s", "t", "can", "will", "just", "don", "should", "now", "with",]
    return any(x == word for x in stop_words)

def MakePhraseVec(phrase, word_dict, word_mat):
    stop_chars = [':', ';', '-',',']
    for c in stop_chars:
        phrase = phrase.replace(c,' ')
    words = phrase.lower().split(' ')
    words = [w for w in words if len(w) > 1]
    words = [w for w in words if not IsStopWord(w)]
    word_inds = []
    for w in words:
        try:
            word_inds.append(word_dict[w])
        except:
            a = 1
    if(len(word_inds) > 0):
        phrase_mat = word_mat[word_inds,:]
        phrase_vec = np.sum(phrase_mat, axis=0)
        phrase_vec_norm = phrase_vec/(np.linalg.norm(phrase_vec))
        return phrase_vec_norm
    else:
        print('no words found in: ' + phrase)
        return np.zeros([1,300])


def FindEmoji(search_phrase, emoji_mat):
    search_vector = MakePhraseVec(search_phrase, word_dict, word_mat)
    similarity = np.matmul(emoji_mat, np.transpose(search_vector))
    sort_inds = np.flipud(np.argsort(similarity))
    return list(sort_inds[1:5])




def Load_Emoji_Data(emoji_data_file):
    unicode_reps = []
    hexidecimal_reps = []
    descriptions = []
    for row in raw_emoji_data:
        sections = row.split(';')
        # Get Unicode:
        if(len(sections) > 0):
            unicode_section = sections[0].strip()
            description_section = sections[1].strip()
        else:
            continue
        description = description_section.split('#')

        # Get Description
        if(len(description) > 0):
            description = description[1]
        else:
            continue

        description_components = description.split(' ')
        if(len(description_components[1]) == 1):
            hexidecimal_rep = description_components[1]
            description = ' '.join(description_components[2:])
        else:
            continue

        remove_chars = ['\n', ';',':', '-']
        for c in remove_chars:
            description = description.replace(c, ' ')
        hexidecimal_reps.append(hexidecimal_rep)
        unicode_reps.append(unicode_section)
        descriptions.append(description)
    return [unicode_reps, hexidecimal_reps, descriptions]



def SetupEmojiSearch(root_directory):
    corpus_file = root_directory + 'Corpra/crawl-300d-2M.vec'
    emoji_data_file = root_directory + 'emoji-test.txt'
    #'Corpra/glove.42B.300d.txt'
    # 'Corpra/wiki-news-300d-1M.vec'
    [unicode_rep, hexidecimal_rep, emoji_description] = Load_Emoji_Data(emoji_data_file)
    [word_dict, word_mat] = LoadWordVecs(corpus_file, 50000)
    emoji_mat = GenerateEmojiMat(emoji_description, word_dict, word_mat)
    [word_dict, word_mat] = LoadWordVecs(corpus_file, 20000)
    return [emoji_mat, word_dict, word_mat, unicode_rep, hexidecimal_rep, emoji_description]



def SerializeData():
    MathJS_Serializer.SerializeMathJS_MatrixJSON(emoji_mat, 'emoji_mat_data.js')
    MathJS_Serializer.SerializeMathJS_MatrixJSON(word_mat, 'word_mat_data.js')
    MathJS_Serializer.SerializeJS_Dictionary(word_dict, 'word_dict.js')
    MathJS_Serializer.SerializeJS_List(["\\u{" + x +"}" for x in unicode_rep], 'unicode_rep.js')
    MathJS_Serializer.SerializeJS_List(hexidecimal_rep, 'hexidecimal_rep.js')

root_directory = '/Users/benlucas/Documents/Semantic_Emoji_Search'
[emoji_mat, word_dict, word_mat, unicode_rep, hexidecimal_rep, emoji_description] = SetupEmojiSearch(root_directory)


test_phrase = 'time'
emoji_inds = FindEmoji(test_phrase, emoji_mat)
print('Search phrase: "' + test_phrase + '"\n' + 'option 1: ' + emoji_description[emoji_inds[0]] + '\noption 2:' + emoji_description[emoji_inds[1]] + '\noption 3:' + emoji_description[emoji_inds[2]])

SerializeData()
