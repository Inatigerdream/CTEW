import pandas as pd
import glob


for f in glob.glob('/home/rlougee/Desktop/Marks_Files/Marks_Files_6_22_2018/*'):
    a = pd.read_csv(f)
    b = f.split('.csv')[0]
    b = b.split('/')[-1]
    # print(b)
    a.to_csv('/home/rlougee/Desktop/Marks_Files/tsv_6_22_2018/{}.tsv'.format(b), sep='\t', index=False)