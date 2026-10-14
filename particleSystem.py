import sys
import random
import pygame
import math

pygame.init()
w = 1920
h = 930
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Particle System")
clock = pygame.time.Clock()
targetFps = 60
particles = []
fontObj = pygame.font.Font('Arial Black.ttf', 32)
radius = 3

gravity = 0.5

class Particle:
    def __init__(self):
        self.position = pygame.Vector2(500,200)
        self.vel = pygame.Vector2(0,0)
        self.radius = radius

    def update(self, delta_time):
        self.vel.y += gravity
        self.position += self.vel

        if self.position.y + radius >= h:
            self.position.y = h - radius
            self.vel.y *= -0.85  # Invert direction and reduce energy
            self.vel.x *= 0.99  # Apply ground friction

            # Stop micro-jittering when momentum is nearly gone
            if abs(self.vel.y) < 1:
                self.vel.y = 0

        # Ceiling Collision (Top)
        elif self.position.y - radius <= 0:
            self.position.y = radius
            self.vel.y *= -0.85

        # Wall Collisions (Left / Right)
        if self.position.x + radius >= w:
            self.position.x = w - radius
            self.vel.x *= -0.8
        elif self.position.x - radius <= 0:
            self.position.x = radius
            self.vel.x *= -0.8

    def resolve_particle_collisions(particles):
        # Check every unique pair of particles (O(N^2) approach)
        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):
                p1 = particles[i]
                p2 = particles[j]

                # Vector from p1 to p2
                axis = p2.position - p1.position
                distance = axis.length()
                rsum = p1.radius + p2.radius

                # if distance <= rsum:
                    

for i in range(1):
    particles.append(Particle())

running = True
while running:
    deltaTime = clock.tick(targetFps) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for Particle in particles:
        Particle.update(deltaTime)
        pygame.draw.circle(screen, (255,255,255), Particle.position, radius, width=0)

    fps = clock.get_fps()
    fpsText = fontObj.render(f"FPS: {fps:.0f}", True, (255, 255, 255))
    screen.blit(fpsText, (15, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()