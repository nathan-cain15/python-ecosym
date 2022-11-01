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
released = True
averageSpeed = 0
averageSightRange = 0


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    root.fill(blue)
    ticks = pygame.time.get_ticks()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if not released and not click[0]:
        released = True

    if first == True:
        game = Game(root, 1200, 900)
        game.generateAgents(10, black, 10, 50, 10, 5)
        game.generateFood(100, 5, lightGreen)
        for agent in game.agents:
            agent.setDirection()

        pauseButton = Button(root, 1100, 50)
        numberOfAgentsText = Text(root, 25, 25, black)
        averageSightRangeText = Text(root, 25, 50, black)
        averageSpeedText = Text(root, 25, 75, black)
        first = False

    agents = [i for i in game.agents]

    game.drawAgents()
    game.drawFood()
    game.checkForFoodInSight()
    game.checkForColisions()

    if ticks % 50 == 0 and not paused:
        averageSpeed = 0
        averageSightRange = 0

        for agent in game.agents:
            agent.timeInDirection -= 1
            agent.move(1200, 900)

            averageSpeed += agent.speed
            averageSightRange += agent.sightRange

        averageSpeed /= len(agents)
        averageSightRange /= len(agents)

        game.killAgents()
        game.agentsReproduce()

    if ticks % 1000 == 0 and not paused:
        game.generateFood(8, 5, lightGreen)


    game.drawAgents()
    game.drawFood()
    game.checkForFoodInSight()
    game.checkForColisions()

    pauseButton.draw(black, white, "pause", 20)
    if pauseButton.pressed(mouse, click) and released:
        paused = not paused
        released = False

    numberOfAgentsText.draw("population " + str(len(agents)), 20)
    averageSpeedText.draw("average speed " + str(round(averageSpeed, 2)), 20)
    averageSightRangeText.draw("average sight range " + str(round(averageSightRange, 2)), 20)

    pygame.display.flip()

