import pandas as pd
import numpy as np
import os
import glob

path = os.path.dirname(os.path.realpath(__file__))
result = glob.glob(path + "\\*.csv")

def label(path, lenpath):
    data = pd.read_csv(path, header=None)
    
    datatransform = {
        "X": data.iloc[0, :].to_numpy(),
        "Y": data.iloc[1, :].to_numpy(),
        "Z": data.iloc[2, :].to_numpy()
        }
    
    Activity = np.empty(len(datatransform["X"]))
    Activity.fill(1)
    datatransform["Label"] = Activity
    pd.DataFrame.from_dict(datatransform).to_csv(path[:-4] + 'Labeled.csv', index=False, header=False)
    

for i in result:
    label(i, len(path))