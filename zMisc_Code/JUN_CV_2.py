import numpy as np
import pandas as pd
import random
from sklearn.model_selection import StratifiedKFold, train_test_split, GridSearchCV

hit1 = pd.read_csv('/home/rlougee/Desktop/JUN_FILES/JUN_CV/CTEW_NIS_ph1,2_hit1_rev4_20180801/CTEW_Results/CT-Enriched_Stats_NIS_ph1,2_hit1_rev4_20180801.tsv', sep='\t')
hit2 = pd.read_csv('/home/rlougee/Desktop/JUN_FILES/JUN_CV/CTEW_NIS_ph1,2_v2_hitcall2_rev3_20180731/CTEW_Results/CT-Enriched_Stats_NIS_ph1,2_v2_hitcall2_rev3_20180731.tsv', sep='\t')

a = pd.read_csv('/home/rlougee/Desktop/JUN_FILES/JUN_CV/CV_results_2/CTEW_JUN_CV_split_a_updated_20181211/CTEW_Results/CT-Enriched_Stats_JUN_CV_split_a_updated_20181211.tsv', sep='\t')
b = pd.read_csv('/home/rlougee/Desktop/JUN_FILES/JUN_CV/CV_results_2/CTEW_JUN_CV_split_b_updated_20181211/CTEW_Results/CT-Enriched_Stats_JUN_CV_split_b_updated_20181211.tsv', sep='\t')
c = pd.read_csv('/home/rlougee/Desktop/JUN_FILES/JUN_CV/CV_results_2/CTEW_JUN_CV_split_c_updated_20181211/CTEW_Results/CT-Enriched_Stats_JUN_CV_split_c_updated_20181211.tsv', sep='\t')
# d = pd.read_csv('/home/rlougee/Desktop/JUN_CV/CV_results/CTEW_JUN_CV_split_d_20181115/CTEW_Results/CT-Enriched_Stats_JUN_CV_split_d_20181115.tsv', sep='\t')
# e = pd.read_csv('/home/rlougee/Desktop/JUN_CV/CV_results/CTEW_JUN_CV_split_e_20181115/CTEW_Results/CT-Enriched_Stats_JUN_CV_split_e_20181115.tsv', sep='\t')

outputdf = hit1.merge(hit2, how='outer', on=['Chemotype ID'], suffixes=('','_h2'))

outputdf = outputdf.merge(a, how='outer', on=['Chemotype ID'], suffixes=('','_split_A'))
outputdf = outputdf.merge(b, how='outer', on=['Chemotype ID'], suffixes=('','_split_B'))
outputdf = outputdf.merge(c, how='outer', on=['Chemotype ID'], suffixes=('','_split_C'))
# outputdf = outputdf.merge(d, how='outer', on=['Chemotype ID'], suffixes=('','_split_D'))
# outputdf = outputdf.merge(e, how='outer', on=['Chemotype ID'], suffixes=('','_split_E'))

outputdf.to_csv('/share/home/rlougee/Desktop/JUN_CV_complete_2.tsv', sep='\t')

print(outputdf.head(5))