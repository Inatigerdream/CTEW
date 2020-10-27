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
MySQL_Check_4_Updates - CLI for checking for any updates to the database 
MySQL_queries - various SQL queries
PullEnrichment - CLI to pull CTEW files out of the database
R_chemotype_script - deprecated R code
RemoveDuplicates - CLI that removes duplicate IDs from a datatable
Show_Datasets - CLI for searching all of the datasets with chemotypeenrichment data
Special_Toxprint - CLI for generating special toxprints combinations etc
SQL_toxprint - CLI for generating Toxprint fingerprints and storing them in a database
SubCategoryAssayDataTables - creates datatables for assay categories first verifies that changes have been made, then creates a new datable
ThiDivider - deprecated
ToxcastFP - CLI for creating fingerprints for compounds across assay hit data
zMisc_Code - Lot's of random stuff in here 
credentials.yml - login credentials for database connections
credentials.yml.orig - see above
requirements.txt - python install requirements

### Installation

### Basic Use

### Improvements for v2

### Disclaimer



importatdataset - CLI 
