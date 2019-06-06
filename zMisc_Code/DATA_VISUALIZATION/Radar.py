import matplotlib.pyplot as plt
import pandas as pd
from math import pi




# plots a radar plot
# probably be better if this worked with dataframes

def radar(data):
    #number of vars
    categories=data.iloc[:,0]
    N = len(categories)
    print(categories)


    # print(data.iloc[:,1])
    # repeat 1st value to close graph
    values2 = data.iloc[0].drop(data.columns.values[0]).values.flatten().tolist()
    values2 = list(data.iloc[:,1])
    # values2 = values2[1:]
    print(values2)
    values2 += values2[:1]
    values2

    # calculate angles
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # init plot
    ax = plt.subplot(111, polar=True)

    # Draw one axe per variable + add labels
    plt.xticks(angles[::int(N/8)+1], categories[::int(N/8)+1], color='grey', size=8)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([3, 5, 10], ["3", "5", "10"], color='grey', size=7)
    plt.ylim(0,10)

    # plot data
    ax.plot(angles, values2, linewidth=2, linestyle='solid', color='#fdc513')

    #fill area
    ax.fill(angles, values2, 'g', alpha=0.1)

# # # TEST # # #
if __name__ == "__main__":
    mydata = pd.DataFrame({
        'group': ['A','B', 'C', 'D'],
        'var1': [38, 1.5, 30, 4],
        'var2': [29, 10, 9, 34],
        'var3': [8, 39, 23, 24],
        'var4': [7, 31, 33, 14],
        'var5': [28, 15, 32, 14]
    })

    print(mydata.head())
    radar(mydata)
    plt.show()