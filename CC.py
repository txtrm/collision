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

# Modern Color Palette
BG_COLOR = (15, 15, 20)
WALL_COLOR = (255, 130, 0)       # Cyan/Azure
SMALL_BALL_COLOR = (255, 20, 0)  # Modern Pink/Red
BIG_BALL_COLOR = (255, 170, 0)    # Amber/Orange
TEXT_COLOR = (240, 240, 240)

# Wall settings
wallPos = np.array([screen_width / 2, screen_height / 2], dtype=np.float64)
wallRadius = 350

# Small circle settings
sCirclePos = np.array([screen_width / 2 - 40, screen_height / 2], dtype=np.float64)
sCircleRadius = 55
sMass = sCircleRadius * sCircleRadius
sCircleVel = np.array([np.random.uniform(-5, 5), np.random.uniform(-5, 5)], dtype=np.float64)

# Big circle settings
bCirclePos = np.array([screen_width / 2 + 40, screen_height / 2], dtype=np.float64)
bCircleRadius = 110
bMass = bCircleRadius * bCircleRadius
bCircleVel = np.array([np.random.uniform(-5, 5), np.random.uniform(-5, 5)], dtype=np.float64)
bCircleAlive = True

Health = 10000
Damage = 2
DamageName = 'None'

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Move Small Circle
    sCirclePos += sCircleVel

    # Move Big Circle if alive
    if bCircleAlive:
        bCirclePos += bCircleVel

    # Small circle vs Wall collision
    s_diff = sCirclePos - wallPos
    sDist = np.linalg.norm(s_diff)
    if sDist + sCircleRadius > wallRadius:
        n = s_diff / sDist
        sCirclePos = wallPos + (wallRadius - sCircleRadius) * n
        sCircleVel = sCircleVel - 2 * np.dot(sCircleVel, n) * n

    # Big circle vs Wall collision if alive
    if bCircleAlive:
        b_diff = bCirclePos - wallPos
        bDist = np.linalg.norm(b_diff)
        if bDist + bCircleRadius > wallRadius:
            n = b_diff / bDist
            bCirclePos = wallPos + (wallRadius - bCircleRadius) * n
            bCircleVel = bCircleVel - 2 * np.dot(bCircleVel, n) * n

    # Ball vs Ball collision logic
    if bCircleAlive:
        impactVec = sCirclePos - bCirclePos
        dist = np.linalg.norm(impactVec)

        if dist < sCircleRadius + bCircleRadius:
            Damage *= 2
            Health -= Damage
            DamageName = 'Damage:' + str(Damage * 2)
            
            if Health <= 0:
                bCircleAlive = False
            else:
                overlap = dist - (sCircleRadius + bCircleRadius)
                direction = (impactVec / dist) * (overlap * 0.5)
                sCirclePos -= direction
                bCirclePos += direction

                mSum = sMass + bMass
                vDiff = (sCircleVel - bCircleVel)
                commonFactor = np.dot(vDiff, impactVec) / (mSum * dist * dist)
                
                deltaVA = (2 * bMass * commonFactor) * impactVec
                deltaVB = (2 * sMass * commonFactor) * impactVec
                
                sCircleVel -= deltaVA
                bCircleVel += deltaVB

    # --- Drawing ---
    screen.fill(BG_COLOR)

    # Wall (Cyan border)
    pygame.gfxdraw.aacircle(screen, int(wallPos[0]), int(wallPos[1]), int(wallRadius), WALL_COLOR)
    pygame.gfxdraw.aacircle(screen, int(wallPos[0]), int(wallPos[1]), int(wallRadius)-1, WALL_COLOR)

    # Small Ball
    pygame.gfxdraw.aacircle(screen, int(sCirclePos[0]), int(sCirclePos[1]), int(sCircleRadius), SMALL_BALL_COLOR)
    pygame.gfxdraw.filled_circle(screen, int(sCirclePos[0]), int(sCirclePos[1]), int(sCircleRadius), SMALL_BALL_COLOR)
    sText = font.render(str(DamageName), True, TEXT_COLOR)
    sTextRect = sText.get_rect(center=(int(sCirclePos[0]), int(sCirclePos[1])))
    screen.blit(sText, sTextRect)

    # Big Ball
    if bCircleAlive:
        pygame.gfxdraw.aacircle(screen, int(bCirclePos[0]), int(bCirclePos[1]), int(bCircleRadius), BIG_BALL_COLOR)
        pygame.gfxdraw.filled_circle(screen, int(bCirclePos[0]), int(bCirclePos[1]), int(bCircleRadius), BIG_BALL_COLOR)
        bText = font.render(str(Health), True, (30, 30, 30)) # Darker text on light ball
        bTextRect = bText.get_rect(center=(int(bCirclePos[0]), int(bCirclePos[1])))
        screen.blit(bText, bTextRect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()