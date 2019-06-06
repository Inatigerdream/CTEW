import sys
import pandas as pd
from PIL import Image
import glob

### creates chemotype images for all the enriched chemotypes in an enrichment table ###

# import all the image files
# images = []
# for filename in glob.glob('/home/rlougee/Desktop/CT_image/*'):
#     im=Image.open(filename)
#     images.append(im)



path = '/home/rlougee/Desktop/CT_image/'

for f in glob.glob('/home/rlougee/Desktop/Assay_Categories/enrichment_tables/*'):
    print(f)

    table = pd.read_csv(f, sep='\t')
    print(table.shape)

    if table.shape[0] == 1:
        continue

    table = table['Fingerprint_ID'][0:-1]

    #open image files for each enriched Toxprint
    images = list(map(Image.open, [path + str(i) for i in table]))
    images = [x.resize((500, 500)) for x in images ]

    # get the total width
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)

    # set max width
    if total_width > 50000:
        total_width = 50000

    # create a blank new image
    new_im = Image.new('RGB', (total_width, max_height))
    new_im2 = Image.new('RGB', (total_width, max_height))
    new_im3 = Image.new('RGB', (total_width, max_height))

    # make the image(s)
    # if > 100 enriched chemotypes 1st file will have black space
    x_offset = 0
    count = 0
    for im in images:
        count += 1
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]
        if count == 100:
            new_im2 = new_im
            new_im = Image.new('RGB', (total_width, max_height))
            x_offset = 0
        if count == 200:
            new_im3 = new_im
            new_im = Image.new('RGB', (total_width, max_height))
            x_offset = 0

    # new_im.show()
    # sys.exit(0)

    file_name = f.split('.')[0].split('/')[-1]


    try:
        new_im.save('/home/rlougee/Desktop/Assay_Categories/enrichment_images/{}.jpg'.format(file_name))
    except:
        print(file_name)

    if count > 100:
        try:
            new_im2.save('/home/rlougee/Desktop/Assay_Categories/enrichment_images/{}_2.jpg'.format(file_name))
        except:
            print(file_name)

    if count > 200:
        try:
            new_im2.save('/home/rlougee/Desktop/Assay_Categories/enrichment_images/{}_3.jpg'.format(file_name))
        except:
            print(file_name)
