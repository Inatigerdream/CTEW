# CTEW
## Chemotype-Enrichment Workflow

#### see NCCT KB for more information

This code contains multiple Command-Line Interfaces (CLI)s for generating Chemotype-Enrichment Workflow (CTEW) data. This CLI integrates directly with the United States Environmental Protection Agency's (USEPA) Center for Computational Toxicology and Exposure (CCTE) databases. The CTEW requires a set of chemical ids (DTXCID, DTXSID, and casrn can currently be used), and assay hitcalls as a binary variable. The CLI tools herein, are used to store the data in the database, generate enrichment statistics, and pull cleaned enrichment data out of the database. Additional CLI's were made for custom fingerprint types, and data preparation.

## Components

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
TheDivider - deprecated  
ToxcastFP - CLI for creating fingerprints for compounds across assay hit data  
zMisc_Code - Lot's of random stuff in here  
credentials.yml - login credentials for database connections  
credentials.yml.orig - see above  
requirements.txt - python install requirements  

## Installation
### 1. Download the CTEW repo  
### 2. In your python virtual environment of choosing install the requirements  
```console
user@computer:~$ cd path/to/chemotypescripts  
user@computer:~$ pip install -r requirements.txt  
# also install this:
user@computer:~$ pip install mysql-client==2.1.7  
```
### 3. Install each individual CLI
```console
user@computer:~$ cd path/to/chemotypescripts/Chemical_ID_Convert  
user@computer:~$ pip install -e .  
# test with -h:
user@computer:~$ chemidconvert -h  
# this will show usage syntax and flag options if succesfully installed
```
### These are the most important directories for CLI installation  
### repeat the commands at the beginning of step 3 for each of these directories  
chemotypescripts/Chemical_ID_Convert  
chemotypescripts/ImportDataTabletoMySQL  
chemotypescripts/Enrichment_MySQL  
chemotypescripts/FillFingerprints  
chemotypescripts/PullEnrichment   
chemotypescripts/Show_Datasets  
chemotypescripts/SQL_toxprint  

### 5. Add your username and password to the credentials.yml file  

## Basic Use of CTEW
#### NCCT KB has a better explaination
### 1. Prepare a .tsv file with (casrn, DTXCID, or DTXSID) in the first column and the second column should contain binary assay hitcalls (0,1)
MyExampleFile.tsv:  
| Chemical ID | Assay Hitcalls |  
|-------------|----------------|  
|  DTXSID101  |        0       |  
|  DTXSID202  |        1       |  
|  DTXSID303  |        1       |   

### 2. Before importing the file into the database the Chemical IDs must be changed to DTXCID

To just convert the IDs in your file use chemicalidconvert:

```console
user@computer:~$ cat MyExampleFile.tsv | chemicalidconvert DTXSID DTXCID -e > MyExampleFile_DTXCID.tsv
```
### 3. If your file contains a header it can be removed using:

```console
user@computer:~$ cat MyExampleFile_DTXCID.tsv | tail -n +2 > MyExampleFile_DTXCID.tsv
```

### 4. Remove duplicates

```console
user@computer:~$ cat MyExampleFile_DTXCID.tsv | removeduplicates --anyhit > MyExampleFile_DTXCID.tsv
```

### 5. Add the file to the database

```console
user@computer:~$ cat MyExampleFile_DTXCID.tsv | datatable2mysl "MyExampleFile_v1_RLOUGEE" "rlougee"
```

### 6. You can see if you datatable has been added using:
```console
user@computer:~$ showdatasets
```

### 7. Create enrichment data using:
```console
user@computer:~$ enrich_mysql
```

### 8. Once this is complete you can pull enrichment data using:
```console
user@computer:~$ pullenrichment "MyExampleFile_v1_RLOUGEE"
```

## Improvements for v2
### 1. Put all of this into one CLI
### 2. Require user ID & password upon installation & verify (dataminer is getting removed)
### 3. Remove deprecated code
### 4. Make seperate repos for zMisc_code etc.
### 5. Update requirements if possible (Hopefully this will improve installation)


## Disclaimer

disclaimed
