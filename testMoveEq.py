import numpy as np 
from matplotlib import pyplot as plt


def main():
	"""
	time = np.linspace(0, 0.5, 100)

	dt = time[2] -time[1]
	y = [600]

	v0 = 800
	a = 3200

	Y = 600 - v0 * time + 0.5 * a * time**2

	for c in range(1,len(time)):
		y.append((y[c-1]-v0 + a*time[c]) )

	plt.plot(time, y)
	plt.plot(time, Y)
	plt.show()
	"""

	"""
	x = np.linspace(0,6,7)
	y = x**2

	dy = []
	dy.append([ y[c] - y[c-1] for c in range(1,len(x))] )

	dy = dy[0]

	print("dy: ", dy)

	x2 = np.linspace(0,len(dy)-1, len(dy))

	print("x2: ", x2)

	plt.plot(x, y)
	plt.plot(x2, dy)


	y2 = [0]
	for c in range(1,len(dy)):
		y2.append(y2[c-1] + dy[c-1])

	print("y2: ", y2)
	print("y: ", y)

	plt.plot(x2, y2)


	plt.show()
	"""

	"""
	time = np.linspace(0, 0.5, 100)

	dt = time[2] -time[1]
	y = [600]

	v0 = 800
	a = 3200

	Y = - v0 * time + 0.5 * a * time**2

	diff = dt * (-v0 + a * time)

	plt.plot(time, Y)

	plt.plot(time, diff)

	cum = np.cumsum(diff)
	plt.plot(time, cum)
	plt.show()
	"""

	time = np.linspace(0, 0.5, 100)

	dt = time[2] -time[1]
	y = [600]

	v0 = 800
	a = 3200

	Y = 600 - v0 * time + 0.5 * a * time**2

	for c in range(1,len(time)):
		y.append((y[c-1]+ dt* (-v0 + a*time[c])) )

	plt.plot(time, y)
	plt.plot(time, Y)
	plt.show()


if __name__ == "__main__":
	main()