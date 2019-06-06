import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import matplotlib.axes as ax
def barplot(height, bars, aeid, mycolor=['#ff8800', '#ff5500', '#f97900', '#ff9b4f', '#ff4912']):
    y_pos = np.arange(len(bars))

    # create bars and choose color
    plt.bar(y_pos, height, color=mycolor)

    # ADd title and axis names
    plt.title('Toxprints Odd\'s Ratios for {}'.format(aeid))
    plt.xlabel('Toxprints')
    plt.ylabel('Odd\'s Ratio')

    # Limits for the Y axis
    plt.ylim(0, 10)
    # Create names
    plt.xticks(y_pos[::20], bars[::20], rotation=90)

    # vertical line at OR 3
    plt.hlines(3,0,len(bars), linestyles='dashed', color='red', alpha=0.3)

    # add see-through boxes for Toxprint Categories
    rect = patch.Rectangle((0,0),1, 1, color='blue', alpha=1)


    
# # # TEST # # #
if __name__=='__main__':
    height = [3, 12, 5, 18, 45]
    bars = ('A', 'B', 'C', 'D', 'E')

    barplot(height, bars)
    plt.tight_layout()
    plt.show()


