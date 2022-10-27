import math

import pygame
import random


class Game:
    def __init__(self, root, maxX, maxY):
        self.root = root
        self.agents = []
        self.foods = []
        self.maxX = maxX
        self.maxY = maxY

    def generateAgents(self, num, size, color, sightRange):
        for i in range(0, num):
            randomX = random.randint(10, self.maxX - 10)
            randomY = random.randint(10, self.maxY - 10)
            pygame.draw.rect(self.root, color, (randomX, randomY, size, size))
            self.agents.append(Agent(randomX, randomY, color, size, sightRange))

    def generateFood(self, num, size, color):
        for i in range(num):
            randomX = random.randint(10, self.maxX - 10)
            randomY = random.randint(10, self.maxY - 10)
            pygame.draw.rect(self.root, color, (randomX, randomY, size, size))
            self.foods.append(Food(randomX, randomY, size, color))



    def drawAgents(self):
        for agent in self.agents:
            pygame.draw.circle(self.root, (255, 255, 255), (agent.xpos + agent.size / 2, agent.ypos + agent.size / 2), agent.sightRange)
            pygame.draw.rect(self.root, agent.color, (agent.xpos, agent.ypos, agent.size, agent.size))

    def drawFood(self):
        for food in self.foods:
            pygame.draw.rect(self.root, food.color, (food.xpos, food.ypos, food.size, food.size) )


class Agent:
    def __init__(self, xpos, ypos, color, size, sightRange):
        self.xpos = xpos
        self.ypos = ypos
        self.color = color
        self.size = size
        self.sightRange = sightRange
        self.searchRange = 300
        self.timeInDirection = 10
        self.movementAngle = None
        self.speed = 5

    def setDirection(self):
        randAngle = random.randint(0, 360)
        self.movementAngle = randAngle

    def move(self, maxX, maxY):
        self.xpos += int(math.cos(self.movementAngle) * self.speed)
        self.ypos += int(math.sin(self.movementAngle) * self.speed)

        if self.xpos <= 0:
            self.xpos += 5
            self.setDirection()
        elif self.xpos >= maxX:
            self.xpos -= 5
            self.setDirection()

        if self.ypos <= 0:
            self.ypos += 5
            self.setDirection()
        elif self.ypos >= maxY:
            self.ypos -= 5
            self.setDirection()

        if self.timeInDirection <= 0:
            self.setDirection()
            self.timeInDirection = 6

class Food:
    def __init__(self, xpos, ypos, size, color):
        self.xpos = xpos
        self.ypos = ypos
        self.size = size
        self.color = color



