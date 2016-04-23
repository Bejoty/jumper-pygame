import random
import sys

import pygame
import pygame.event as GAME_EVENTS
import pygame.locals as GAME_GLOBALS

from constants import (
    BLACK,
    GRAVITY,
)

from player import Player
from screen import Screen

pygame.init()
clock = pygame.time.Clock()
screen = Screen()
surface = pygame.display.set_mode(screen.dimensions)

pygame.font.init()
font = pygame.font.SysFont("Arial", 25)

pygame.display.set_caption(screen.caption)

debug = {}

leftPressed = False
rightPressed = False

player = Player(screen.width / 2, screen.height)

springs = []

bg0 = pygame.image.load('assets/bg0.png').convert()
bg1 = pygame.image.load('assets/bg1.png').convert_alpha()
bg2 = pygame.image.load('assets/bg2.png').convert_alpha()
bg3 = pygame.image.load('assets/bg3.png').convert_alpha()

offset = 0
cameraY = 0

for i in range(20):
    boop = i % 4
    if boop == 1 or boop == 3:
        x = random.randint(screen.width/3, 2*screen.width/3 - 30)
    elif boop == 0:
        x = random.randint(0, screen.width/3 - 30)
    else:
        x = random.randint(2*screen.width/3, screen.width - 30)
    # y = random.randint(0, screen.height - player.height - 30)
    y = screen.height - (i+1) * 100 - 40
    springs.append(pygame.Rect(x, y, 30, 30))


def draw():
    surface.fill((51, 22, 0))
    surface.blit(bg0, (0, 0))
    surface.blit(bg1, (0, cameraY * 0.3))
    surface.blit(bg2, (0, cameraY * 0.5))
    surface.blit(bg3, (0, cameraY * 0.8))
    surface.blit(bg1, (0, cameraY * 0.3 - screen.height))
    surface.blit(bg2, (0, cameraY * 0.5 - screen.height))
    surface.blit(bg3, (0, cameraY * 0.8 - screen.height))
    surface.blit(bg2, (0, cameraY * 0.5 - 2*screen.height))
    surface.blit(bg3, (0, cameraY * 0.8 - 2*screen.height))

    player.draw(surface, cameraY)

    for spring in springs:
        pygame.draw.rect(surface, (94, 124, 56), spring.move(0, cameraY))


def update():
    if leftPressed:
        player.moveLeft()
        if player.x < 0:
            player.x = 0
    if rightPressed:
        player.moveRight()
        if player.x + player.width > screen.width:
            player.x = screen.width - player.width

    player.update()

    if player.elevation <= 0:
        diff = 0 - player.elevation
        player.elevation = 0
        player.y -= diff
        player.jumping = False
        player.vy = 0

    global offset
    global cameraY
    cameraBanding = (1.0 * abs(player.y + player.height + cameraY - screen.height/2) / (screen.height/2)) ** 2
    if player.y + cameraY < screen.height / 2:
        offset = player.maxVY * cameraBanding
    elif cameraY > 0:
        offset = -player.maxVY * cameraBanding

    cameraY += offset
    if cameraY < 0:
        cameraY = 0

    # Collision detection
    playerRect = player.get_rect().move(0, cameraY)
    for spring in springs:
        if playerRect.colliderect(spring.move(0, cameraY)):
            player.jump()

    debug['offset'] = int(offset)
    debug['cameraY'] = int(cameraY)


def quitGame():
    pygame.quit()
    sys.exit()


def debugDisplay():
    debug['elevation'] = int(player.elevation / 10)
    debug['player.y'] = int(player.y)
    y = 25
    for entry, value in debug.iteritems():
        surface.blit(font.render(entry + ": " + str(value), -1, (255, 255, 255)), (25, y))
        y += 25


while True:
    for event in GAME_EVENTS.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()
            if event.key == pygame.K_LEFT:
                leftPressed = True
            if event.key == pygame.K_RIGHT:
                rightPressed = True
            if event.key == pygame.K_UP:
                if player.elevation == 0:
                    player.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                leftPressed = False
            if event.key == pygame.K_RIGHT:
                rightPressed = False

        if event.type == GAME_GLOBALS.QUIT:
            quitGame()

    update()
    draw()
    debugDisplay()

    clock.tick(60)
    pygame.display.update()
