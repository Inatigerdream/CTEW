from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.session import SQLSession
import pandas as pd
import numpy as np
########################################################################################################################

# # # MAKE THE SPECIAL TOXPRINTS COMBINATIONS # # #

def mk_toxcastfp(idrow):
    # query existing toxprints
    dsi = 1449

    mysession = SQLSession(Schemas.qsar_schema).get_session()

    # pull compound ids in invitrodb
    CID1 = mysession.execute('SELECT compounds.id, mc5.aeid, compounds.dsstox_compound_id, mc5.hitc FROM invitrodb.mc5'
                                ' JOIN invitrodb.mc4 ON mc4.m4id = mc5.m4id'
                                ' JOIN invitrodb.sample ON sample.spid = mc4.spid'
                                ' JOIN ro_stg_dsstox.generic_substances ON generic_substances.id = sample.chid'
                                ' JOIN ro_stg_dsstox.generic_substance_compounds ON generic_substance_compounds.fk_generic_substance_id = generic_substances.id'
                                ' JOIN ro_stg_dsstox.compounds ON compounds.id = generic_substance_compounds.fk_compound_id')

    CID1 = pd.DataFrame(list(CID1))

    # filter out rows without a given id
    output_df = pd.merge(idrow, CID1, on=0, how='inner')

    # sort
    output_df = output_df.sort_values([output_df.columns.values[0], output_df.columns.values[1]])
    output_df = output_df.reset_index(drop=True)

    # remove -1 values replace with 0 !!!
    output_df = output_df.replace(-1, 0)

    # pivot tables per dtxcid
    output_df = pd.pivot_table(output_df, index=0, columns=1, values=3, fill_value='', aggfunc=np.sum)

    # sets correct hitcall
    # if any duplicate is a hit, fingerprint is considered a hit !!!

    output_df = output_df.apply(lambda x: [y if y=='' else (int(y) if y <= 1 else 1) for y in x])

    # not all columns are present depending on query
    # pull remaining columns and add empty columns to output_df dataframe
    full_columns = [x[0] for x in mysession.execute('SELECT assay_component_endpoint.aeid FROM invitrodb.assay_component_endpoint')]

    for x in full_columns:
        if x not in output_df.columns.values:
            output_df[x] = ''

    # output_df = output_df.sort_values(list(output_df.columns), axis=1, ascending=True)
    output_df = output_df.reindex_axis(sorted(output_df.columns), axis=1)

    return output_df

# TEST ##
# am i inputting a list just like this?
if __name__ == "__main__":
    mylist = [1030, 12344, 12390, 12392,
              12398, 12500, 12502, 12552,
              12637, 1336]
    a = mk_toxcastfp(pd.DataFrame(mylist))
    print(a.head(), '\n', a.shape)
    # a.to_csv('/home/rlougee/Desktop/test3.tsv', sep='\t')


