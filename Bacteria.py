

import pygame

import copy

from Character import Character
from Constants import *


class Bacteria(Character):
    images = [pygame.image.load("orange_0.png").convert(),
              pygame.image.load("cyan_0.png").convert()]
    for i in range(len(images)):
        images[i].set_colorkey((0, 0, 0))
    ISBLUE_TIME = int(10 * FPS)
    ADD_TIME = int(30 * FPS)
    add_time = ADD_TIME

    def __init__(self):
        super().__init__()
        self.surface = Bacteria.images[0]
        self.rect = self.surface.get_rect()
        self.rect.left = 315
        self.rect.top = 275
        self.speed = 1
        self.course = [0] * int(50 / self.speed)
        self.isBlue = False
        self.isBlue_time = 0

    def makeBlue(self):
        #  Меняет антитела на голубые.
        self.isBlue = True
        self.isBlue_time = Bacteria.ISBLUE_TIME  # количество кадров
        self.surface = Bacteria.images[1]
        self.course = []

    def makeNotBlue(self):
        
        #  Меняет голубое антитело на обычное.
        self.surface = Bacteria.images[0]
        self.course = []
        self.isBlue = False
        self.isBlue_time = 0

    def checkBlue(self):
        #  Проверяет, должно ли антитело вернуться в нормальное состояние, и делает это при необходимости.
        self.isBlue_time -= 1
        if self.isBlue_time <= 0:
            self.makeNotBlue()

    def reset(self):
        '''in - (self)
        Сбрасывает положение антитела и делает его обычным.'''
        self.makeNotBlue()
        self.rect.left = 315
        self.rect.top = 275
        self.course = [0] * int(50 / self.speed)

    def add(self, ghosts):
        '''in - (self, list of ghosts)
        Определяет, должно ли быть добавлено антитело, добавляет его в список и сбрасывает таймер добавления антитела.
        Вычитает/прибавляет время в таймере'''
        Bacteria.add_time -= 1
        if len(ghosts) == 0:
            if Bacteria.add_time > int(Bacteria.ADD_TIME / 10.0):
                Bacteria.add_time = int(Bacteria.ADD_TIME / 10.0)

        if Bacteria.add_time <= 0:
            ghosts.append(Bacteria())
            Bacteria.add_time = Bacteria.ADD_TIME

    def canMove_distance(self, direction, walls):
        '''in - (self, direction, list of walls)
        Определяет количество шагов, которые антитело может сделать в указанном направлении        .
        out - int'''
        #test = copy.deepcopy(self)
        counter = 0
        while True:
            if not Character.canMove(self, direction, walls):
                break
            Character.move(self, direction)
            counter += 1
        return counter

    def move(self, walls, pacman):
        '''in - (self, list of walls, pacman)
        Использует ИИ для перемещения антитела к вирусу.'''
        if len(self.course) > 0:
            if self.canMove(self.course[0], walls) or self.rect.colliderect(pygame.Rect((268, 248), (112, 64))):
                Character.move(self, self.course[0])
                del self.course[0]
            else:
                self.course = []

        else:
            xDistance = pacman.rect.left - self.rect.left
            yDistance = pacman.rect.top - self.rect.top
            choices = [-1, -1, -1, -1]

            if abs(xDistance) > abs(yDistance):  # горизонтально 1
                if xDistance > 0:  # право 1
                    choices[0] = 3
                    choices[3] = 1
                elif xDistance < 0:  # лево 1
                    choices[0] = 1
                    choices[3] = 3

                if yDistance > 0:  # вниз 2
                    choices[1] = 2
                    choices[2] = 0
                elif yDistance < 0:  # наверх 2
                    choices[1] = 0
                    choices[2] = 2
                else:  # yDistance == 0
                    if self.canMove_distance(2, walls) < self.canMove_distance(0, walls):  # вниз 2
                        choices[1] = 2
                        choices[2] = 0
                    elif self.canMove_distance(0, walls) < self.canMove_distance(2, walls):  # наверх 2
                        choices[1] = 0
                        choices[2] = 2

            elif abs(yDistance) >= abs(xDistance):  # вертикально 1
                if yDistance > 0:  # вниз 1
                    choices[0] = 2
                    choices[3] = 0
                elif yDistance < 0:  # наверх 1
                    choices[0] = 0
                    choices[3] = 2

                if xDistance > 0:  # право 2
                    choices[1] = 3
                    choices[2] = 1
                elif xDistance < 0:  # лево 2
                    choices[1] = 1
                    choices[2] = 3
                else:  # xDistance == 0
                    if self.canMove_distance(3, walls) < self.canMove_distance(1, walls):  # право 2
                        choices[1] = 3
                        choices[2] = 1
                    elif self.canMove_distance(1, walls) < self.canMove_distance(3, walls):  # лево 2
                        choices[1] = 1
                        choices[2] = 3

            if self.isBlue:
                choices.reverse()
            choices_original = choices[:]
            for i, x in enumerate(choices[:]):
                if x == -1 or (not Character.canMove(self, x, walls)):
                    del choices[choices.index(x)]

            if len(choices) > 0:
                Character.move(self, choices[0])
                if choices_original.index(choices[0]) >= 2:  # если ход 3-й или 4-й выбор
                    global FPS
                    for i in range(int(FPS * 1.5)):
                        self.course.append(choices[0])
