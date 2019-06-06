
import sys

# split an sdf file into multiple mol files

f = open('/home/rlougee/Desktop/Aseda_1800_v2000.sdf', 'r')

lines = f.readlines()
f.close()
filename = 0
text=''
check = 0
for i, line in enumerate(lines):
    # print(line)
    # if filename == 0:
    #     filename = line
    #     # filename = filename.replace('','')[1]

    if check == 1:
        filename = line
        check = 0

    if line == '>  <Substance_CASRN>\n':
        check = 1

    text += line

    if line == '$$$$\n':
        myfile = open('/home/rlougee/Desktop/Aseda_mol_files/{}.mol'.format(filename), 'w+')
        myfile.write(text)
        myfile.close()
        filename = 0
        text = ''
