import sys
import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("bouncing circles")
clock = pygame.time.Clock()

ballPos = pygame.Vector2(400, 300)
ballVel = pygame.Vector2(6, 0)
Gravity = 0.5
radius = 20

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ballVel.y = random.randint(-20, 20)
                ballVel.x = random.randint(-20, 20)

    # 1. Apply Physics
    ballVel.y += Gravity
    ballPos += ballVel

    # 2. Floor Collision (Bottom)
    if ballPos.y + radius >= 600:
        ballPos.y = 600 - radius
        ballVel.y *= -0.85  # Invert direction and reduce energy
        ballVel.x *= 0.99  # Apply ground friction

        # Stop micro-jittering when momentum is nearly gone
        if abs(ballVel.y) < 1:
            ballVel.y = 0

    # Ceiling Collision (Top)
    elif ballPos.y - radius <= 0:
        ballPos.y = radius
        ballVel.y *= -0.85

    # Wall Collisions (Left / Right)
    if ballPos.x + radius >= 800:
        ballPos.x = 800 - radius
        ballVel.x *= -0.8
    elif ballPos.x - radius <= 0:
        ballPos.x = radius
        ballVel.x *= -0.8

    # 3. Draw & Render
    screen.fill((40, 44, 52))
    pygame.draw.circle(screen, (255, 255, 255), (int(ballPos.x), int(ballPos.y)), radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
