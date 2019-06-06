import matplotlib
import matplotlib.pyplot as plt

from zMisc_Code.DATA_VISUALIZATION.spirograph import plot_spiro

ncycle = 10
r1 = 1
r2 = 1
r3 = 1
mylist1 = [[ncycle, x, r2, r3] for x in range(-3,4)]
mylist2 = [[ncycle, r1, x, r3] for x in range(-3,4)]
mylist3 = [[ncycle, r1, r2, x] for x in range(-3,4)]

fig, ax = plt.subplots()
a = plt.Circle((0,0), r1, alpha=.3, color='blue')
b = plt.Circle((-(r1+r2),0), r2, alpha=.3, color='red')
c = matplotlib.lines.Line2D([(-(r1+r2)+(r3)), -(r1+r2)],[0,0], alpha=.3, c='yellow')
ax.add_artist(a)
ax.add_artist(b)
ax.add_artist(c)
# plt.plot(circle(ncycle, r3))
# plt.show()

# print(mylist)
plot_spiro([[ncycle, r1, r2, r3]])
plot_spiro(mylist1)
plot_spiro(mylist2)
plot_spiro(mylist3)