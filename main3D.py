import pygame
import numpy as np
from math import *
import time
import random

speedRotation = 0.0005
WHITE = (255, 255, 255)
RED = (245, 71, 72)
GREEN = (121, 212, 94)
BLUE = (49, 191, 243)
YELLOW = (247, 253, 4)
ORANGE = (251, 147, 0)
BLACK = (0, 0, 0)
COLOR = [BLACK, RED, ORANGE, BLUE,
         GREEN, WHITE, YELLOW]

WIDTH, HEIGHT = 390, 680
pygame.display.set_caption("3D")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
scale = 30
circle_pos = [WIDTH/2, HEIGHT/2]  # x, y
angle = 0.02
angleX = 0
angleY = 0
angleZ = 0
isBusy = 0
c = 0
countStep = 0
Text = ""
#########################################
vecpoint = np.array([[-3,-1],[-1,1],[1,3]])
boxs = []
projected_boxs = []
zpos = np.array([[0]*8]*27)
points = []
for i in range(3):
    for j in range(3):
        for k in range(3):
            for x in range(2):
                for y in range(2):
                    for z in range(2):
                        points.append(np.array([vecpoint[i][x], vecpoint[j][y], vecpoint[k][z]]))
            boxs.append(points)
            projected_boxs.append(points)
            points = []
#########################################
cube = [6, 6, 6, 6, 6, 6, 6, 6, 6, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5]
matrixRotcw = np.array([[0] * 20] * 20)
CW = [6, 7, 0, 1, 2, 3, 4, 5, 17, 18, 19, 8, 9, 10, 11, 12, 13, 14, 15, 16]
matrixRotMidcw = np.array([[0] * 12] * 12)
CWM = [9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8]
for i in range(20):
    matrixRotcw[i][CW[i]] = 1
for i in range(12):
    matrixRotMidcw[i][CWM[i]] = 1
matrixRotccw = np.transpose(matrixRotcw)
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
    if direction == -2: direction = 2
    if direction == -1:
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
    if direction == -2: direction = 2
    if direction == -1:
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
#################################################################################
L = [0,1,2,3,4,5,6,7,8]  # x
M = [9,10,11,12,13,14,15,16,17]  # x
R = [18,19,20,21,22,23,24,25,26]  # x
U = [0,1,2,9,10,11,18,19,20]  # y
E = [3,4,5,12,13,14,21,22,23]  # y
D = [6,7,8,15,16,17,24,25,26]  # y
B = [0,3,6,9,12,15,18,21,24]  # z
S = [1,4,7,10,13,16,19,22,25]  # z
F = [2,5,8,11,14,17,20,23,26]  # z
allBlock = [L, M, R, U, E, D, B, S, F]
def rotation(key,dir):
    global boxs,points,isBusy,allBlock,zpos
    if dir == -2 : dir = 2
    angleRot = pi/2 * dir
    if isBusy == 0:
        isBusy = 1
        c = 0
        prevtime = time.time()
        maxSt = 60 * abs(dir)
        while c < maxSt:
            while time.time() - prevtime < speedRotation:
                pygameMain()
            for i in range(9):
                for j in range(8):
                    rotated2d = boxs[allBlock[key][i]][j].reshape((3, 1))
                    rotation_z = np.array([
                        [cos(angleRot/maxSt), -sin(angleRot/maxSt), 0],
                        [sin(angleRot/maxSt), cos(angleRot/maxSt), 0],
                        [0, 0, 1],
                    ])
                    rotation_y = np.array([
                        [cos(angleRot/maxSt), 0, sin(angleRot/maxSt)],
                        [0, 1, 0],
                        [-sin(angleRot/maxSt), 0, cos(angleRot/maxSt)],
                    ])
                    rotation_x = np.array([
                        [1, 0, 0],
                        [0, cos(angleRot/maxSt), -sin(angleRot/maxSt)],
                        [0, sin(angleRot/maxSt), cos(angleRot/maxSt)],
                    ])
                    if key < 3:
                        rotated2d = np.dot(rotation_x, rotated2d)
                    elif key < 6:
                        rotated2d = np.dot(rotation_y, rotated2d)
                    else:
                        rotated2d = np.dot(rotation_z, rotated2d)

                    x = rotated2d[0][0]
                    y = rotated2d[1][0]
                    z = rotated2d[2][0]
                    # zpos[i] = z
                    points.append(np.array([x, y, z]))

                boxs[allBlock[key][i]] = points
                points = []
            c += 1
            prevtime = time.time()
        for i in range(9):
            for j in range(8):
                rotated2d = boxs[allBlock[key][i]][j].reshape((3, 1))
                rotation_z = np.array([
                    [cos(-angleRot), -sin(-angleRot), 0],
                    [sin(-angleRot), cos(-angleRot), 0],
                    [0, 0, 1],
                ])
                rotation_y = np.array([
                    [cos(-angleRot), 0, sin(-angleRot)],
                    [0, 1, 0],
                    [-sin(-angleRot), 0, cos(-angleRot)],
                ])
                rotation_x = np.array([
                    [1, 0, 0],
                    [0, cos(-angleRot), -sin(-angleRot)],
                    [0, sin(-angleRot), cos(-angleRot)],
                ])
                if key < 3:
                    rotated2d = np.dot(rotation_x, rotated2d)
                elif key < 6:
                    rotated2d = np.dot(rotation_y, rotated2d)
                else:
                    rotated2d = np.dot(rotation_z, rotated2d)

                x = rotated2d[0][0]
                y = rotated2d[1][0]
                z = rotated2d[2][0]
                zpos[i][j] = z
                points.append(np.array([x, y, z]))

            boxs[allBlock[key][i]] = points
            points = []
        isBusy = 0

