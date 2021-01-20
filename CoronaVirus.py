import pygame

from Character import Character
from Constants import *


class CoronaVirus(Character):

    def __init__(self):
        super().__init__()
        self.reset()
        self.speed = 5
        self.score = 0
        self.lives = 3

    def reset(self):
        #  восстанавливает положение, скорость и тд
        self.images = [pygame.image.load("бактерия первая.png").convert(), \
                       pygame.image.load("бактерия вторая.png").convert(), \
                       pygame.image.load("бактерия третья.png").convert()]
        self.surface = self.images[0]
        self.isFirstPic = True
        self.image = 0
        self.rect = self.surface.get_rect()
        # размещаем на холсте, не двигается
        self.rect.left = 315
        self.rect.top = 315
        self.direction = 0
        self.moveUp = self.moveLeft = self.moveDown = self.moveRight = False
        #  картинки

    def getSurface(self):
        #  задаем карусель картинок
        self.image += 1
        if self.image == 3:
            self.isFirstPic = not self.isFirstPic
            self.image = 0

        if self.direction == 0:
            self.surface = self.images[self.isFirstPic]
        elif self.direction == 1:
            self.surface = pygame.transform.rotate(self.images[self.isFirstPic], 90)
        elif self.direction == 2:
            self.surface = pygame.transform.rotate(self.images[self.isFirstPic], 180)
        elif self.direction == 3:
            self.surface = pygame.transform.rotate(self.images[self.isFirstPic], 270)

    def move_c(self, walls):
        #  проверка возможности движения и движение
        if self.moveUp and self.canMove(0, walls):
            self.move(0)
        if self.moveLeft and self.canMove(1, walls):
            self.move(1)
        if self.moveDown and self.canMove(2, walls):
            self.move(2)
        if self.moveRight and self.canMove(3, walls):
            self.move(3)

    def teleport(self):
        '''in - (self)
        Determines if pacman collided with one of teleport locations and moves him.'''
        if self.rect.colliderect(pygame.Rect((100, 256), (6, 48))):
            self.rect.left += 400
        if self.rect.colliderect(pygame.Rect((549, 256), (6, 48))):
            self.rect.left -= 400
        if self.rect.left < 100:
            self.rect.left += 400
        if self.rect.left > 550:
            self.rect.left -= 400

    def getScoreSurface(self):
        '''in - (self)
        Creates surface object of pacman's score.
        out - Surface'''
        global YELLOW
        return pygame.font.SysFont(None, 48).render("Score: " + str(self.score), True, YELLOW)

    def getLivesSurface(self):
        '''in - (self)
        Creates surface object of pacman's lives.
        out - Surface'''
        global YELLOW
        surface = pygame.font.SysFont(None, 48).render("Lives:          ", True, YELLOW)
        x = 110
        for i in range(self.lives):
            surface.blit(self.images[2], (x, 5))
            x += 25
        return surface

    def getWinningSurface(self):
        '''in - (self)
        Creates surface object of 'You Win!',
        out - Surface'''
        global YELLOW
        return pygame.font.SysFont(None, 72).render("You Win!", True, YELLOW)

    def getLosingSurface(self):
        '''in - (self)
        Creates surface object of 'You Lose...'.
        out - Surface'''
        global YELLOW
        return pygame.font.SysFont(None, 72).render("You Lose...", True, YELLOW)
