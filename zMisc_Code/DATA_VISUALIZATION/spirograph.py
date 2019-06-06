import matplotlib.pyplot as plt
from numpy import pi, exp, real, imag, linspace

# # # CODE TO PLOT SPIROGRAPHS # # #
# this hypercycloid aka epicycloid # how to do hypoclycloid?
def spiro(t, r1, r2, r3):
    """
    Create Spirograph curves made by one circle of radius r2 rolling around
     the inside (or outside) of another or radius r1. The pen is a distance
     r3 from the center of the first circle.
    """
    return r3*exp(1j*t*(r1+r2)/r2) + (r1+r2)*exp(1j*t)


def circle(t, r):
    return r * exp(1j*t)

def plot_spiro(list):

    plt.style.use('seaborn-pastel')
    plt.rcParams['axes.facecolor'] = 'white'
    for i in list:
        t = linspace(0, i[0]*2 * pi, 1000)
        plt.plot(real(spiro(t, i[1], i[2], i[3])), imag(spiro(t, i[1], i[2], i[3])))
    fig = plt.gcf()
    fig.gca().set_aspect('equal')
    plt.show()

























# # # TEST # # #
if __name__ == '__main__':
    # set style for pyplot
    # plt.style.use('ggplot')
    plt.style.use('seaborn-pastel')
    plt.rcParams['axes.facecolor'] = 'white'

    # set params
    r1 = 0.01
    r2 = 52.0 / 100.0
    r3 = 42.0 / 100.0
    ncycle = 20 # LCM(r1,r2)/r2
    t = linspace(0, ncycle*2*pi, 1000)

    # plot circle
    plt.plot(real(circle(t/ncycle, r1*150)), imag(circle(t/ncycle, r1*150)))

    # plot spirographs
    #plt.plot(real(spiro(t,r1,r2,r3)), imag(spiro(t, r1, r2, r3)))
    #plt.plot(real(spiro(t,r1,r2,r3)), imag(spiro(t, r1/10, r2/10, r3/30)))
    plt.plot(real(spiro(t,r1,r2,r3)), imag(spiro(t, r1, r2, r3)))
    #plt.plot(real(spiro(t,r1,r2,r3)), imag(spiro(t, r1, r2/10, r3/30)))
    plt.plot(real(spiro(t,r1,r2,r3)), imag(spiro(t, r1, r2, r3-.5)))
    plt.plot(real(spiro(t,r1,r2,r3)), imag(spiro(t, r1+.5, r2, r3)))



    fig = plt.gcf()
    fig.gca().set_aspect('equal')
    plt.show()