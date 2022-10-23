import matplotlib.pyplot as plt
from collections import namedtuple

Point = namedtuple('Point', 'x, y')

snake = [Point(x=1,y=5), Point(x=1,y=4), Point(x=1,y=3), Point(x=1,y=2), Point(x=1,y=1), Point(x=2,y=1),
            Point(x=3,y=1), Point(x=4,y=1), Point(x=4,y=2), Point(x=4,y=3), Point(x=3,y=3)]
print(snake)

xcoordinates = []
ycoordinates = []
for i in snake:
    xcoordinates.append(i.x)
    ycoordinates.append(i.y)

checkpoints = []
for i in snake:
    checkpoints.append([i.x-1, i.y])
    checkpoints.append([i.x+1, i.y])
    checkpoints.append([i.x, i.y-1])
    checkpoints.append([i.x, i.y+1])
print(checkpoints)

xcheckpoints = []
ycheckpoints = []
for i in checkpoints:
    xcheckpoints.append(i[0])
    ycheckpoints.append(i[1])

unsafe = []
for i in checkpoints:
    if checkpoints.count(i) > 1:
        unsafe.append(i)
print(unsafe)

xunsafe = []
yunsafe = []
for i in unsafe:
    xunsafe.append(i[0])
    yunsafe.append(i[1])


plt.plot(xcoordinates, ycoordinates, color='green', linewidth=7)
plt.scatter(xcheckpoints, ycheckpoints, color='blue')
plt.scatter(xunsafe, yunsafe, color='red')
plt.show()