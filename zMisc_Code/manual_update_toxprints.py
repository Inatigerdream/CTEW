import pandas as pd

a = pd.read_csv('/share/home/rlougee/Desktop/CID_for_updating.tsv',sep='\t', header=None)
a = list(a[0])
print(len(a), a[0:10])

from Toxprint_generator import mktoxprints
from Toxprint_force_update import update_toxprint_database

b = mktoxprints(a)
print(b.shape)
print(1)
update_toxprint_database(b)
print(2)