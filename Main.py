# Импортируем сам пайгейм и распаковываем его модули
import pygame
from pygame.locals import *

pygame.init()

from Constants import *

# Рисуем окошко игры
wSurface = pygame.display.set_mode(WINDOWSIZE, 0, 32)
pygame.display.set_caption("CoronaVirus eats people!!")

from CoronaVirus import CoronaVirus
from AntiBody import AntiBody
from Walls import Walls
from Dots import Dots
from Sound import Sound

# Создаем объекты для игры
background = pygame.image.load("bg.png").convert()
corona = CoronaVirus()
bacteria = [AntiBody()]
walls = Walls.createList(Walls())
small_dots = Dots.createListSmall(Dots())
large_dots = Dots.createListLarge(Dots())
clock = pygame.time.Clock()
pygame.mixer.music.load("bg_music.mp3")
pygame.mixer.music.set_volume(0.1)

# Открываем окно игры, включаем музыку
Sound.channel.play(Sound.opening)
wSurface.fill((0, 0, 0))
wSurface.blit(background, (100, 0))
wSurface.blit(corona.getScoreSurface(), (10, 10))
wSurface.blit(corona.getLivesSurface(), (WINDOWSIZE[0] - 200, 10))
for p in small_dots:
    wSurface.blit(Dots.images[0], (p[0] + Dots.shifts[0][0], p[1] + Dots.shifts[0][1]))
for p in large_dots:
    wSurface.blit(Dots.images[1], (p[0] + Dots.shifts[1][0], p[1] + Dots.shifts[1][1]))
for g in bacteria:
    wSurface.blit(g.surface, g.rect)
wSurface.blit(corona.surface, corona.rect)
pygame.display.update()
while True:
    if not pygame.mixer.get_busy():
        break

# Основной цикл игры
keepGoing_game = True
while keepGoing_game:
    # Один раунд
    keepGoing_round = True
    pygame.mixer.music.play(-1, 0.0)
    while keepGoing_round:

        # Обрабатываем событие
        for event in pygame.event.get():
            # Заканчиваем обработку
            if event.type == QUIT:
                keepGoing_game = keepGoing_round = False

            # Нажатия кнопок
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    corona.moveUp = True
                    corona.moveLeft = corona.moveDown = corona.moveRight = False
                    corona.direction = 0
                elif event.key == K_LEFT:
                    corona.moveLeft = True
                    corona.moveUp = corona.moveDown = corona.moveRight = False
                    corona.direction = 1
                elif event.key == K_DOWN:
                    corona.moveDown = True
                    corona.moveUp = corona.moveLeft = corona.moveRight = False
                    corona.direction = 2
                elif event.key == K_RIGHT:
                    corona.moveRight = True
                    corona.moveUp = corona.moveLeft = corona.moveDown = False
                    corona.direction = 3

            # Проверяем нажатие клавиши
            elif event.type == KEYUP:
                corona.moveUp = corona.moveLeft = corona.moveDown = corona.moveRight = False

        # Перемещаем вирус
        corona.move_c(walls)

        # Проверяем, должен ли телепортироваться вирус
        corona.teleport()

        # Организуем с помощью sprite повороты вируса, анимацию
        corona.getSurface()

        # Проверяяем, съел ли вирус точку, удаляем ее, если да
        Dots.check(Dots(), small_dots, large_dots, corona, bacteria)

        # Добавляем антитело при необходимости
        AntiBody.add(AntiBody(), bacteria)

        # Проверяем, вернулись ли голубые антитела в нормальное состояние
        for g in bacteria:
            if g.isBlue:
                g.checkBlue()

        # Располагаем антитела
        for g in bacteria:
            g.move(walls, corona)

        # Draw screen
        wSurface.fill((0, 0, 0))
        wSurface.blit(background, (100, 0))
        wSurface.blit(corona.getScoreSurface(), (10, 10))
        wSurface.blit(corona.getLivesSurface(), (WINDOWSIZE[0] - 200, 10))
        for p in small_dots:
            wSurface.blit(Dots.images[0], (p[0] + Dots.shifts[0][0], p[1] + Dots.shifts[0][1]))
        for p in large_dots:
            wSurface.blit(Dots.images[1], (p[0] + Dots.shifts[1][0], p[1] + Dots.shifts[1][1]))
        for g in bacteria:
            wSurface.blit(g.surface, g.rect)
        wSurface.blit(corona.surface, corona.rect)
        pygame.display.update()

        # Проверяем, не столкнулся вирус с антителом
        for g in bacteria[:]:
            if corona.rect.colliderect(g.rect):
                if not g.isBlue:
                    keepGoing_round = False
                    corona.lives -= 1
                    if corona.lives == 0:
                        keepGoing_game = False
                    else:
                        Sound.channel.play(Sound.death)
                    break
                else:  # Ghost is blue
                    del bacteria[bacteria.index(g)]
                    corona.score += 100
                    Sound.channel.play(Sound.eatGhost)


        # Проверяем, съедены ли все точки
        else:
            if len(small_dots) == 0 and len(large_dots) == 0:
                keepGoing_game = keepGoing_round = False
        clock.tick(FPS)
    # Убираем точки
    pygame.mixer.music.stop()
    corona.reset()
    for g in bacteria:
        g.reset()
    while True:
        if not pygame.mixer.get_busy():
            break

# Закрываем окно игры
wSurface.fill((0, 0, 0))
surface_temp = None

if corona.lives == 0:  # Проигрыш
    Sound.channel.play(Sound.lose)
    surface_temp = corona.getLosingSurface()

elif len(small_dots) == 0 and len(large_dots) == 0:  # Выигрыш
    Sound.channel.play(Sound.win)
    surface_temp = corona.getWinningSurface()

if surface_temp != None:  # Игрок проиграл или выиграл, но не вышел из игры
    rect_temp = surface_temp.get_rect()
    rect_temp.center = wSurface.get_rect().center
    wSurface.blit(surface_temp, rect_temp)
    pygame.display.update()

while True:
    if not pygame.mixer.get_busy():
        pygame.quit()
        break
