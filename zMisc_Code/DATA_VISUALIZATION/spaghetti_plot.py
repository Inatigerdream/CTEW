import matplotlib.pyplot as plt
import pandas as pd
import sys

#make ordered txp list
txplist=[]
for i in range(0,729):
    txplist.append('Txp-{}'.format(i+1))
# print(len(txplist), txplist)

fig, ax = plt.subplots()

# function to plot spaghetti plot
def spaghetti_plot(data1, data2):
    # print(data1['descriptors_name'])
    # print(len(data2))




    # add labels


    ax.plot(data1['descriptors_name'], color='cyan', linewidth=1, alpha=.5, label='Burst')
    ax.plot( data2['descriptors_name'], color='pink', linewidth=1, alpha=.5, label='Non-Burst')

    # plt.show()

# test
if __name__ =='__main__':
    # import burst and nonburst results
    burst = pd.read_csv('/home/rlougee/Desktop/primary_data/burst.tsv', sep='\t')
    nonburst = pd.read_csv('/home/rlougee/Desktop/primary_data/nonburst.tsv', sep='\t')

    # import assay category data
    cats = pd.read_csv('/home/rlougee/Desktop/primary_data/categories_table_invitrodb_v2.tsv', sep='\t')

    # merge cats table to others
    burst_full = pd.merge(cats, burst, how='right', left_on='assay_component_endpoint_name', right_on='name')
    nonburst_full = pd.merge(cats, nonburst, how='right', left_on='assay_component_endpoint_name', right_on='name')

    for x in cats.columns[2:]:
        for i in cats[x].unique():
            try:
                # print(x, i)
                b = burst_full.loc[burst_full[x] == i]
                nb = nonburst_full.loc[nonburst_full[x] == i]
                # print(b)
                # print(nb)

                b_VC = b['descriptors_name'].value_counts()
                nb_VC = nb['descriptors_name'].value_counts()


                b_VC = pd.merge(pd.DataFrame(txplist), pd.DataFrame(b_VC), how='outer', left_on=0,
                                   right_index=True)
                b_VC = b_VC.fillna(value=0)

                nb_VC = pd.merge(pd.DataFrame(txplist), pd.DataFrame(nb_VC), how='outer', left_on=0,
                                right_index=True)
                nb_VC = nb_VC.fillna(value=0)
                # print(0)
                # print(pd.DataFrame(txplist))
                # print(b_VC)
                # print(b_VC)
                # print(nb_VC[['0', 'descriptors_name']])
                # sys.exit(1)

                ### PLOT
                spaghetti_plot(b_VC, nb_VC)

            except:
                # fail message
                print('fail')
                pass
    ax.set_ylabel('Counts', fontsize=14, fontweight='bold')
    ax.set_title('blabla', fontsize=14, fontweight='bold')
    ax.set_xticks(list(range(0,729, 20)))
    ax.set_xticklabels(txplist[0::20], rotation='vertical', fontweight='bold')
    ax.set_facecolor('.98')
    ax.grid(color='.9', zorder=0)
    ax.set_ylim(0,50)
    ax.legend()

    plt.show()
