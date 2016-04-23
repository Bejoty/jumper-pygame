import pygame

from constants import GRAVITY


class Player():
    def __init__(self, x, platformHeight):
        self.width = 20
        self.height = 40
        self.x = x
        self.y = platformHeight - self.height
        self.speed = 5
        self.color = (124, 94, 56)
        self.jumpStrength = 15
        self.jumping = False
        self.vy = 0.0
        self.elevation = 0
        self.maxVY = 25

    def update(self):
        if self.jumping:
            self.elevation -= self.vy
            self.y += self.vy
            self.vy += GRAVITY
            if self.vy > self.maxVY:
                self.vy = self.maxVY

    def draw(self, surface, offset=0):
        pygame.draw.rect(surface, self.color, self.get_rect(offset))

    def get_rect(self, offset=0):
        return pygame.Rect(self.x, self.y + offset, self.width, self.height)

    def moveLeft(self):
        self.x -= self.speed

    def moveRight(self):
        self.x += self.speed

    def jump(self):
        self.jumping = True
        self.vy = -self.jumpStrength
