import pygame
import numpy as np
from math import *
import time
import random

WHITE = (255, 255, 255)
RED = (245, 71, 72)
GREEN = (121, 212, 94)
BLUE = (49, 191, 243)
YELLOW = (247, 253, 4)
ORANGE = (251, 147, 0)
BLACK = (0, 0, 0)
COLOR = [BLACK, RED, ORANGE, BLUE, GREEN, WHITE, YELLOW]

WIDTH, HEIGHT = 390, 680
pygame.display.set_caption("3D")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
scale = 30
circle_pos = [WIDTH/2, HEIGHT/2]  # x, y
angle = 0.02
angleX = 0
angleY = 0
angleZ = 0
speedRotation = 0.1
isBusy = 0
countStep = 0
c = 0
Text = ""

cube = [6, 6, 6, 6, 6, 6, 6, 6, 6, # Vàng (Upper)
        3, 3, 3, 3, 3, 3, 3, 3, 3, # Xanh biển (Left)
        1, 1, 1, 1, 1, 1, 1, 1, 1, # Đỏ (Front)
        4, 4, 4, 4, 4, 4, 4, 4, 4, # Xanh lá (Right)
        2, 2, 2, 2, 2, 2, 2, 2, 2,  # Cam (Behind)
        5, 5, 5, 5, 5, 5, 5, 5, 5]  # Trắng (Down)

matrixRotcw = np.array([[0] * 20] * 20)
CW = [6, 7, 0, 1, 2, 3, 4, 5, 17, 18, 19, 8, 9, 10, 11, 12, 13, 14, 15, 16]
for i, value in enumerate(CW):
    matrixRotcw[i][value] = 1
matrixRotccw = np.transpose(matrixRotcw)

matrixRotMidcw = np.array([[0] * 12] * 12)
CWM = [9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8]
for i, value in enumerate(CWM):
    matrixRotMidcw[i][CWM[i]] = 1
matrixRotMidccw = np.transpose(matrixRotMidcw)

rotU = np.array([0, 1, 2, 5, 8, 7, 6, 3, 38, 37, 36, 29, 28, 27, 20, 19, 18, 11, 10, 9])
rotD = np.array([45, 46, 47, 50, 53, 52, 51, 48, 24, 25, 26, 33, 34, 35, 42, 43, 44, 15, 16, 17])
rotF = np.array([18, 19, 20, 23, 26, 25, 24, 21, 6, 7, 8, 27, 30, 33, 47, 46, 45, 17, 14, 11])
rotB = np.array([36, 37, 38, 41, 44, 43, 42, 39, 2, 1, 0, 9, 12, 15, 51, 52, 53, 35, 32, 29])
rotR = np.array([27, 28, 29, 32, 35, 34, 33, 30, 8, 5, 2, 36, 39, 42, 53, 50, 47, 26, 23, 20])
rotL = np.array([9, 10, 11, 14, 17, 16, 15, 12, 0, 3, 6, 18, 21, 24, 45, 48, 51, 44, 41, 38])
rotE = np.array([12,13,14,21,22,23,30,31,32,39,40,41])
rotM = np.array([37,40,43,52,49,46,25,22,19,7,4,1])
rotS = np.array([3,4,5,28,31,34,50,49,48,16,13,10])
rotA = np.array([rotU, rotD, rotF, rotB, rotR, rotL])
rotC = np.array([rotM, rotE, rotS])

def cwNccw(key, direction):
    if direction == 0:
        T = [0] * 20
        for i in range(20):
            T[i] = cube[rotA[key][i]]
        T = matrixRotcw.dot(T)
        for i in range(20):
            cube[rotA[key][i]] = T[i]
    elif direction == 1:
        T = [0] * 20
        for i in range(20):
            T[i] = cube[rotA[key][i]]
        T = matrixRotccw.dot(T)
        for i in range(20):
            cube[rotA[key][i]] = T[i]
    elif direction == 2:
        T = [0] * 20
        for i in range(20):
            T[i] = cube[rotA[key][i]]
        T = matrixRotcw.dot(T)
        T = matrixRotcw.dot(T)
        for i in range(20):
            cube[rotA[key][i]] = T[i]
def cwNccwMid(key, direction):
    if direction == 0:
        T = [0] * 12
        for i in range(12):
            T[i] = cube[rotC[key][i]]
        T = matrixRotMidcw.dot(T)
        for i in range(12):
            cube[rotC[key][i]] = T[i]
    elif direction == 1:
        T = [0] * 12
        for i in range(12):
            T[i] = cube[rotC[key][i]]
        T = matrixRotMidccw.dot(T)
        for i in range(12):
            cube[rotC[key][i]] = T[i]
    elif direction == 2:
        T = [0] * 12
        for i in range(12):
            T[i] = cube[rotC[key][i]]
        T = matrixRotMidcw.dot(T)
        T = matrixRotMidcw.dot(T)
        for i in range(12):
            cube[rotC[key][i]] = T[i]
