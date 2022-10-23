from matplotlib import markers
from matplotlib.lines import lineStyles
import matplotlib.pyplot as plt
import numpy as np

xCoordinates = np.array([1, 2, 3, 4, 4, 4, 3, 2, 1, 1])
yCoordinates = np.array([1, 1, 1, 1, 2, 3, 3, 3, 3, 2])

plt.plot(xCoordinates, yCoordinates)
plt.show()
