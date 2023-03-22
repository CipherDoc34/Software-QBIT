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

def todataarray(path):
    data = pd.read_csv(path)
    return data


X = []
Y = []
Z = []
Labels = []

for i in result:
    if (i == "C:\\Users\\Keshav\\Downloads\\DataLabels\\Jumping\\Person10-Jumping-Trial2.csv"):
        continue
    X.extend(todataarray(i).iloc[:, 0])
    Y.extend(todataarray(i).iloc[:, 1])
    Z.extend(todataarray(i).iloc[:, 2])
    Labels.extend(todataarray(i).iloc[:, 3])
    

df = pd.DataFrame.from_dict({"X": X, "Y":Y, "Z":Z, "label":Labels}, orient='columns')
df.dropna(axis=0, how="all", inplace=True)

df.to_csv("data.csv", index=False, header=True)