blockFace = np.array([[0,1,3,2],[0,1,5,4],[0,2,6,4],[1,3,7,5],[2,3,7,6],[4,5,7,6]])
colorStiker =  [[0,4,13,0],[1,4,99,0],[2,4,99,0],[3,4,99,0],[4,4,99,0],[5,4,99,0],
                [1,10,4,0],[0,10,99,0],[2,10,99,0],[3,10,99,0],[4,10,99,0],[5,10,99,0],
                [2,12,40,0],[0,12,99,0],[1,12,99,0],[3,12,99,0],[4,12,99,0],[5,12,99,0],
                [3,14,22,0],[0,14,99,0],[1,14,99,0],[2,14,99,0],[4,14,99,0],[5,14,99,0],
                [4,16,49,0],[0,16,99,0],[1,16,99,0],[2,16,99,0],[3,16,99,0],[5,16,99,0],
                [5,22,31,0],[0,22,99,0],[1,22,99,0],[2,22,99,0],[3,22,99,0],[4,22,99,0],
                #### 6 block chính giữa
                [0,0,9,0],[1,0,0,0],[2,0,38,0],[3,0,99,0],[4,0,99,0],[5,0,99,0],
                [0,2,11,0],[1,2,6,0],[2,2,99,0],[3,2,18,0],[4,2,99,0],[5,2,99,0],
                [0,6,15,0],[1,6,99,0],[2,6,44,0],[3,6,99,0],[4,6,51,0],[5,6,99,0],
                [0,8,17,0],[1,8,99,0],[2,8,99,0],[3,8,24,0],[4,8,45,0],[5,8,99,0],
                [0,18,99,0],[1,18,2,0],[2,18,36,0],[3,18,99,0],[4,18,99,0],[5,18,29,0],
                [0,20,99,0],[1,20,8,0],[2,20,99,0],[3,20,20,0],[4,20,99,0],[5,20,27,0],
                [0,24,99,0],[1,24,99,0],[2,24,42,0],[3,24,99,0],[4,24,53,0],[5,24,35,0],
                [0,26,99,0],[1,26,99,0],[2,26,99,0],[3,26,26,0],[4,26,47,0],[5,26,33,0],
                #### 8 block góc
                [0,1,10,0],[1,1,3,0],[2,1,99,0],[3,1,99,0],[4,1,99,0],[5,1,99,0],
                [0,3,12,0],[1,3,99,0],[2,3,41,0],[3,3,99,0],[4,3,99,0],[5,3,99,0],
                [0,5,14,0],[1,5,99,0],[2,5,99,0],[3,5,21,0],[4,5,99,0],[5,5,99,0],
                [0,7,16,0],[1,7,99,0],[2,7,99,0],[3,7,99,0],[4,7,48,0],[5,7,99,0],
                [0,9,99,0],[1,9,1,0],[2,9,37,0],[3,9,99,0],[4,9,99,0],[5,9,99,0],
                [0,11,99,0],[1,11,7,0],[2,11,99,0],[3,11,19,0],[4,11,99,0],[5,11,99,0],
                [0,15,99,0],[1,15,99,0],[2,15,43,0],[3,15,99,0],[4,15,52,0],[5,15,99,0],
                [0,17,99,0],[1,17,99,0],[2,17,99,0],[3,17,25,0],[4,17,46,0],[5,17,99,0],
                [0,19,99,0],[1,19,5,0],[2,19,99,0],[3,19,99,0],[4,19,99,0],[5,19,28,0],
                [0,21,99,0],[1,21,99,0],[2,21,39,0],[3,21,99,0],[4,21,99,0],[5,21,32,0],
                [0,23,99,0],[1,23,99,0],[2,23,99,0],[3,23,23,0],[4,23,99,0],[5,23,30,0],
                [0,25,99,0],[1,25,99,0],[2,25,99,0],[3,25,99,0],[4,25,50,0],[5,25,34,0],
                ##### 12 block cạnh
              ]

