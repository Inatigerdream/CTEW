from PIL import Image
import sys, os

file_names = ('/home/rlougee/Desktop/CID_pix/264/' + fn for fn in os.listdir('/home/rlougee/Desktop/CID_pix/264/.') if fn.endswith('.png'))

# print(file_names)

images = [Image.open(fn) for fn in file_names]
print(images)
images[0].save('/home/rlougee/Desktop/gif1.gif', save_all=True, append_images=images, duration=len(images)/1000, loop=0)