import pygame


class Pattern:
    def __init__(self):

        pattern = []
        # pattern.append(pygame.Rect((x, y), (width, height)))
        pattern.append(pygame.Rect((99, 47), (447, 7)))
        pattern.append(pygame.Rect((99, 54), (7, 152)))
        pattern.append(pygame.Rect((99, 199), (7, 63)))
        pattern.append(pygame.Rect((267, 248), (7, 64)))
        pattern.append(pygame.Rect((139, 87), (48, 31)))
        pattern.append(pygame.Rect((219, 87), (63, 31)))
        pattern.append(pygame.Rect((364, 87), (65, 31)))
        pattern.append(pygame.Rect((460, 87), (49, 31)))
        pattern.append(pygame.Rect((99, 199), (86, 8)))
        pattern.append(pygame.Rect((139, 152), (48, 16)))
        pattern.append(pygame.Rect((316, 55), (16, 65)))
        pattern.append(pygame.Rect((540, 55), (7, 153)))
        pattern.append(pygame.Rect((460, 200), (88, 7)))
        pattern.append(pygame.Rect((460, 152), (49, 16)))
        pattern.append(pygame.Rect((412, 152), (16, 112)))
        pattern.append(pygame.Rect((363, 200), (49, 16)))
        pattern.append(pygame.Rect((268, 152), (112, 16)))
        pattern.append(pygame.Rect((316, 166), (16, 50)))
        pattern.append(pygame.Rect((220, 152), (16, 112)))
        pattern.append(pygame.Rect((235, 200), (49, 16)))
        pattern.append(pygame.Rect((100, 256), (88, 8)))
        pattern.append(pygame.Rect((460, 256), (89, 8)))
        pattern.append(pygame.Rect((460, 296), (89, 8)))
        pattern.append(pygame.Rect((460, 352), (88, 8)))
        pattern.append(pygame.Rect((460, 296), (9, 64)))
        pattern.append(pygame.Rect((412, 296), (17, 65)))
        pattern.append(pygame.Rect((220, 296), (16, 64)))
        pattern.append(pygame.Rect((460, 199), (8, 64)))
        pattern.append(pygame.Rect((99, 296), (88, 8)))
        pattern.append(pygame.Rect((179, 296), (9, 64)))
        pattern.append(pygame.Rect((99, 352), (88, 8)))
        pattern.append(pygame.Rect((99, 352), (8, 193)))
        pattern.append(pygame.Rect((107, 440), (33, 16)))
        pattern.append(pygame.Rect((99, 536), (448, 9)))
        pattern.append(pygame.Rect((540, 352), (8, 193)))
        pattern.append(pygame.Rect((507, 439), (34, 16)))
        pattern.append(pygame.Rect((267, 248), (40, 8)))
        pattern.append(pygame.Rect((339, 248), (41, 8)))
        pattern.append(pygame.Rect((460, 200), (9, 64)))
        pattern.append(pygame.Rect((139, 392), (49, 17)))
        pattern.append(pygame.Rect((170, 406), (17, 51)))
        pattern.append(pygame.Rect((219, 392), (64, 17)))
        pattern.append(pygame.Rect((363, 392), (65, 17)))
        pattern.append(pygame.Rect((459, 392), (49, 17)))
        pattern.append(pygame.Rect((460, 406), (17, 51)))
        pattern.append(pygame.Rect((411, 440), (17, 50)))
        pattern.append(pygame.Rect((364, 488), (145, 17)))
        pattern.append(pygame.Rect((266, 440), (114, 17)))
        pattern.append(pygame.Rect((315, 358), (16, 51)))
        pattern.append(pygame.Rect((219, 440), (16, 50)))
        pattern.append(pygame.Rect((138, 488), (145, 17)))
        pattern.append(pygame.Rect((371, 248), (9, 64)))
        pattern.append(pygame.Rect((267, 304), (113, 7)))
        pattern.append(pygame.Rect((267, 344), (112, 16)))
        pattern.append(pygame.Rect((315, 455), (16, 50)))
        # Стена блокирует центр игрового поля, создает ловушку для антител
        pattern.append(pygame.Rect((268, 248), (112, 64)))
        self.walls = pattern[:]
