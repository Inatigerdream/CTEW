import subprocess as subp
import pandas as pd
import numpy as np

from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.session import SQLSession


########################################################################################################################
# take a list of ddstox_compound_id and generate fingerprint files for them

def mktoxprints(dsstox_id_list):
    mysession = SQLSession(Schemas.dsstox_schema).get_session()
    mydata = mysession.query(Compounds.dsstox_compound_id, Compounds.smiles)#.filter(Compounds.dsstox_compound_id.in_(dsstox_id_list))
    df = pd.DataFrame(list(mydata))
    # filter is too big need to merge instead
    idframe = pd.DataFrame(list(set(dsstox_id_list)), columns=['dsstox_compound_id'])
    df = pd.merge(idframe, df, on='dsstox_compound_id', how='left')
    print(len(dsstox_id_list), len(list(df['dsstox_compound_id'])))

    number_per_file = 50000
    files_so_far = 0
    ix = 0
    file_path = "/home/rlougee/Desktop/tmptmp{0}.smi"
    out_file = open(file_path.format(files_so_far), 'w')
    file_list = [file_path.format(files_so_far)]
    for index, row in df.iterrows():
        #handle null values
        if row['smiles'] == None:
            row['smiles'] = ''
        if ix % number_per_file == 0 and ix > 0:
            out_file.close()
            files_so_far += 1
            out_file = open(file_path.format(files_so_far), 'w')
            file_list.append(file_path.format(files_so_far))
        smile_file = row['smiles'] + "\t" + row['dsstox_compound_id'] + "\n"
        ix += 1
        out_file.write(smile_file)
    out_file.close()
    ## generate fingerprints
    ### FOR DEBUGGING: AN ACTUAL SMILEY FACE ☻ IS USED IN THIS FILE
    ### this is only used in BASH commands and IS necessary
    ### -L is a flag that identifies a file separator and most characters break the command. Also, multiple characters in a row don't work
    bashstring = ''
    for file in file_list:
        bashstring += "{0}{1}".format(str(file), str('☻'))
    command = '/opt/CORINA_Symphony/CORINA_Symphony_14698/bin/moses -N -L ☻ symphony batch -i {0} -o /share/home/rlougee/Desktop/results.tsv descriptors -f /opt/CORINA_Symphony/CORINA_Symphony_14698/content/symphony/toxprint_V2.0.xml'.format(bashstring)
    a = subp.Popen(command, shell=True)
    a.communicate()
    #import the toxprint file
    toxprintdf = pd.DataFrame.from_csv('/share/home/rlougee/Desktop/results.tsv', sep='\t')

    #handle bad smiles
    # smiles renamed
    drop_list = []
    for index, row in toxprintdf.iterrows():
        if row['M_CORINA_SYMPHONY_ERRORS_[STRING]'] != 'No errors':
            drop_list.append(index)
        elif len(index) <= 6:
            drop_list.append(index)
        elif index[0:6] != 'DTXCID':
            drop_list.append(index)

    # drop bad rows
    toxprintdf = toxprintdf.drop(drop_list)

    # remove extra columns
    toxprintdf.drop('M_COMPOUND_HISTORY_[STRING]', axis=1, inplace=True)
    toxprintdf.drop('M_CORINA_SYMPHONY_ERRORS_[STRING]', axis=1, inplace=True)

    # remove temporary files
    b = subp.Popen('rm /share/home/rlougee/Desktop/tmptmp*.smi', shell=True)
    b.communicate()
    c = subp.Popen('rm /share/home/rlougee/Desktop/results.tsv', shell=True)
    c.communicate()

    return toxprintdf

########################################################################################################################

# # # TEST
# if __name__ == '__main__':
#     session = SQLSession(Schemas.dsstox_schema).get_session()
#     compounds = session.query(Compounds.dsstox_compound_id).limit(30)
#     user_list = [x[0] for x in compounds]
#
#     print(mktoxprints(user_list))

#######################################################################################################################
