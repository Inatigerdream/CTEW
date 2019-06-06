from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.session import SQLSession
import sys
import pandas as pd
from colorama import init, Fore
# initilize colorama colored CLI text
init(autoreset=True)

# returns a list of DTXCIDs that need to be created

def check(f):
    mysession = SQLSession(Schemas.qsar_schema).get_session()

    # pull compound ids in invitrodb
    CID1 = mysession.execute('SELECT compounds.id FROM invitrodb.mc5'
                                ' JOIN invitrodb.mc4 ON mc4.m4id = mc5.m4id'
                                ' JOIN invitrodb.sample ON sample.spid = mc4.spid'
                                ' JOIN ro_stg_dsstox.generic_substances ON generic_substances.id = sample.chid'
                                ' JOIN ro_stg_dsstox.generic_substance_compounds ON generic_substance_compounds.fk_generic_substance_id = generic_substances.id'
                                ' JOIN ro_stg_dsstox.compounds ON compounds.id = generic_substance_compounds.fk_compound_id')

    CID1 = set([x[0] for x in list(CID1)])

    # pull compound ids in compound_descriptor_sets
    CID2 = mysession.query(CompoundDescriptorSets.efk_dsstox_compound_id) \
        .filter(CompoundDescriptorSets.fk_descriptor_set_id == '1449')

    CID2 = [x[0] for x in list(CID2)]

# # # CHECKS FOR ID AND ToxcastFPs IN QSAR.COMPOUND_DESCRIPTOR_SETS # # #
# # # MAKE A LIST OF THE DSSTOX.COMPOUNDS.ID THAT DON'T HAVE SPECIAL ToxcastFPs # # #

    CID3 = list(CID1-set(CID2))

# check dataframes
    # print("\n set CID1:", len(set(CID1)))
    # print("\n set CID2:", len(set(CID2)))
    # print("\n CID3", len(CID3), CID3)
    # print("\n CID3df", pd.DataFrame(CID3).head())
    # print("\n CID1df", pd.DataFrame(list(CID1)).head())

    # # # # IF QSAR.COMPOUND_DESCRIPTOR_SETS IS MISSING EITHER THEN GENERATE ToxcastFPs FOR THIS COMPOUND # # #
    if CID3 == [] and f is False:
        print(Fore.RED + 'SQL query is empty: All ToxcastFP available or no DTXCIDs')
        sys.exit(0)

    elif CID3 == [] and f is True:
        return pd.DataFrame([]), pd.DataFrame(CID1)

    else:
        return pd.DataFrame(CID3), pd.DataFrame(CID1)


########################################################################################################################
########################################################################################################################

# # TEST #
#
# if __name__=='__main__':
#     print(check(True))

if __name__=='__main__':
    print(check(False))

########################################################################################################################
