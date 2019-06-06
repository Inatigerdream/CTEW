import numpy as np
import pandas as pd
import random
from sklearn.model_selection import StratifiedKFold, train_test_split, GridSearchCV
import glob

for f in glob.glob('/home/rlougee/Desktop/invitrodb_v2_burst_splits/clean_assays2/*'):
    try:
        assay_name = f.split('/')[-1]
        hit1 = pd.read_csv(f, sep='\t', index_col=0, names=['hitc'])
        hit2 = pd.read_csv('/home/rlougee/Desktop/Marks_Files/MARKS_DATA_V2/Burst_MC/split/{}'.format(assay_name), sep='\t', index_col=0)

        print(hit1.columns)
        print(hit2.head(3))

        y1 = hit1.iloc[:,0]

        # separate rows with positive hits
        hit1pos = hit1[hit1['hitc'] == 1]
        hit1neg = hit1[hit1['hitc'] == 0]

        hit2_count = len(hit2[hit2['hitc'] == 1])
        # randomly select 120 rows from hit30 pos
        def random_select(df, num_rows):
            return df.ix[random.sample(list(df.index), num_rows)]

        a = random_select(hit1pos, hit2_count)
        b = random_select(hit1pos, hit2_count)
        c = random_select(hit1pos, hit2_count)

        a.append(hit1neg).to_csv('/home/rlougee/Desktop/invitrodb_v2_burst_splits/abc_splits/{}_split_a.tsv'.format(assay_name), sep='\t', index=True)
        b.append(hit1neg).to_csv('/home/rlougee/Desktop/invitrodb_v2_burst_splits/abc_splits/{}_split_b.tsv'.format(assay_name), sep='\t', index=True)
        c.append(hit1neg).to_csv('/home/rlougee/Desktop/invitrodb_v2_burst_splits/abc_splits/{}_split_c.tsv'.format(assay_name), sep='\t', index=True)
    except: print("FAIL: {}".format(f))


