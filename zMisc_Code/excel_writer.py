import pandas as pd
from PIL import Image
import xlsxwriter

### THIS DOES NOT WORK ###
# trying to add images to excel comments

writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')

print('woop')

df1 = pd.read_csv('/home/rlougee/Desktop/Assay_Categories/enrichment_tables/intended_target_family_nuclearreceptor_table.tsv.tsv', sep='\t')
df1.to_excel(writer, sheet_name='Sheet1')
Txp118 = Image.open('/home/rlougee/Desktop/CT_image/Txp-118')
workbook = writer.book
# print(workbook.worksheets())
workbook.get_worksheet_by_name('Sheet1').write_comment('A2', Txp118)
# print(workbook)

writer.save()