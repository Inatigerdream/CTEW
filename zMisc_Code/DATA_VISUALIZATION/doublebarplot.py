import numpy as np
import matplotlib.pyplot as plt

def doublebarplot(list1, list2, n=20, title='', label1='l1', label2='l2', xlabel=[], color1='turquoise', color2='dodgerblue', save='', barval=True):
    """ Plot a double barplot of two lists. specify length with n """

    if len(xlabel) == 0:
        xlabel = list1.index

    barwidth = 0.3
    n = 50
    r1 = np.arange(len(list1[:n]))
    r2 = [x + barwidth for x in r1]

    fig, ax = plt.subplots()

    rects1 = ax.bar(r1, list1[:n], barwidth, color=color1, alpha=1, zorder=3, label=label1)
    rects2 = ax.bar(r2, list2[:n], barwidth, color=color2, alpha=.8, zorder=3, label=label2)

    # add labels
    ax.set_ylabel('Counts', fontsize=14, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(r1)
    ax.set_xticklabels(xlabel[:n+1], rotation='vertical', fontweight='bold')
    ax.set_facecolor('.98')
    ax.grid(color='.9', zorder=0)
    ax.legend()

    plt.ylim(0, 300)

    # auto label
    def autolabel(rects, xpos='center'):
        """
        attach a text label above each bar displaying its height
        """
        xpos = xpos.lower()
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}

        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                    '{}'.format(int(height)), ha=ha[xpos], va='bottom')

    if barval==True:
        autolabel(rects1, "center")
        autolabel(rects2, "center")
    # plt.ylim((0,25))
    fig.set_size_inches(15, 7)
    if save == '':
        plt.show()
    else:
        plt.savefig(save, dpi=500, quality=95, format='jpg', orientation='landscape')