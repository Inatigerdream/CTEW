import glob
import sys
import pandas as pd

# create the final output table
output_table = pd.DataFrame(columns=['Error rate', 'Accuracy', 'Sensitivity', 'Specificity', 'False positive rate', 'Error rate on train set', 'Accuracy on train set', 'Error rate on test set', 'Accuracy on test set', 'Performance train', 'Performance test', 'parameters'])

list = []

for i in glob.glob('/home/rlougee/Desktop/xgb_results/*'):
    # print(i)
    aeid = i.split('/')[-1]

    # open file
    f = open('{}/{}_output.txt'.format(i,aeid), 'r')
    lines = f.readlines()
    f.close()
    check = 1

    # print(aeid)
    #check for FAILURE
    for line in lines[-3:]:
        a = line[0:8]
        if a == 'FAILURE: {}'.format(aeid):
            list.append(int(aeid))
            output_table = output_table.append(pd.DataFrame([[ '','','','','','','','','','','', '']], columns=['Error rate', 'Accuracy', 'Sensitivity', 'Specificity', 'False positive rate', 'Error rate on train set', 'Accuracy on train set', 'Error rate on test set', 'Accuracy on test set', 'Performance train', 'Performance test', 'parameters'], index=[aeid]))
            check = 0
            continue
    if check == 1:
        output_table = output_table.append(pd.DataFrame([[ '', '', '', '', '', '', '', '', '', '', '', '']],
                                                    columns=['Error rate', 'Accuracy',
                                                             'Sensitivity', 'Specificity', 'False positive rate',
                                                             'Error rate on train set', 'Accuracy on train set',
                                                             'Error rate on test set', 'Accuracy on test set',
                                                             'Performance train', 'Performance test',
                                                             'parameters'], index=[aeid]))

        # collect stats
        for line in lines[-12:]:
            a = line.split(':')[0]
            b = line.split(':')[-1].rstrip('\n')
            # print(a, line)
            if a == "Performance train ":
                output_table['Performance train'][aeid] = b
                # print(1, b)
            elif a == 'Performance test ':
                output_table['Performance test'][aeid] = b
                # print(2, b)
            elif a == 'Error rate  ':
                output_table['Error rate'][aeid] = b
                # print(3, b)
            elif a == 'Accuracy  ':
                output_table['Accuracy'][aeid] = b
                # print(4, b)
            elif a == 'Sensitivity  ':
                output_table['Sensitivity'][aeid] = b
                # print(5, b)
            elif a == 'Specificity  ':
                output_table['Specificity'][aeid] = b
                # print(6, b)
            elif a == 'False positive rate  ':
                output_table['False positive rate'][aeid] = b
                # print(7, b)
            elif a == 'Error rate  on train set ':
                output_table['Error rate on train set'][aeid] = b
                # print(8, b)
            elif a == 'Accuracy  on train set  ':
                output_table['Accuracy on train set'][aeid] = b
                # print(9, b)
            elif a == 'Error rate  on test set ':
                output_table['Error rate on test set'][aeid] = b
                # print(10, b)
            elif a == 'Accuracy  on test set  ':
                output_table['Accuracy on test set'][aeid] = b
                # print(11, b)
            # elif a == '{"booster"':
            #     output_table['parameters'][aeid] = line
                # print(12, line)
            # print(output_table.head())
            # sys.exit(1)

        # elif a ==
    # sys.exit(0)
    # for i, line in enumerate(lines):
output_table.to_csv('/home/rlougee/Desktop/XGB_model_results_full.tsv', sep='\t')
# print(sorted(list))