import pandas as pd
import matplotlib.pyplot as plt

# MAKE CORRELATION MATRICES FOR TOXPRINTS

a = pd.read_csv('/home/rlougee/Desktop/primary_data/Cytotoxicity_CID_HITC_invitrodbv2_fullfp_2.tsv', sep='\t')

# drop nan columns and columns only containing 0
a = a.dropna(axis=1)
a = a.loc[:, (a != 0).any(axis=0)]

print(a)

c = a.corr(method='spearman') # use spearman for correlations of discrete values
c.to_csv('/home/rlougee/Desktop/cytotoxicity_assays_correlation_matrix.tsv', sep='\t')

plt.matshow(a.corr())
plt.show()