def updateZ():
    global colorStiker
    for i, face in enumerate(colorStiker):
        sumZ = zpos[face[1]][blockFace[face[0]][0]] \
               + zpos[face[1]][blockFace[face[0]][1]] \
               + zpos[face[1]][blockFace[face[0]][2]] \
               + zpos[face[1]][blockFace[face[0]][3]]
        colorStiker[i][3] = sumZ
    colorStiker.sort(key=lambda x: x[3])

def rot3D(key):
    direction = -1
    if len(key) > 1:
        if key[1] == "'":
            direction = 1
        else:
            direction = 2
    if key[0] == "U":
        rotation(3, direction)
        cwNccw(0, direction)
    elif key[0] == "D":
        rotation(5, -direction)
        cwNccw(1, direction)
    elif key[0] == "F":
        rotation(8, -direction)
        cwNccw(2, direction)
    elif key[0] == "B":
        rotation(6, direction)
        cwNccw(3, direction)
    elif key[0] == "R":
        rotation(2, -direction)
        cwNccw(4, direction)
    elif key[0] == "L":
        rotation(0, direction)
        cwNccw(5, direction)
    elif key[0] == "M":
        rotation(1, -direction)
        cwNccwMid(0, direction)
    elif key[0] == "E":
        rotation(4, -direction)
        cwNccwMid(1, direction)
    elif key[0] == "S":
        rotation(7, -direction)
        cwNccwMid(2, direction)

def draw(x, y, z, t, points, color):
    pygame.draw.polygon(screen, color,
                        (points[x], points[y], points[z], points[t]), 0)
    pygame.draw.polygon(screen, BLACK,
                        (points[x], points[y], points[z], points[t]), 1)

def algorithm(algo):
    global countStep,Text,speedRotation
    step = algo.split(" ")
    for st in step:
        rot3D(st)
        print(st, end=" ", flush=True)
        Text = Text + " " +st
        countStep +=1

clock = pygame.time.Clock()
def pygameMain():
    global points,projected_boxs,boxs,angle,angleX,angleY,angleZ,zpos
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if isBusy == 0:
                if event.key == pygame.K_f:
                    algorithm("U L F B D2 U'")
                if event.key == pygame.K_g:
                    rot3D("F")
                if event.key == pygame.K_h:
                    rot3D("S")

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

    for i in range(len(boxs)):
        for j in range(len(boxs[0])):
            rotated2d = boxs[i][j].reshape((3, 1))
            rotation_z = np.array([
                [cos(angleZ), -sin(angleZ), 0],
                [sin(angleZ), cos(angleZ), 0],
                [0, 0, 1],
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
            zpos[i][j] = z
            points.append(np.array([xx, yy]))
            # pygame.draw.circle(screen, RED, (xx, yy), 2)
        projected_boxs[i] = points
        points = []

    updateZ()
    for i, face in enumerate(colorStiker):
        if face[2] == 99:
            color = BLACK
        else: color = COLOR[cube[face[2]]]
        draw(blockFace[face[0]][0],blockFace[face[0]][1],
             blockFace[face[0]][2],blockFace[face[0]][3],
             projected_boxs[face[1]],color)

    pygame.display.update()
while True:
    pygameMain()