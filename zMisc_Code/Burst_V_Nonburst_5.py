import pandas as pd

from zMisc_Code.DATA_VISUALIZATION.doublebarplot import doublebarplot

# look at p-value differences of features between burst and non-burst assay results

burst = pd.read_csv('/home/rlougee/Desktop/primary_data/burst.tsv', sep='\t')
nonburst = pd.read_csv('/home/rlougee/Desktop/primary_data/nonburst.tsv', sep='\t')

# loop creates tables for specific assays
for i in burst['name'].unique():
    print(i)

    temp = pd.merge(burst[burst['name'] == i], nonburst[nonburst['name']==i], left_on=['name', 'descriptors_name'], right_on=['name', 'descriptors_name'], how='outer')
    print(temp[['descriptors_name','OR_x', 'OR_y']])
    # sys.exit(1)


    doublebarplot(temp['OR_x'], temp['OR_y'], xlabel=temp['descriptors_name'], n=200, title='Significant CTs Burst v Non-Burst {}'.format(i), label1='burst', label2='nonburst', color2='magenta', barval=False, save='/home/rlougee/Desktop/individual_assay_barplots/{}_barplot.jpg'.format(i) )


    # sys.exit(0)