def rot2D(key):
    direction = 0
    if len(key) > 1:
        if key[1] == "'":
            direction = 1
        else:
            direction = 2
    if key[0] == "U":
        cwNccw(0, direction)
    elif key[0] == "D":
        cwNccw(1, direction)
    elif key[0] == "F":
        cwNccw(2, direction)
    elif key[0] == "B":
        cwNccw(3, direction)
    elif key[0] == "R":
        cwNccw(4, direction)
    elif key[0] == "L":
        cwNccw(5, direction)
    elif key[0] == "M":
        cwNccwMid(0, direction)
    elif key[0] == "E":
        cwNccwMid(1, direction)
    elif key[0] == "S":
        cwNccwMid(2, direction)
def algorithm(algo):
    global countStep,Text,speedRotation
    step = algo.split(" ")
    prevtime = time.time()
    for st in step:
        while time.time() - prevtime < speedRotation:
            pygameMain()
        rot2D(st)
        print(st, end=" ", flush=True)
        Text = Text + " " +st
        prevtime = time.time()
        countStep +=1

ff = ["U", "D", "R", "L", "F", "B"]
gg = ["", "'", "2"]
def randomRot():
    global Text
    scramble = ""
    g = 6
    t = 0
    while t < 25:
        i = random.randint(0, 5)
        j = random.randint(0, 2)
        if i != g:
            tx = ff[i] + gg[j]
            scramble = scramble + tx + " "
            g = i
            t +=1
    scramble = scramble[:-1]
    algorithm(scramble)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 13)
def message(text):
    global Text
    t = ""
    txt = text.split("*/")
    for i in range(len(txt)):
        lineMax = 56
        if len(txt[i]) > lineMax:
            if txt[i][lineMax-1] == " ":
                c = lineMax -1
            elif txt[i][lineMax-2] == " ":
                c = lineMax - 2
            else: c = lineMax
            x = txt[i][(c):]
            txt[i] = txt[i][0:(c)]
            if i == len(txt) - 1:
                txt.append(x)
            else: txt.insert(i+1, x)
    for i in range(len(txt)):
        t = t + "*/" + txt[i]
    Text = t[2:]
    if len(txt) == 0 :
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface,(10,0))
    if len(txt) > 0 :
        for i in range(len(txt)):
            textsurface = myfont.render(txt[i], False, (0, 0, 0))
            screen.blit(textsurface,(10,i*20))

vecpoint = [-3,-1,1,3]
points = []
zpos = [0]*64
# all the cube vertices

for z in vecpoint:
    for x in vecpoint:
        for y in vecpoint:
            points.append(np.array([x, y, z]))


projected_points = [
    [n, n] for n in range(len(points))
]

def draw(x, y, z, t, points, color):
    pygame.draw.polygon(screen, color,
                        (points[x], points[y], points[z], points[t]), 0)
    pygame.draw.polygon(screen, BLACK,
                        (points[x], points[y], points[z], points[t]), 1)
def drawFace(color):
    if color == 2:
        for i in range(3):
            k = i
            draw(k, k + 1, k + 5, k + 4, projected_points, COLOR[cube[38+i*3]])
            k = i + 4
            draw(k, k + 1, k + 5, k + 4, projected_points, COLOR[cube[37+i*3]])
            k = i + 8
            draw(k, k + 1, k + 5, k + 4, projected_points, COLOR[cube[36+i*3]])
    elif color == 1:
        for i in range(3):
            k = i + 48
            draw(k, k + 1, k + 5, k + 4, projected_points, COLOR[cube[18+i*3]])
            k = i + 52
            draw(k, k + 1, k + 5, k + 4, projected_points, COLOR[cube[19+i*3]])
            k = i + 56
            draw(k, k + 1, k + 5, k + 4, projected_points, COLOR[cube[20+i*3]])
    elif color == 3:
        for i in range(3):
            k = i
            draw(k, k + 1, k + 17, k + 16, projected_points, COLOR[cube[9+i*3]])
            k = i + 16
            draw(k, k + 1, k + 17, k + 16, projected_points, COLOR[cube[10+i*3]])
            k = i + 32
            draw(k, k + 1, k + 17, k + 16, projected_points, COLOR[cube[11+i*3]])
    elif color == 4:
        for i in range(3):
            k = i +12
            draw(k, k + 1, k + 17, k + 16, projected_points, COLOR[cube[29+i*3]])
            k = i + 28
            draw(k, k + 1, k + 17, k + 16, projected_points, COLOR[cube[28+i*3]])
            k = i + 44
            draw(k, k + 1, k + 17, k + 16, projected_points, COLOR[cube[27+i*3]])
    elif color == 6:
        for i in range(3):
            k = i*4
            draw(k, k + 4, k + 20, k + 16, projected_points, COLOR[cube[i]])
            k = i*4 + 16
            draw(k, k + 4, k + 20, k + 16, projected_points, COLOR[cube[i+3]])
            k = i*4 + 32
            draw(k, k + 4, k + 20, k + 16, projected_points, COLOR[cube[i+6]])

    elif color == 5:
        for i in range(3):
            k = i*4 +3
            draw(k, k + 4, k + 20, k + 16, projected_points, COLOR[cube[i+51]])
            k = i*4 + 19
            draw(k, k + 4, k + 20, k + 16, projected_points, COLOR[cube[i+48]])
            k = i*4 + 35
            draw(k, k + 4, k + 20, k + 16, projected_points, COLOR[cube[i+45]])

