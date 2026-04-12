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
click_sfx = pygame.mixer.Sound("Click.wav")

DigitAmount = 2
bMass = 10000
bSize = 100
bVel = -5  # normal value: -5

sMass = 1
sSize = 100
sVel = 0
sPos = np.array([200, 500], dtype=np.float64)

collisions = 0
time_steps = 10000

bMass = 100 ** (DigitAmount-1)

if bMass != 1:
    bSize = (np.log10(bMass + 9)-1) * (200/5) + 100

bPos = np.array([1000, 600-bSize], dtype=np.float64)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((0,0,0))

    for _ in range(time_steps):
        if sPos[0] <= 0 and sVel < 0:
            click_sfx.play()
            sVel *= -1
            collisions += 1

        if bPos[0] <= sPos[0] + sSize and bVel < sVel:
            click_sfx.play()
            sumM = sMass + bMass
            difM = sMass - bMass
            sNewVel = (difM/sumM) * sVel + (2*bMass/sumM) * bVel
            bNewVel = (2*sMass/sumM) * sVel + (-difM/sumM) * bVel
            sVel = sNewVel
            bVel = bNewVel
            collisions += 1

        bPos[0] += bVel / time_steps
        sPos[0] += sVel / time_steps

    pygame.draw.rect(screen, (255, 0, 0), (sPos[0], sPos[1], sSize, sSize))
    pygame.draw.rect(screen, (0, 0, 255), (bPos[0], bPos[1], bSize, bSize))

    # Display collision count on screen
    text = font.render(f'Collisions: {collisions}', True, (255, 255, 255))
    text2 = font.render(f'Digits of Pi: {DigitAmount}', True, (150, 255, 150))
    screen.blit(text, (20, 20))
    screen.blit(text2, (20, 60))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
