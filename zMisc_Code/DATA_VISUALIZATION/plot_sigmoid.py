import matplotlib.pyplot as plt
import numpy as np
import math

#plot sigmoid curves to represent does reponse curves for BURST vs NONBURST

Xaxis = np.arange(-20,20, 1)
Yaxis = np.arange(-20 ,20, 1)

def sigmoid(x):
    a = []
    for item in x:
        a.append(1/(1+math.exp(-item)))
    return a

x = Xaxis
sig = sigmoid(x)
y = Xaxis
sig2 = sigmoid(y+2)
print(np.random.normal(0, 1, 200))
for i in np.random.normal(-5, 2, 200):
    plt.plot(x, sigmoid(x+i), color='turquoise', alpha=.3)

for i in np.random.normal(5, 4, 30):
    plt.plot(x, sigmoid(x+i),  color='magenta', alpha=.3)
print(x.shape)
plt.plot([1 for i in range(40)], sigmoid(x), linestyle='--', color='red')
plt.xticks([-15, -10, -5, 0, 5, 10], [0.01,0.1, 1, 10, 100, 1000])
plt.xlabel("DOSE")
plt.ylabel('RESPONSE')
plt.title("MOCK Dose Response Curve")
plt.xlim(-17, 10)
print(sigmoid(x))
# ply.ylim
plt.show()
