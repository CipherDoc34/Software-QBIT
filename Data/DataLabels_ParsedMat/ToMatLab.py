# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os
import glob
import mat4py as mp
import scipy
import json

path = os.path.dirname(os.path.realpath(__file__))
result = glob.glob(path + "\\**\\*.csv")

def tonparray(path):
    data = pd.read_csv(path)
    return data.to_numpy()

def lettering(column_int):
    start_index = 1   #  it can start either at 0 or at 1
    letter = ''
    while column_int > 25 + start_index:   
        letter += chr(65 + int((column_int-start_index)/26) - 1)
        column_int = column_int - (int((column_int-start_index)/26))*26
    letter += chr(65 - start_index + (int(column_int)))
    return letter

fallarray = []
otherarray = []
fall = []
other = []

for i in result:
    if(i.find("Fall") != -1):
        fall.append(i)
    else:
        other.append(i)

for i in fall:
    fallarray.append(tonparray(i).tolist())
    
for i in other:
    otherarray.append(tonparray(i).tolist())

mp.savemat("fulldata.mat", {
        "fall": fallarray,
        "NotFall": otherarray
    })

# enumerated = enumerate(fallarray, 1)

# tempdict = dict(enumerate(fallarray, 0))

# dictionary = {}

#for i in tempdict.keys():
#    dictionary[lettering(i+1)] = tempdict[i]

# mp.savemat("data.mat", {"data":dictionary})

# with open("data.json", "w") as outfile:
#     json.dump({"data":saveform}, outfile)
    