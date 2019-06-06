from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.session import SQLSession
import sys
import pandas as pd
import subprocess as subp
import glob

# make a dataframe to fill
output_df = pd.DataFrame(columns = ['Assay', 'Balanced Accuracy'])

# calculate stats and add to file
for x in glob.glob('/share/home/rlougee/Desktop/invitrodb_v2_enrichments/*', recursive=False):
     try:
        # print(d)
        y = x.split('/')[-1].split('_', 1)[-1]
        df = pd.read_csv(x + '/CTEW_Results/CT-Enriched_Stats_'+y+'.tsv', sep='\t')
        # print(y, df['Balanced Accuracy'].tail(1))
        # print(df.tail(1))
        df['Assay'] = y
        output_df = output_df.append(df.tail(1))
     except:
         # pass
         # print(x)
         y = x.split('/')[-1].split('_', 1)[-1]
         output_df = output_df.append(pd.DataFrame([[y]], columns=['Assay']), ignore_index=True)
         pass

print(output_df)
# export file
output_df.to_csv('/home/rlougee/Desktop/invitrodb2_percent_coverage.tsv', sep='\t', index=False)

# print(datasets)

