import pygame
import pygame.gfxdraw
import numpy as np
import math

run = True
pygame.init()
pygame.display.set_caption("Gravity Simulation")

screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))

font = pygame.font.SysFont('Inter, Arial', 32, bold=True)
clock = pygame.time.Clock()

p1Pos = np.array([960, 540], dtype=np.float64)
p1Vel = np.array([0.0, 0.0], dtype=np.float64)
p1Radius = 112
p1Mass = p1Radius*10
p1Img = pygame.transform.scale(pygame.image.load("Jupiter.png"), (p1Radius*2, p1Radius*2))

p2Pos = np.array([960+p1Radius+300, 540], dtype=np.float64)
p2Vel = np.array([-2.0, -2.0], dtype=np.float64)
p2Radius = p1Radius/11.2
p2Mass = p2Radius*10
p2Img = pygame.transform.scale(pygame.image.load("Earth.png"), (p2Radius*2, p2Radius*2))

# Universal Gravitational Constant (scaled for simulation visibility)
# The actual G is 6.674e-11, but a larger value is used here for visual effect in a pixel-based simulation.
G_CONSTANT = 3
time_steps = 10  # More steps = more stable orbits
softening = 10   # Prevents "slingshot" when planets are very close

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for _ in range(time_steps):
        # 1. Calculate the shared force based on CURRENT positions
        dx = p1Pos[0] - p2Pos[0]
        dy = p1Pos[1] - p2Pos[1]
        distance_sq = dx**2 + dy**2 + softening**2
        distance = math.sqrt(distance_sq)

        # Calculate the single gravitational force using the universal constant
        force = (G_CONSTANT * p1Mass * p2Mass) / distance_sq

        # 2. Calculate unit vector components (direction)
        # atan2(dy, dx) gives the angle from p2 to p1
        angle = math.atan2(dy, dx)
        fx = force * math.cos(angle)
        fy = force * math.sin(angle)

        # 3. Apply forces to both velocities (f = ma -> a = f/m)
        # Planet 2 moves toward Planet 1 (force components fx, fy)
        p2Vel[0] += (fx / p2Mass) / time_steps
        p2Vel[1] += (fy / p2Mass) / time_steps

        # Planet 1 moves toward Planet 2 (opposite force components -fx, -fy)
        p1Vel[0] -= (fx / p1Mass) / time_steps
        p1Vel[1] -= (fy / p1Mass) / time_steps

        # 4. Update both positions simultaneously
        p1Pos += p1Vel / time_steps
        p2Pos += p2Vel / time_steps

    # Calculate the Center of Mass (Barycenter) to use as the camera focus
    com = (p1Pos * p1Mass + p2Pos * p2Mass) / (p1Mass + p2Mass)
    camera_offset = np.array([screen_width / 2, screen_height / 2]) - com

    screen.fill((0,0,0))

    screen.blit(p1Img, (p1Pos[0], p1Pos[1] - p1Radius))
    screen.blit(p2Img, (p2Pos[0], p2Pos[1] - p2Radius))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()