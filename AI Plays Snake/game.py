import pygame
import random
from enum import Enum
from collections import namedtuple  # used to assign meaning to each element within a tuple, increasing readability
import numpy as np
import unsafe

pygame.init() # initialise all pygame modules correctly
font = pygame.font.SysFont('arial', 25)  # taken from system file, runs much slower

# changes to make it 'AI worthy'
# 1. reset function
# 2. reward function to agent
# 3. play(action) -> direction
# 4. game_iteration
# 5. change is_collision function

class Direction(Enum):  # uppercase used for const
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')  # Point object behaves the same way as a class object but more lightweight

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
YELLOW = (255, 255, 0)

BLOCK_SIZE = 20
SPEED = 75

# Object Oriented Programming, or OOP is a programming methodology where objects are defined with properties and values, 
# over the traditional logic and functional approach of procedural programming
class snakeGameAI: # class is a user defined data structure

    def __init__(self, w=640, h=480): # lets class initialise attributes
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                        Point(self.head.x-BLOCK_SIZE, self.head.y),
                        Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.unsafeCoordinates = []
        snake = []

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
    

    def _place_food(self):  # define helper function for food placing
        # pick a random point on the x and y axis of the window in intervals of the block size of the snake.
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self._move(action)  # update the head
        self.snake.insert(0, self.head)  # add new position to front of list

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()  # removes last element from snake

        # 5. find new unsafe coordinates
        snake = self.snake
        self.unsafeCoordinates = unsafe.inUnsafe(snake)

        # 6. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 7. return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # check for hitting boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # check for hitting itself 
        if pt in self.snake[1:]:
            return True
        return False

    def is_unsafe(self, pt=None):
        if pt is None:
            pt = self.head
        # check for hitting unsafe Coordinates
        if pt in self.unsafeCoordinates:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))  # draw food

        for i in self.unsafeCoordinates:
            if i not in self.snake:
                pygame.draw.rect(self.display, YELLOW, pygame.Rect(i.x+5, i.y+5, 10, 10))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()  # updates changes to screen

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)
