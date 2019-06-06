import numpy as np
import pandas as pd
import random
from sklearn.model_selection import StratifiedKFold, train_test_split, GridSearchCV
import glob
import sys


def random_select_hits(df, number):
    hitpos = df[df['hitc'] == 1]
    hitneg = df[df['hitc'] == 0]
    hitpos = hitpos.sample(frac=1).reset_index(drop=True)
    hitpos.loc[number:, 'hitc'] = hitpos.loc[number:, 'hitc'].map({1: 0})
    output = hitpos.append(hitneg)
    # print(df.shape, output.shape)
    # print(output)
    return output


for f in glob.glob('/home/rlougee/Desktop/invitrodb_v2_burst_splits/clean_assays2/*'):
    try:
        print(f)
        assay_name = f.split('/')[-1]
        hit1 = pd.read_csv(f, sep='\t',  names=['DTXCID', 'hitc'])#index_col=0,
        # import burst to see how many hits are in burst
        hit2 = pd.read_csv('/home/rlougee/Desktop/Marks_Files/MARKS_DATA_V2/Burst_MC/split/{}'.format(assay_name), sep='\t',
                           index_col=0)
        hit2_count = len(hit2[hit2['hitc'] == 1])
        # make 3 splits
        for letter in ['a', 'b', 'c']:
            random_select_hits(hit1, hit2_count).to_csv('/home/rlougee/Desktop/invitrodb_v2_burst_splits/abc_splits/{}_split_{}.tsv'.format(assay_name, letter), sep='\t', index=False)
    except:
        print('FAIL: {}'.format(f))
