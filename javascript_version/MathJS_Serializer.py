#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 12:38:22 2018

@author: benjaminlucas
"""
import io
import numpy as np

def SerializeMathJS_MatrixJSON(mat, json_file, rounding = 5):
    n_rows = np.size(mat,0)
    n_cols = np.size(mat,1)
    mat_json_string = json_file.split('.')[0] + "={\"mathjs\":\"DenseMatrix\",\"data\":["
    for i in range(n_rows):
        row_string = "["
        for j in range(n_cols):
            if(j < (n_cols - 1)):
                row_string += str(np.round(mat[i,j],rounding)) + ","
            else:
                row_string += str(np.round(mat[i,j],rounding)) + "]"
            
        if(i < (n_rows - 1)):
            mat_json_string += row_string + ","
        else:
            mat_json_string += row_string
        
    mat_json_string += "],\"size\":[" + str(n_rows) + "," + str(n_cols) + "]}"
    with open(json_file, 'w') as f:
        f.write(mat_json_string)


def SerializeJS_Dictionary(word_dict, json_file):
    dict_string = json_file.split('.')[0] + "={";
    i = 0
    n = len(word_dict.items())
    for key, value in word_dict.items():
        dict_string += "\"" + key + "\":" + str(value);
        if i < (n - 1):
            dict_string += ","
        else:
            dict_string += "};" 
        i += 1
    with open(json_file, 'w') as f:
        f.write(dict_string)
                                  
def SerializeJS_List(target_list, filename):
    list_string = filename.split('.')[0] + "=["
    for i, x in enumerate(target_list):
        list_string += "\"" + str(x) + "\""
        if(i < (len(target_list)-1)):
            list_string += ","
        else:
            list_string += "];"
    with open(filename, 'w') as f:
        f.write(list_string)
        
