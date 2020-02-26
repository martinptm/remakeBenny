#import matplotlib.pyplot as plt
#import numpy as np
import time
import turtle
"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 6*np.pi, 100)
y = np.sin(x)

# You probably won't need this if you're embedding things in a tkinter plot...
plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma

for phase in np.linspace(0, 10*np.pi, 500):
    line1.set_ydata(np.sin(x + phase))
    fig.canvas.draw()
    fig.canvas.flush_events()

x = 2
y = 4

plt.plot(x,y, 'o')
for c in range(5):
    y = y- 0.5
    plt.plot(x,y,'o')
    plt.show()
    time.sleep(0.3)
"""
v_x = 3
v_y = 0
g = 0.2

ball = turtle.Turtle()
ball.shape('circle')
ball.speed(0)

for c in range(0,50):
    ball.forward(v_x)
    ball.right(90)
    ball.forward(v_y)
    ball.left(90)
    v_y += g
    #time.sleep(0.01)

