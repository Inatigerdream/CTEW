# CTEW
Chemotype-Enrichment Workflow

This code contains multiple Command-Line Interfaces (CLI)s for generating Chemotype-Enrichment Workflow (CTEW) data. This CLI integrates directly with the United States Environmental Protection Agency's (USEPA) Center for Computational Toxicology and Exposure (CCTE) databases. The CTEW requires a set of chemical ids (DTXCID, DTXSID, and casrn can currently be used), and assay hitcalls as a binary variable. The CLI tools herein, are used to store the data in the database, generate enrichment statistics, and pull cleaned enrichment data out of the database. Additional CLI's were made for custom fingerprint types, and data preparation.

### Components
database - database files for establishing connections
Chemical_ID_Convert - CLI for converting various chemical IDs (DTXSID, DTXCID, casrn)
DTXSIDtoDTXCID - deprecated version of Chemical_ID_Convert
Enrichment_MySQL - CLI deprecated? for generating Chemotype-Enrichments
Enrichment_Table_Generator - deprecated CLI for creating Chemotype Enrichments without a database connection
Enrichment_to_MySQL - CLI deprecated? for generating Chemotype-Enrichments
FillFingerprints - CLI for pulling fingerprint sets from the database
fingerprint_combination_generator - CLI for looking at pairwise combinations of fingerprint bits
ImportDataTabletoMySQL - CLI for importing raw assay hitcall data into the database
MySQL_Check_4_Updates - 
MySQL_queries - 
PullEnrichment - 
R_chemotype_script - 
RemoveDuplicates - 
Show_Datasets - 
Special_Toxprint - 
SQL_toxprint - 
SubCategoryAssayDataTables - 
ThiDivider -
ToxcastFP - 
zMisc_Code - 
.gitignore - 
credentials.yml - login credentials for database connections
credentials.yml.orig - idk?
requirements.txt - python install requirements

### Installation

### Basic Use

### Improvements for v2

### Disclaimer



importatdataset - CLI 
