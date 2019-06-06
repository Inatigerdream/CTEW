import os
from PIL import Image
import glob
import sys

def cutupimage(path, input, cutsvertical, cutshorizontal, k):
    im = Image.open(input)
    imgwidth, imgheight = im.size
    height = int((imgheight/cutsvertical)) # some difficulty using round here with range below
    width = int((imgwidth/cutshorizontal)) # some difficulty using round here with range below
    # print(imgheight, height)
    # print(imgwidth, width)
    for i in range(0, imgheight-height, height):
        for j in range(0, imgwidth-width, width):
            box = (j, i, j+width, i+height)
            o = im.crop(box)
            try:
                o.save('{}Txp-{}.png'.format(path,str(k)))
            except:
                print('image save fail')
            k += 1


for i in glob.glob('/home/rlougee/Desktop/CTs/*'):
    count = i.split('/')[-1].split('.')[0]
    print(count)
    cutupimage('/home/rlougee/Desktop/CT_images_2/', i, 6, 10, int(count))
    # sys.exit()