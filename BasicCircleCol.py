import pygame
import pygame.gfxdraw
import numpy as np

run = True
pygame.init()

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

font = pygame.font.SysFont('Inter, Arial', 32, bold=True)
clock = pygame.time.Clock()

circlePos = np.array([screen_width / 2, screen_height / 2], dtype=np.float64)
circleRadius = 55
circleVel = np.array([10.0, 0.0], dtype=np.float64)

gravity = 0.5
time_steps = 10

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for _ in range(time_steps):
        # Apply gravity scaled by sub-steps
        circleVel[1] += gravity / time_steps

        # Side walls with position correction
        if (circlePos[0] - circleRadius) < 0:
            circlePos[0] = circleRadius
            circleVel[0] *= -0.8
        elif (circlePos[0] + circleRadius) > screen_width:
            circlePos[0] = screen_width - circleRadius
            circleVel[0] *= -0.8

        # Floor and Ceiling with position correction
        if (circlePos[1] - circleRadius) < 0:
            circlePos[1] = circleRadius
            circleVel[1] *= -0.8
        elif (circlePos[1] + circleRadius) > screen_height:
            circlePos[1] = screen_height - circleRadius
            circleVel[1] *= -0.8

        # Update position scaled by sub-steps
        circlePos += circleVel / time_steps

    screen.fill((0,0,0))
    pygame.gfxdraw.filled_circle(screen, int(circlePos[0]), int(circlePos[1]), int(circleRadius), (255, 0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()