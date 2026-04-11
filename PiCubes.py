import pygame
import pygame.gfxdraw
import numpy as np

run = True
pygame.init()
clock = pygame.time.Clock()

screen_width = 1400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont('Inter, Arial', 32, bold=True)

bMass = 100000
bSize = 100
bVel = -2

sMass = 1
sSize = 100
sVel = 0
sPos = np.array([200, 500], dtype=np.float64)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((0,0,0))

    if bMass != 1:
        bSize = (np.log10(bMass + 9)-1) * (200/5) + 100

    bPos = np.array([1000, 600-bSize], dtype=np.float64)


    pygame.draw.rect(screen, (255, 0, 0), (sPos[0], sPos[1], sSize, sSize))
    pygame.draw.rect(screen, (0, 0, 255), (bPos[0], bPos[1], bSize, bSize))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
