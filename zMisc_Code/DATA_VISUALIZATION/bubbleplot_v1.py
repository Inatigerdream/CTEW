import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cbook as cbook
import matplotlib.cm as cm
import circlify as circ
from PIL import Image
import numpy as np

# import an image
# image = plt.imread('/home/rlougee/Desktop/CT_image_3/Txp-{}.png'.format(111))
# image = image.resize((np.array(image.size)/2).astype(int))

#
image = Image.open('/home/rlougee/Desktop/CT_image_3/Txp-{}.png'.format(111))
# plt.imshow(image)
# plt.show()


# ### TRYING TO PLOT TXP IMAGE AS CIRCLE
### AXIS NOT THE SAME FOR PATCH AND NEWAX?
# # plot figure
# fig, ax = plt.subplots()
# count = .1
# for txp in [ 561]:
#     image = plt.imread('/home/rlougee/Desktop/CT_image_3/Txp-{}.png'.format(txp))
#     newax = fig.add_axes([count, count, count+.5, count+.5])
#     im = newax.imshow(image)
#
#     patch = patches.Circle((count+.26, count+.26), radius=.3333, transform=ax.transData)
#     im.set_clip_path(patch)
#     newax.axis('off')
#     count+=.1
# ax.set_axis_bgcolor('lightslategray')
# # ax.axis('off')
# fig.set_size_inches(10,10)
# plt.show()

data = [19, 17, 13, 11, 7, 5, 321, 217, 123]

# print(circles)

def bubbles(data, labels, images=None, lim=None, labeltext=True):
    """packed circles plot"""
    data = sorted(data, reverse=True)
    circles = circ.circlify(data, with_enclosure=False)


    fig, ax = plt.subplots(figsize=(8.0,8.0))

    n_missing_labels = len(circles) - len(labels)
    if n_missing_labels > 0:
        labels += [""] * n_missing_labels

    axes_dict = {}
    images_dict = {}
    for circle, label in zip(circles, labels):
        x, y, r, = circle
        image = Image.open('/home/rlougee/Desktop/CT_image_3/{}.png'.format(label))
        # print(label, x, y, r)
        patch = ax.add_patch(patches.Circle((x,y), r, alpha=0.2, linewidth=2, fill=False, color='green'))
        r2=r*1.1
        im = ax.imshow(image, extent=[(x-r2),(x+r2),(y+r2),(y-r2)], origin='lower', transform=ax.transData,)
        # im.set_transform(ax.transData) # not doing anything?
        # im.get_extent() # ???
        im.set_clip_path(patch)
        if labeltext==True:
            #ADD TEXT TO BUBBLES
            ax.text(x-len(str(label))/75, y-.015,label, color='red')

    if lim is None:
        lim=max([max(abs(c.x) + c.r, abs(c.y) + c.r)
                 for c in circles])

    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)
    # ax.set_facecolor('lightblue')
    ax.axis('off')
    plt.show()

bubbles(data, ['Txp-{}'.format(x) for x in data], labeltext=False)