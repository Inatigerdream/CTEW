import pandas as pd

fast = pd.read_csv('/home/rlougee/Desktop/fastfilltest.tsv', sep='\t').iloc[:,2:6]
slow = pd.read_csv('/home/rlougee/Desktop/slowfilltest.tsv', sep='\t').iloc[:,2:6]

# print(slow)
for i in (fast != slow).any(1):
    if i == True:
        print(i)