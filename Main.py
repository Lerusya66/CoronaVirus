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
from Pattern import Pattern
from Dots import Dots
from Sound import Sound

# Создаем объекты для игры
background = pygame.image.load("bg.png").convert()
corona = CoronaVirus()
antybody = [AntiBody()]
walls = Pattern().walls
small_dots = Dots().createListSmall()
large_dots = Dots().createListLarge()
clock = pygame.time.Clock()
pygame.mixer.music.load("bg_music.mp3")
pygame.mixer.music.set_volume(0.1)

# Открываем окно игры, включаем музыку
Dot_s = Dots()
Sound.channel.play(Sound.opening)
wSurface.fill((0, 0, 0))
wSurface.blit(background, (100, 0))
wSurface.blit(corona.getScoreSurface(), (10, 10))
wSurface.blit(corona.getLivesSurface(), (WINDOWSIZE[0] - 200, 10))
for p in small_dots:
    wSurface.blit(Dot_s.images[0], (p[0] + Dot_s.shifts[0][0], p[1] + Dot_s.shifts[0][1]))
for p in large_dots:
    wSurface.blit(Dot_s.images[1], (p[0] + Dot_s.shifts[1][0], p[1] + Dot_s.shifts[1][1]))
for cur_anti in antybody:
    wSurface.blit(cur_anti.surface, cur_anti.rect)
wSurface.blit(corona.surface, corona.rect)
pygame.display.update()
while True:
    if not pygame.mixer.get_busy():
        break

# Основной цикл игры
game_is_on = True
while game_is_on:
    # Один раунд
    round_is_on = True
    pygame.mixer.music.play(-1, 0.0)
    while round_is_on:

        # Обрабатываем событие
        for event in pygame.event.get():
            # Заканчиваем обработку
            if event.type == QUIT:
                game_is_on = round_is_on = False

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
        for anti in antybody:
            anti.teleport()

        # Организуем с помощью sprite повороты вируса, анимацию
        corona.getSurface()
        Dot_s = Dots()
        # Проверяяем, съел ли вирус точку, удаляем ее, если да
        Dot_s.check(small_dots, large_dots, corona, antybody)

        # Добавляем антитело при необходимости
        AntiBody.add(AntiBody(), antybody)

        # Проверяем, вернулись ли голубые антитела в нормальное состояние
        for cur_anti in antybody:
            if cur_anti.isBlue:
                cur_anti.checkBlue()

        # Располагаем антитела
        for cur_anti in antybody:
            cur_anti.move_antibody(walls, corona)

        # Draw screen
        Dot_s = Dots()
        wSurface.fill((0, 0, 0))
        wSurface.blit(background, (100, 0))
        wSurface.blit(corona.getScoreSurface(), (10, 10))
        wSurface.blit(corona.getLivesSurface(), (WINDOWSIZE[0] - 200, 10))
        for p in small_dots:
            wSurface.blit(Dot_s.images[0], (p[0] + Dot_s.shifts[0][0], p[1] + Dot_s.shifts[0][1]))
        for p in large_dots:
            wSurface.blit(Dot_s.images[1], (p[0] + Dot_s.shifts[1][0], p[1] + Dot_s.shifts[1][1]))
        for cur_anti in antybody:
            wSurface.blit(cur_anti.surface, cur_anti.rect)
        wSurface.blit(corona.surface, corona.rect)
        pygame.display.update()

        # Проверяем, не столкнулся вирус с антителом
        for cur_anti in antybody[:]:
            if corona.rect.colliderect(cur_anti.rect):
                if not cur_anti.isBlue:
                    round_is_on = False
                    corona.lives -= 1
                    if corona.lives == 0:
                        game_is_on = False
                    else:
                        Sound.channel.play(Sound.death)
                    break
                else:  # Ghost is blue
                    del antybody[antybody.index(cur_anti)]
                    corona.score += 100
                    Sound.channel.play(Sound.eatGhost)


        # Проверяем, съедены ли все точки
        else:
            if len(small_dots) == 0 and len(large_dots) == 0:
                game_is_on = round_is_on = False
        clock.tick(FPS)
    # Убираем точки
    pygame.mixer.music.stop()
    corona.reset()
    for cur_anti in antybody:
        cur_anti.reset()
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
