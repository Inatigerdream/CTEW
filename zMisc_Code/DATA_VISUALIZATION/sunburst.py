import matplotlib.pyplot as plt
import numpy as np

def sunburst(nodes, total=np.pi * 2, offset=0, level=0, ax=None, color_list=['#f9dc26', '#fdc513', '#8be0f6', '#eafbfa']):
    ax = ax or plt.subplot(111, projection='polar')
    index = 0
    if level ==0 and len(nodes) == 1:
        label, value, subnodes = nodes[0]
        ax.bar([0], [.5], [np.pi*2], color=color_list[level])
        ax.text(0, 0, label, ha='center', va='center')
        sunburst(subnodes, total=value, level=level + 1, ax=ax, color_list=color_list)
    elif nodes:
        d = np.pi*2 / total
        labels = []
        widths = []
        local_offset = offset
        for label, value, subnodes in nodes:
            labels.append(label)
            widths.append(value * d)
            sunburst(subnodes, total=total, offset=local_offset, level=level + 1, ax=ax, color_list=color_list)
            local_offset += value
        values = np.cumsum([offset * d] + widths[:-1])
        heights = [1] * len(nodes)
        bottoms = np.zeros(len(nodes)) + level - .5
        rects = ax.bar(values, heights, widths, bottoms, linewidth=1, edgecolor='white', align='edge', color = color_list[level])
        for rect, label in zip(rects, labels):
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_y() + rect.get_height() / 2
            rotation = (90 + (360 - np.degrees(x) % 180)) % 360
            ax.text(x, y, label, rotation = rotation, ha='center', va='center')

    if level == 0:
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location('N')
        ax.set_axis_off()


# # # TEST # # #
if __name__ == "__main__":
    data = [
        ('', 100, [
            ('Cell\nAssays', 70, [
                ('Mouse', 40, []),
                ('Human', 20, []),
                ('Avian', 5, []),
            ]),
            ('Biochem\nAssays', 15, [
                ('SRC', 6, [
                    ('black', 4, []),
                    ('blue', 1, []),

                ]),
                ('ATP', 4, []),
                ('SAM', 2, []),
                ('CAT', 1, []),
                ('DOG', 1, []),
                ('LOL', 1, []),
            ]),
        ]),
    ]

    sunburst(data, color_list = ['#00ffec', '#00c5ff', '#0092ff', '#005eff'])
    plt.show()

    #color_list = ['#00ffec', '#00c5ff', '#0092ff', '#005eff']
    #color_list = ['#f9dc26', '#fdc513', '#8be0f6', '#eafbfa']