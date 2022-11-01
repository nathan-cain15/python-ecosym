import math

import pygame
import random


def changeGene(parentValue, changeBy):
    return random.choice([parentValue, parentValue, parentValue - changeBy, parentValue + changeBy])
class Game:
    def __init__(self, root, maxX, maxY):
        self.root = root
        self.agents = []
        self.foods = []
        self.maxX = maxX
        self.maxY = maxY

    def generateAgents(self, num, color, size, sightRange, timeInDirectionConst, speed):
        for i in range(0, num):
            randomX = random.randint(10, self.maxX - 10)
            randomY = random.randint(10, self.maxY - 10)
            pygame.draw.rect(self.root, color, (randomX, randomY, size, size))
            self.agents.append(Agent(randomX, randomY, color, size, sightRange, timeInDirectionConst, speed))

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

    def agentsReproduce(self):
        for agent in self.agents:
            if agent.energy >= 2000:
                agent.energy -= 1000
                xposDirection = random.choice([agent.size + 5, -1 * agent.size - 5])
                yposDirection = random.choice([agent.size + 5, -1 * agent.size - 5])
                self.agents.append(Agent(agent.xpos + xposDirection, agent.ypos + xposDirection, agent.color, agent.size, changeGene(agent.sightRange, 2), changeGene(agent.timeInDirectionConst, 0.5), changeGene(agent.speed, 0.25)))

    def killAgents(self):
        for agent in self.agents:
            if agent.energy <= 0:
                self.agents.remove(agent)


class Agent:
    def __init__(self, xpos, ypos, color, size, sightRange, timeInDirectionConst, speed):
        self.xpos = xpos
        self.ypos = ypos
        self.color = color
        self.size = size
        self.sightRange = sightRange
        self.timeInDirection = timeInDirectionConst
        self.timeInDirectionConst = timeInDirectionConst
        self.movementAngle = 0
        self.speed = speed
        self.energy = 1000
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

        self.energy -= self.speed + (self.sightRange / 10)

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
        self.energy = 500

class Button:
    def __init__(self, root, x, y):
        self.root = root
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0

    def draw(self, color1, color2, text, size):
        font = pygame.font.SysFont('Comic Sans MS', size)
        textSurface = font.render(text, True, color1, color2)
        textRect = textSurface.get_rect()
        self.width = textRect[2]
        self.height = textRect[3]

        self.root.blit(textSurface, (self.x, self.y))

    def pressed(self, mouse, click):
        if (self.x <= mouse[0] and mouse[0] <= self.x + self.width) and (
                self.y <= mouse[1] and mouse[1] <= self.y + self.height) and click[0] == True:
            pygame.draw.rect(self.root, (0, 0, 0), (self.x - 1, self.y - 1, self.width + 2, self.height + 2))
            return True
        return False

class Text:
    def __init__(self, root, xpos, ypos, color):
        self.root = root
        self.xpos = xpos
        self.ypos = ypos
        self.color = color

    def draw(self, text, size):
        font = pygame.font.SysFont('Comic Sans MS', size)
        textSurface = font.render(text, True, self.color)
        self.root.blit(textSurface, (self.xpos, self.ypos))


