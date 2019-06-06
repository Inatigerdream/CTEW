import tkinter
from tkinter import *

HEIGHT = 1000
WIDTH = 1000
xa = -2.0; xb = 1.0
ya = -1.5; yb = 1.5
maxIt = 2000

root = Tk()
root.geometry('1000x1000')

my_canvas = Canvas(root, height=HEIGHT, width=WIDTH, bg="white")



my_canvas.grid(row=0, column=0)

# basic shapes
# l = my_canvas.create_line(5,5,5,5, width=100)
# o = my_canvas.create_oval(20,20,100,100, fill='grey')
# a = my_canvas.create_arc(10,50,240,210, extent=66, fill='pink')


# def mandelbrotDraw():
img = PhotoImage(width= WIDTH, height=HEIGHT)
my_canvas.create_image((0,0), image = img, state = "normal", anchor = tkinter.NW)

for ky in range(HEIGHT):
    for kx in range(WIDTH):
        c = complex(xa + (xb - xa) * kx / WIDTH, ya + (yb - ya) * ky / HEIGHT)
        z = complex(0.0, 0.0)
        for i in range(maxIt):
            z = z * z + c
            if abs(z) >= 2.0:
                break
        rd = hex(i % 4 * 64)[2:].zfill(2)
        gr = hex(i % 8 * 32)[2:].zfill(2)
        bl = hex(i % 16 * 16)[2:].zfill(2)
        # img.put("#" + rd + gr + bl, (kx, ky))
        img.put("#" + '00' + gr + bl, (kx, ky))
        root.title("mandelbrot set")





my_canvas.pack()

root.mainloop()


