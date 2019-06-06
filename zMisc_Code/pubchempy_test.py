import pubchempy as pcp
from Bio import Entrez
import time
import pprint
# from PIL import image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import sys
from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.session import SQLSession
import pandas as pd

# # # THIS CODE TAKES A SMILES FOR A CHEMICAL SUBSTRUCUTRE AND RETURNS INFO FROM PAPERS CONTAINING THIS SUBSTRUCTURE # # #

# # query descriptor strings and ids
# mysession = SQLSession(Schemas.qsar_schema).get_session()
#
# query0 = mysession.execute('SELECT indigo_inchi, descriptor_string_tsv FROM sbox_rlougee_qsar.compound_descriptor_sets JOIN ro_stg_dsstox.compounds ON sbox_rlougee_qsar.compound_descriptor_sets.efk_dsstox_compound_id = ro_stg_dsstox.compounds.id WHERE sbox_rlougee_qsar.compound_descriptor_sets.fk_descriptor_set_id = 1445')
#
# query0 = pd.DataFrame(list(query0))
# print(query0.shape)
# query0 = pd.merge(query0, query0[1].str.split('\t', expand=True) ,left_index=True, right_index=True)
# print(query0.shape)
#
# query0.to_csv('/home/rlougee/Desktop/toxprint_pubmed.tsv', sep='\t', index=False)
# sys.exit(0)

# import table containing toxprints and chemical IDs
mydf = pd.read_csv('/home/rlougee/Desktop/toxprint_pubmed.tsv', sep='\t')
mydf = mydf.drop(['1_x'], axis=1)
print(mydf.head(5))
mydf = mydf.rename(index=str, columns={'0_y':'0', '1_y':'1'})
print(mydf.head(5))
print(mydf.shape)

# function to query pubmed papers from search terms and return their pubmed ids
def search(query):
    Entrez.email = 'fake@fakemail.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='20',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results

# function to retrieve article details from pubmed ids
def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'fake@fakemail.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results



for i in range(110,729):
    text = ''
    count = 0
    for id in mydf[mydf[str(i)]==1].sample(frac=1).iterrows():
        # print(id[1]['0_x'])
        try:
            k = pcp.get_synonyms(id[1]['0_x'], 'inchi')
        except:
            k = []

        try:
            pubmedIDs = search(k[0]['Synonym'][0])
            papers = fetch_details(pubmedIDs['IdList'])
            count += 1

        except:
            print('NO RESULTS')
            papers = {}

        try:
            for x in papers['PubmedArticle']:
                print('#############################################')
                print(x['MedlineCitation']['Article']['ArticleTitle'])
                text += x['MedlineCitation']['Article']['ArticleTitle'][:-1] + ' '
            print(text)

        except: pass

        time.sleep(1)
        if count == 1000:
            count = 0
            break
    try:
        wordcloud = WordCloud(background_color='white', max_words=100, max_font_size=50).generate(text)
        print("IMAGE SAVED")
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig("/home/rlougee/Desktop/wordclouds/TXP-{}".format(i+1), dpi=1200)
        # plt.show()
    except:
        pass

# pcp.download('PNG', '/share/home/rlougee/Desktop/pubchem_images/{}.png'.format(i), i, 'cid')

# sys.exit(0)
# # Quinuclidinium = ['C12CCN(CC1)CC2', 'C2C1CCCCN1CCC2', 'C2C1CCCN1CC2', 'C(CN(C)C)C', 'C1CCN(CC1)C']
# print('Related Compound Count:', len(pcp.get_cids('C12CCN(CC1)CC2', 'smiles', searchtype='substructure')))
# text = ''
# count = 0
# for i in pcp.get_cids('C12CCN(CC1)CC2', 'smiles', searchtype='substructure'):
#     j = pcp.get_synonyms(i, 'cid')
#     count += 1
#     # print(count, j[0]['Synonym'][0])
#     try:
#         pubmedIDs = search(j[0]['Synonym'][0])
#         papers = fetch_details(pubmedIDs['IdList'])
#     except:
#         print('NO RESULTS')
#         papers = {}
#     try:
#         # pprint.pprint(papers)
#
#         for i in papers['PubmedArticle']:
#             print('#############################################')
#             print(i['MedlineCitation']['Article']['ArticleTitle'])
#             text += i['MedlineCitation']['Article']['ArticleTitle'][:-1] + ' '
#         print(text)
#
#     except: print('2')
#
#     time.sleep(1)
#     if count == 100:
#         break



    # pcp.download('PNG', '/share/home/rlougee/Desktop/pubchem_images/{}.png'.format(i), i, 'cid')

# for i in range(0,1000,100):
#     print(i)
#     n = pcp.get_compounds('C12CCN(CC1)CC2', 'smiles', searchtype='substructure', listkey_count=i+100, listkey_start=i)
#     for i in n:
#         print(i.synonyms)
#         # print(pcp.)
#     time.sleep(300)

