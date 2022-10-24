from collections import namedtuple

Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 20

unsafeCoordinates = []

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
