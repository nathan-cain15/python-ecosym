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

    def generateAgents(self, num, size, color):
        for i in range(0, num):
            randomX = random.randint(10, self.maxX - 10)
            randomY = random.randint(10, self.maxY - 10)
            pygame.draw.rect(self.root, color, (randomX, randomY, size, size))
            self.agents.append(Agent(randomX, randomY, color, size))

    def generateFood(self, num, size, color):
        for i in range(num):
            randomX = random.randint(10, self.maxX - 10)
            randomY = random.randint(10, self.maxY - 10)
            pygame.draw.rect(self.root, color, (randomX, randomY, size, size))
            self.foods.append(Food(randomX, randomY, size, color))

    def drawAgents(self):
        for agent in self.agents:
            agent.circleRect = pygame.draw.circle(self.root, (255, 255, 255), (agent.xpos + agent.size / 2, agent.ypos + agent.size / 2), agent.sightRange)
            agent.rect = pygame.draw.rect(self.root, agent.color, (agent.xpos, agent.ypos, agent.size, agent.size))

    def drawFood(self):
        for food in self.foods:
            food.rect = pygame.draw.rect(self.root, food.color, (food.xpos, food.ypos, food.size, food.size))

    def checkForColisions(self):
        for agent in self.agents:
            if agent.currentFood != None:
                if agent.currentFood not in self.foods:
                    agent.currentFood = None
            for food in self.foods:
                if agent.rect.colliderect(food.rect):
                    agent.energy += 1
                    agent.setDirection()
                    agent.timeInDirection = agent.timeInDirectionConst
                    agent.energy += food.energy
                    agent.currentFood = None
                    self.foods.remove(food)

    def checkForFoodInSight(self):
        for agent in self.agents:
            if agent.currentFood != None:
                continue
            for food in self.foods:
                if agent.circleRect.colliderect(food.rect):
                    agent.currentFood = food


class Agent:
    def __init__(self, xpos, ypos, color, size):
        self.xpos = xpos
        self.ypos = ypos
        self.color = color
        self.size = size
        self.sightRange = 50
        self.timeInDirection = 10
        self.timeInDirectionConst = 10
        self.movementAngle = None
        self.speed = 5
        self.energy = 300
        self.circleRect = None
        self.rect = None
        self.currentFood = None

    def setDirection(self):
        randAngle = random.randint(0, 360)
        self.movementAngle = randAngle

    def move(self, maxX, maxY):
        if self.currentFood != None:
            if self.currentFood.xpos - self.xpos == 0:
                self.xpos += 1
            angle = math.degrees(math.atan((self.currentFood.ypos - self.ypos) / (self.currentFood.xpos - self.xpos)))
            if self.currentFood.ypos - self.ypos <= 0 and self.currentFood.xpos - self.xpos <= 0:
                self.movementAngle = 180 + angle
            elif self.currentFood.ypos - self.ypos >= 0 and self.currentFood.xpos - self.xpos <= 0:
                self.movementAngle = 180 + angle

            elif self.currentFood.ypos - self.ypos <= 0 and self.currentFood.xpos - self.xpos >= 0:
                self.movementAngle = 360 + angle
            else:
                self.movementAngle = angle
        self.xpos += math.cos(math.radians(self.movementAngle)) * self.speed
        self.ypos += math.sin(math.radians(self.movementAngle)) * self.speed

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
            self.timeInDirection = self.timeInDirectionConst

class Food:
    def __init__(self, xpos, ypos, size, color):
        self.xpos = xpos
        self.ypos = ypos
        self.size = size
        self.color = color
        self.rect = None
        self.energy = 100



