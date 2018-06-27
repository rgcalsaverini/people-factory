from numpy.random import normal
import matplotlib.pyplot as plt


func = lambda: normal(0.75, 0.08)

size = 500000
all = [func() for _ in range(size)]

plt.hist(all, bins='auto')
plt.show()