clock = pygame.time.Clock()
def pygameMain():
    global points,projected_points,angle,angleX,angleY,angleZ,zpos,Text
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            # if event.key == pygame.K_u:
            #     algorithm("U L R B2 F' U' B2")
            if event.key == pygame.K_r:
                prevTime = time.time()
                print("")
                print("Scramble: ", end=" ", flush=True)
                Text = "Scramble: "
                randomRot()
                Text = Text + "*/Step: " + str(countStep) + " (" + str(round(time.time() - prevTime, 5)) + "s)"

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        angleX += angle
    if keys[pygame.K_DOWN]:
        angleX -= angle
    if keys[pygame.K_RIGHT]:
        angleZ += angle
    if keys[pygame.K_LEFT]:
        angleZ -= angle
    if keys[pygame.K_PERIOD]:
        angleY += angle
    if keys[pygame.K_COMMA]:
        angleY -= angle

    screen.fill(WHITE)
    message(Text)

    i = 0
    for point in points:
        rotated2d = point.reshape((3, 1))
        rotation_z = np.array([
            [cos(angleZ), -sin(angleZ), 0],
            [sin(angleZ), cos(angleZ), 0],
            [0, 0, 1]
        ])
        rotation_y = np.array([
            [cos(angleY), 0, sin(angleY)],
            [0, 1, 0],
            [-sin(angleY), 0, cos(angleY)],
        ])
        rotation_x = np.array([
            [1, 0, 0],
            [0, cos(angleX), -sin(angleX)],
            [0, sin(angleX), cos(angleX)],
        ])
        rotated2d = np.dot(rotation_z, rotated2d)
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        x = rotated2d[0][0]
        y = rotated2d[1][0]
        z = rotated2d[2][0]
        xx = int(x * scale) + circle_pos[0]
        yy = int(y * scale) + circle_pos[1]
        zpos[i] = z
        # pygame.draw.circle(screen, RED, (xx, yy), 2)

        projected_points[i] = [xx, yy]
        i+= 1

    if zpos[0] >= 3 and zpos[0] >= zpos[12] and zpos[0] >= zpos[15] and zpos[0] >= zpos[3] and zpos[0] >= zpos[48] and \
            zpos[0] > zpos[51]:
        drawFace(2)
        drawFace(6)
        drawFace(3)
    elif zpos[3] >= 3 and zpos[3] >= zpos[12] and zpos[3] >= zpos[15] and zpos[3] >= zpos[0] and zpos[3] > zpos[48] and \
            zpos[3] >= zpos[51]:
        drawFace(2)
        drawFace(5)
        drawFace(3)
    elif zpos[12] >= 3 and zpos[12] >= zpos[0] and zpos[12] >= zpos[15] and zpos[12] >= zpos[3] and zpos[12] >= zpos[
        60] and zpos[12] > zpos[63]:
        drawFace(2)
        drawFace(6)
        drawFace(4)
    elif zpos[15] >= 3 and zpos[15] >= zpos[12] and zpos[15] >= zpos[0] and zpos[15] >= zpos[3] and zpos[15] > zpos[
        60] and zpos[15] >= zpos[63]:
        drawFace(2)
        drawFace(5)
        drawFace(4)
    elif zpos[48] >= 3 and zpos[48] >= zpos[60] and zpos[48] >= zpos[63] and zpos[48] >= zpos[51] and zpos[48] >= zpos[
        0] and zpos[48] > zpos[3]:
        drawFace(1)
        drawFace(6)
        drawFace(3)
    elif zpos[51] >= 3 and zpos[51] >= zpos[60] and zpos[51] >= zpos[48] and zpos[51] >= zpos[63] and zpos[51] > zpos[
        0] and zpos[51] >= zpos[3]:
        drawFace(1)
        drawFace(5)
        drawFace(3)
    elif zpos[60] >= 3 and zpos[60] >= zpos[63] and zpos[60] >= zpos[48] and zpos[60] >= zpos[51] and zpos[60] >= zpos[
        12] and zpos[60] > zpos[15]:
        drawFace(1)
        drawFace(6)
        drawFace(4)
    elif zpos[63] >= 3 and zpos[63] >= zpos[60] and zpos[63] >= zpos[48] and zpos[63] >= zpos[51] and zpos[63] > zpos[
        12] and zpos[63] >= zpos[15]:
        drawFace(1)
        drawFace(5)
        drawFace(4)

    pygame.display.update()

while True:
    pygameMain()