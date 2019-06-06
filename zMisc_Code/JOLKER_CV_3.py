import numpy as np
import pandas as pd
import random
from sklearn.model_selection import StratifiedKFold, train_test_split, GridSearchCV

hit30 = pd.read_csv('/home/rlougee/Desktop/JOLKER_files/CTEW_DIO1_PhII-hit30_JOlker_20180904/CTEW_Results/CT-Enriched_Stats_DIO1_PhII-hit30_JOlker_20180904.tsv', sep='\t')
print(hit30.head())
import sys
sys.exit()
hit50 = pd.read_csv('/home/rlougee/Desktop/JOLKER_files/CTEW_DIO1_PhII-hit50_JOlker_20180904/CTEW_Results/CT-Enriched_Stats_DIO1_PhII-hit50_JOlker_20180904.tsv', sep='\t')

a = pd.read_csv('/home/rlougee/Desktop/JOLKER_files/JOLKER_CV_2/CTEW_JOlker_split_a_updated_20181211/CTEW_Results/CT-Enriched_Stats_JOlker_split_a_updated_20181211.tsv', sep='\t')
b = pd.read_csv('/home/rlougee/Desktop/JOLKER_files/JOLKER_CV_2/CTEW_JOlker_split_b_updated_20181211/CTEW_Results/CT-Enriched_Stats_JOlker_split_b_updated_20181211.tsv', sep='\t')
c = pd.read_csv('/home/rlougee/Desktop/JOLKER_files/JOLKER_CV_2/CTEW_JOlker_split_c_updated_20181211/CTEW_Results/CT-Enriched_Stats_JOlker_split_c_updated_20181211.tsv', sep='\t')
# d = pd.read_csv('/home/rlougee/Desktop/JOLKER_splits/enrichments/CTEW_JOlker_split_d_20181016/CTEW_Results/CT-Enriched_Stats_JOlker_split_d_20181016.tsv', sep='\t')
# e = pd.read_csv('/home/rlougee/Desktop/JOLKER_splits/enrichments/CTEW_JOlker_split_e_20181016/CTEW_Results/CT-Enriched_Stats_JOlker_split_e_20181016.tsv', sep='\t')

outputdf = hit30.merge(hit50, how='outer', on=['Chemotype ID'], suffixes=('_h30','_h50'))
outputdf = outputdf.merge(a, how='outer', on=['Chemotype ID'], suffixes=('','_split_A'))
outputdf = outputdf.merge(b, how='outer', on=['Chemotype ID'], suffixes=('','_split_B'))
outputdf = outputdf.merge(c, how='outer', on=['Chemotype ID'], suffixes=('','_split_C'))
# outputdf = outputdf.merge(d, how='outer', on=['Chemotype ID'], suffixes=('','_split_D'))
# outputdf = outputdf.merge(e, how='outer', on=['Chemotype ID'], suffixes=('','_split_E'))

outputdf.to_csv('/share/home/rlougee/Desktop/JOLKER_CV_complete_v3.tsv', sep='\t')

print(outputdf.head(5))