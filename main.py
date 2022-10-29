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

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    root.fill(blue)
    ticks = pygame.time.get_ticks()

    if first == True:
        game = Game(root, 1200, 900)
        game.generateAgents(10, 10, black)
        game.generateFood(30, 5, lightGreen)
        for agent in game.agents:
            agent.setDirection()

        first = False
    agents = [i for i in game.agents]

    game.drawAgents()
    game.drawFood()
    game.checkForFoodInSight()
    game.checkForColisions()
    if ticks % 50 == 0:
        for agent in game.agents:
            agent.timeInDirection -= 1
            agent.move(1200, 900)

    if ticks % 1000 == 0:
        game.generateFood(5, 5, lightGreen)

    game.drawAgents()
    game.drawFood()
    game.checkForFoodInSight()
    game.checkForColisions()



    #print(agents)



    pygame.display.flip()

