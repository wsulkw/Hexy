import random
import time
from math import cos, sin, sqrt

import pygame

pygame.font.init()

W, H = 1920, 1080

WIN = pygame.display.set_mode((W, H))
END = pygame.Surface((W, H))
END.fill((0, 0, 0))

f = pygame.font.SysFont('calibre', 100)
hs_f = pygame.font.SysFont('calibre', 50)

BLE = (145, 178, 199)
YLW = (243, 228, 150)
GRY = (54, 54, 54)
TXT = (88, 86, 97)

hexes = []

pi2 = 2 * 3.14

pos = ()
dec = 1

score = 0

gameover = False

restart = False

class Hexagon:
    def __init__(self):
        self.rot = random.randint(0, 360)
        self.size = 600
        self.points = []
        self.half = False

    def draw(self):
        global dec, hexes
        self.rot += .01
        if self.size <= 300 and not self.half and not gameover:
            self.half = True
            hexes.append(Hexagon())
        if self.size >= 0:
            self.size -= dec
        self.points = []
        for i in range(6):
            self.points.append(
                (cos(i / 6 * pi2 + self.rot) * self.size + W // 2, sin(i / 6 * pi2 + self.rot) * self.size + H // 2))

        pygame.draw.lines(WIN, GRY, False, self.points, 3)


def touching(points, c):
    for p in range(len(points) - 1):
        px = points[p + 1][0] - points[p][0]
        py = points[p + 1][1] - points[p][1]

        norm = px * px + py * py

        u = ((c[0] - points[p][0]) * px + (c[1] - points[p][1]) * py) / float(norm)
        if u > 1:
            u = 1
        elif u < 0:
            u = 0

        x = points[p][0] + u * px
        y = points[p][1] + u * py

        dx = x - c[0]
        dy = y - c[1]

        dist = (dx * dx + dy * dy) ** .5
        if 5 >= dist:
            return True

    return False


def player_coordinates(coordinates):
    coords = ((coordinates[0] - W // 2), (coordinates[1] - H // 2))

    if coords[0] == 0:
        return -1
    slope = coords[1] / coords[0]

    x = -(sqrt(2500 / (1 + slope ** 2)))
    if coords[0] >= 0:
        x = abs(x)
    y = slope * x

    return x + W // 2, y + H // 2


def end_animation():
    global dec
    while len(hexes) != 0:
        WIN.fill(BLE)
        pygame.draw.circle(WIN, YLW, pos, 5)
        for i in hexes.copy():
            dec = 3
            if i.size > 0:
                i.draw()
            else:
                hexes.remove(i)
        pygame.display.update()
    time.sleep(0.5)
    for i in range(int(max(W, H) * 0.15)):
        WIN.fill(BLE)
        pygame.draw.circle(WIN, YLW, pos, 5 * i)
        time.sleep(0.005)
        pygame.display.update()


def get_hs():
    with open('hs.txt', 'r+') as file:
        num = file.read()

        if score > int(num):
            file.close()

            with open('hs.txt', 'w') as file:
                file.truncate(0)
                file.write(str(score))
            num = score

        file.close()

    return num


def end_screen():
    global restart
    score_color = list(YLW)
    highscore_color = list(YLW)
    restart_color = list(YLW)
    for i in range(243):
        for i in range(len(score_color)):
            if score_color[i] > list(GRY)[i]:
                score_color[i] -= 1

        for i in range(len(highscore_color)):
            if highscore_color[i] > list(TXT)[i]:
                highscore_color[i] -= 1

        for i in range(len(restart_color)):
            if restart_color[i] > list(GRY)[i]:
                restart_color[i] -= 1

        WIN.fill(YLW)

        score_txt = f.render(f"{score}", True, tuple(score_color))
        score_txt_rect = score_txt.get_rect(center=(W // 2, H // 2 - 300))
        WIN.blit(score_txt, score_txt_rect)

        highscore_txt = hs_f.render(f"{get_hs()}", True, tuple(highscore_color))
        highscore_txt_rect = highscore_txt.get_rect(center=(W // 2, H // 2 - 200))
        WIN.blit(highscore_txt, highscore_txt_rect)

        restart_txt = hs_f.render("press r to restart", True, tuple(restart_color))
        restart_txt_rect = restart_txt.get_rect(center=(W // 2, H // 2))
        WIN.blit(restart_txt, restart_txt_rect)

        time.sleep(0.01)
        pygame.display.update()

    pygame.event.clear()
    restart = True


def redraw():
    global hexes, pos, run, score, dec, gameover
    dec += 1 * 10 ** -3

    WIN.fill(BLE)

    c = player_coordinates(pygame.mouse.get_pos())
    if c != -1:
        pos = c

    pygame.draw.circle(WIN, YLW, pos, 5)

    for i in hexes.copy():
        if i.size > 0:
            i.draw()
        else:
            hexes.remove(i)
            score += 1

    txt = f.render(f'{score}', False, TXT)
    WIN.blit(txt, (0, 0))

    if touching(hexes[0].points, pos):
        gameover = True
        end_animation()
        end_screen()

    pygame.display.update()


run = True
clock = pygame.time.Clock()
spawn = 300
hexes.append(Hexagon())

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if restart:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart = False
                    hexes.append(Hexagon())
                    gameover = False
                    score = 0


    if not gameover:
        redraw()

pygame.quit()
