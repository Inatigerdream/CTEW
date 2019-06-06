import pandas as pd

from PullEnrichment.ImageMaker import imagemaker
from zMisc_Code.DATA_VISUALIZATION.doublebarplot import doublebarplot

# import burst and nonburst results
burst = pd.read_csv('/home/rlougee/Desktop/primary_data/burst.tsv', sep='\t')
nonburst = pd.read_csv('/home/rlougee/Desktop/primary_data/nonburst.tsv', sep='\t')

# import assay category data
cats = pd.read_csv('/home/rlougee/Desktop/primary_data/categories_table_invitrodb_v2.tsv', sep='\t')

# merge cats table to others
burst_full = pd.merge(cats, burst, how='right', left_on='assay_component_endpoint_name', right_on='name')
nonburst_full = pd.merge(cats, nonburst, how='right', left_on='assay_component_endpoint_name', right_on='name')

# print(burst.shape, burst_full.shape, nonburst.shape, nonburst_full.shape)
# print(cats.columns[2:])
# sys.exit(0)

for x in []:#cats.columns[2:]:
    for i in cats[x].unique():
        try:
            print(x, i)
            b = burst_full.loc[burst_full[x] == i]
            nb = nonburst_full.loc[nonburst_full[x] == i]
            # print(b)
            # print(nb)

            b_VC = b['descriptors_name'].value_counts()
            nb_VC = nb['descriptors_name'].value_counts()

            full_VC = pd.merge(pd.DataFrame(nb_VC), pd.DataFrame(b_VC), how='outer', left_index=True, right_index=True)
            full_VC = full_VC.fillna(value=0).sort_values(by=['descriptors_name_x', 'descriptors_name_y'], axis=0, ascending=False)

            # full_VC.to_csv('/home/rlougee/Desktop/fullVC_{}.tsv'.format(i), sep='\t')

            # make barplot for enriched CTs
            doublebarplot(full_VC['descriptors_name_x'], full_VC['descriptors_name_y'], n=200, title='Significant CTs Burst v Non Assay Category:{}={}'.format(x, i), save='', label1='nonburst', label2='burst',  color2='magenta')
            # print([x.upper() for x in full_VC.index[0:20]])
            # make images for enriched CTs
            imagemaker(pd.DataFrame(full_VC.index, columns=['Chemotype ID']), "top_CT_{}:{}".format(x, i), '/home/rlougee/Desktop/figures_ACS_2/assay_cat_pics_full_b/')


        except:
            print('fail')
            pass
        # print(full_VC)
        # sys.exit(0)