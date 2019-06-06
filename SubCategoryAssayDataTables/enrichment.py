import sys
import pandas as pd
import scipy.stats as stats


def enrich(my_full_table):

    # CREATE THE ENRICHMENT TABLE
    endpoint = my_full_table.columns[1]

    row_names = my_full_table.columns[2:]
    column_names = ['CT-Total','TP', 'FP', 'FN', 'TN','Balanced Accuracy', 'Odds Ratio', 'P-val', 'Inv P-val', 'Inv OR']
    enrichment_table = pd.DataFrame(index=row_names, columns=column_names, dtype=float)
    enrichment_table = enrichment_table.fillna(value=0.0)



    # FILL THE CONFUSION MATRIX
    for index, row in my_full_table.iterrows():
        if int(row[endpoint]) == 1:
            count = -1
            for i in row[my_full_table.columns[2]:]:
                i = int(i)
                count += 1
                if i == 1:
                    enrichment_table['TP'][row_names[count]] += 1
                elif i == 0:
                    enrichment_table['FN'][row_names[count]] += 1
                else:
                    print('Error')
                    sys.exit(1)
        elif int(row[endpoint]) == 0:
            count = -1
            for i in row[my_full_table.columns[2]:]:
                i = int(i)
                count += 1
                if i == 1:
                    enrichment_table['FP'][row_names[count]] += 1
                elif i == 0:
                    enrichment_table['TN'][row_names[count]] += 1
                else:
                    print('Error')
                    sys.exit(1)
        else:
            print(row[endpoint])
            print('ERROR: endpoint error')
    # CALCULATE & FILL ODDS RATIOS & FISHER'S EXACT P-VALUES

    for index, row in enrichment_table.iterrows():
        oddsratio, pvalue = stats.fisher_exact([[row['TP'], row['FP']], [row['FN'], row['TN']]], alternative='greater')
        enrichment_table.loc[index, 'P-val'] = pvalue
        enrichment_table.loc[index, 'Odds Ratio'] = oddsratio
        enrichment_table.loc[index, 'CT-Total'] = (row['TP'] + row['FP'])
        BA = (((row['TP'] / (row['TP'] + row['FP'])) + (row['TN'] / (row['TN'] + row['FN']))) / 2)
        enrichment_table.loc[index, 'Balanced Accuracy'] = float(BA)
        inv_oddsratio, inv_pvalue = stats.fisher_exact([[row['FP'], row['TP']], [row['TN'], row['FN']]],alternative='greater')
        enrichment_table.loc[index, 'Inv P-val'] =inv_pvalue
        enrichment_table.loc[index, 'Inv OR'] = inv_oddsratio


    # ROUNDS AND SETS VALUES AS INT
    # enrichment_table = enrichment_table.sort_values(by=['TP'], ascending=False)

    #enrichment_table[['Balanced Accuracy', 'Odds Ratio', 'P-val']] = enrichment_table[['Balanced Accuracy', 'Odds Ratio', 'P-val']].round(decimals=3)
    enrichment_table[['CT-Total','TP', 'FP', 'FN', 'TN']] = enrichment_table[['CT-Total','TP', 'FP', 'FN', 'TN']].astype(int)

## create flipped endpoint statistics
    return enrichment_table