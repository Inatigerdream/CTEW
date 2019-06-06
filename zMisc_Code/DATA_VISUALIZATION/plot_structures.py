import pandas as pd
import sys
import matplotlib.pyplot as plt
from functools import reduce
import pubchempy

# look for specific structures based on fingerprints

#import and drop bad columns
invitrodbv2_fp = pd.read_csv('/home/rlougee/Desktop/primary_data/invitrodbv2_fullfp.tsv', sep='\t')
invitrodbv2_fp = invitrodbv2_fp.dropna(axis=1)


def smile_from_txp(txplist):
    str = """invitrodbv2_fp["""
    for i in txplist:
        str += "(invitrodbv2_fp['{}']==1)&".format(i)
        # print(str)
    str = str[:-1] + ']'
    return eval(str)

# print(invitrodbv2_fp.columns)
# print(smile_from_txp(['Txp-123', 'Txp-124']).columns)
for n, i in enumerate(smile_from_txp(['Txp-338'])['smiles']):
    pubchempy.download('png', '/home/rlougee/Desktop/CID_pix/{}.png'.format(n), i, 'smiles' )
