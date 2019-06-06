from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.dsstox.compounds import Compounds
from database.database_schemas import Schemas
from database.session import SQLSession

mysession = SQLSession(Schemas.qsar_schema).get_session()

x_aeid = 926

query3 = mysession.query(Compounds.dsstox_compound_id, CompoundDescriptorSets.descriptor_string_tsv) \
    .join(CompoundDescriptorSets, Compounds.id == CompoundDescriptorSets.efk_dsstox_compound_id) \
    .filter(CompoundDescriptorSets.fk_descriptor_set_id == int(1445))
    # .filter(Compounds.dsstox_compound_id.in_(str(new_df.iloc[0]))) \


print(list(query3))