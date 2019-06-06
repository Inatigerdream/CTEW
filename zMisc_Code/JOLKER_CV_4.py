import numpy as np
import pandas as pd
import random
from sklearn.model_selection import StratifiedKFold, train_test_split, GridSearchCV
import numpy as np
import pandas as pd
import random
from sklearn.model_selection import StratifiedKFold, train_test_split, GridSearchCV
import glob
import sys

hit30 = pd.read_csv('/home/rlougee/Desktop/JOLKER_files/DIO1_PhII-hit30_JOlker.tsv', sep='\t', names=['DTXCID','hitc'], skiprows=[0])#, index_col=0)
hit50 = pd.read_csv('/home/rlougee/Desktop/JOLKER_files/DIO1_PhII-hit50_JOlker.tsv', sep='\t')#, index_col=0)

def random_select_hits(df, number):
    hitpos = df[df['hitc'] == 1]
    print(len(hitpos))
    hitneg = df[df['hitc'] == 0]
    hitpos = hitpos.sample(frac=1).reset_index(drop=True)
    hitpos.loc[number:, 'hitc'] = hitpos.loc[number:, 'hitc'].map({1: 0})
    output = hitpos.append(hitneg)
    # print(df.shape, output.shape)
    # print(output)
    return output
print(hit30)
for i in ['a', 'b', 'c']:
    random_select_hits(hit30, 120).to_csv('/share/home/rlougee/Desktop/JOLKER_files/splits/JOlker_split_{}.tsv'.format(i), sep='\t', index=False)