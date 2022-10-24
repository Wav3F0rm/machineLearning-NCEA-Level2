import game
from collections import namedtuple
import matplotlib.pyplot as plt
from IPython import display

Point = namedtuple('Point', 'x, y')
plt.ion()

BLOCK_SIZE = 20

def inUnsafe(snake):
    snake = snake
    checkpoints = []
    unsafeCoordinates = []

    for i in snake:
        checkpoints.append(Point(i.x-BLOCK_SIZE, i.y))
        checkpoints.append(Point(i.x+BLOCK_SIZE, i.y))
        checkpoints.append(Point(i.x, i.y-BLOCK_SIZE))
        checkpoints.append(Point(i.x, i.y+BLOCK_SIZE))

    for i in checkpoints:
        if checkpoints.count(i) > 1:
            unsafeCoordinates.append(i)
    return unsafeCoordinates


''' def _graphUnsafe(snake, checkpoints, unsafeCoordinates):
        display.clear_output(wait=True)
        display.display(plt.gcf())
        plt.clf()
        plt.plot()'''