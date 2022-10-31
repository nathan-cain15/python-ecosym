import pygame

from classes import *

pygame.init()
root = pygame.display.set_mode((1200, 900))

lightGreen = (81, 125, 25)
darkGreen = (55, 75, 30)
blue = (79, 166, 235)
yellow = (240, 173, 0)
red = (156, 67, 0)
grey = (123, 111, 131)
tan = (243, 192, 114)
white = (249, 238, 225)
black = (0, 0, 0)



run = True
first = True
paused = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    root.fill(blue)
    ticks = pygame.time.get_ticks()

    if first == True:
        game = Game(root, 1200, 900)
        game.generateAgents(10, black, 10, 50, 10, 5)
        game.generateFood(100, 5, lightGreen)
        for agent in game.agents:
            agent.setDirection()
        pauseButton = Button(root, 1100, 50)
        first = False

    agents = [i for i in game.agents]

    game.drawAgents()
    game.drawFood()
    game.checkForFoodInSight()
    game.checkForColisions()
    if ticks % 50 == 0 and not paused:
        for agent in game.agents:
            agent.timeInDirection -= 1
            agent.move(1200, 900)
        game.killAgents()
        game.agentsReproduce()
        print([agents[-1].speed, agents[-1].sightRange, agents[-1].timeInDirectionConst])

    if ticks % 1000 == 0 and not paused:
        game.generateFood(8, 5, lightGreen)

    game.drawAgents()
    game.drawFood()
    game.checkForFoodInSight()
    game.checkForColisions()


    pygame.display.flip()

