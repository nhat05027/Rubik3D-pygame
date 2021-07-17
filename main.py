import pygame
import numpy as np
from math import *
import time
import random

speedRotation = 0.5
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
countStep = 0
c = 0
Text = ""

cube = [6, 6, 6, 6, 6, 6, 6, 6, 6, # Vàng (Upper)
        3, 3, 3, 3, 3, 3, 3, 3, 3, # Xanh biển (Left)
        1, 1, 1, 1, 1, 1, 1, 1, 1, # Đỏ (Front)
        4, 4, 4, 4, 4, 4, 4, 4, 4, # Xanh lá (Right)
        2, 2, 2, 2, 2, 2, 2, 2, 2,  # Cam (Behind)
        5, 5, 5, 5, 5, 5, 5, 5, 5]  # Trắng (Down)

#12 edge
edge = np.array([
    [7,19], #uf up-front
    [3,10], #ul up-left
    [5,28], #ur up-right
    [1,37], #ub up-back
    [21,14], #fl front-left
    [23,30], #fr front-right
    [41,12], #bl back-lèt
    [39,32], #br back-right
    [46,25], #df down-front
    [48,16], #dl down-left
    [50,34], #dr down-right
    [52,43], #db down back
])
#8 corner
corner = np.array([
    [6,18,11], #ufl
    [8,20,27], #ufr
    [0,38,9], #ubl
    [2,36,29], #ubr
    [45,24,17], #dfl
    [47,26,33], #dfr
    [51,44,15], #dbl
    [53,42,35], #dbr
])

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
    g = 999
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

def whiteCross():
    global countStep
    listf = [2,4,1,3] # cam-xanhlá-đỏ-xanhbiển
    for i in listf:
        if cube[edge[11][0]] == i and cube[edge[11][1]] == 5:
            algorithm("B R' U' R B2")
        elif cube[edge[0][0]] == i and cube[edge[0][1]] == 5:
            algorithm("U2 B' R' U' R B2")
        elif cube[edge[0][0]] == 5 and cube[edge[0][1]] == i:
            algorithm("U2 B2")
        elif cube[edge[1][0]] == i and cube[edge[1][1]] == 5:
            algorithm("U B' R' U' R B2")
        elif cube[edge[1][0]] == 5 and cube[edge[1][1]] == i:
            algorithm("U B2")
        elif cube[edge[2][0]] == i and cube[edge[2][1]] == 5:
            algorithm("U' B' R' U' R B2")
        elif cube[edge[2][0]] == 5 and cube[edge[2][1]] == i:
            algorithm("U' B2")
        elif cube[edge[3][0]] == i and cube[edge[3][1]] == 5:
            algorithm("B' R' U' R B2")
        elif cube[edge[3][0]] == 5 and cube[edge[3][1]] == i:
            algorithm("B2")
        elif cube[edge[4][0]] == i and cube[edge[4][1]] == 5:
            algorithm("L2 B L2")
        elif cube[edge[4][0]] == 5 and cube[edge[4][1]] == i:
            algorithm("D L D'")
        elif cube[edge[5][0]] == i and cube[edge[5][1]] == 5:
            algorithm("R2 B' R2")
        elif cube[edge[5][0]] == 5 and cube[edge[5][1]] == i:
            algorithm("D' R' D")
        elif cube[edge[6][0]] == i and cube[edge[6][1]] == 5:
            algorithm("B")
        elif cube[edge[6][0]] == 5 and cube[edge[6][1]] == i:
            algorithm("L U L' B2")
        elif cube[edge[7][0]] == i and cube[edge[7][1]] == 5:
            algorithm("B'")
        elif cube[edge[7][0]] == 5 and cube[edge[7][1]] == i:
            algorithm("R' U' R B2")
        elif cube[edge[8][0]] == i and cube[edge[8][1]] == 5:
            algorithm("F2 U2 B' R' U' R B2")
        elif cube[edge[8][0]] == 5 and cube[edge[8][1]] == i:
            algorithm("F2 U2 B2")
        elif cube[edge[9][0]] == i and cube[edge[9][1]] == 5:
            algorithm("L B")
        elif cube[edge[9][0]] == 5 and cube[edge[9][1]] == i:
            algorithm("L2 U B2")
        elif cube[edge[10][0]] == i and cube[edge[10][1]] == 5:
            algorithm("R' B'")
        elif cube[edge[10][0]] == 5 and cube[edge[10][1]] == i:
            algorithm("R2 U' B2")
        algorithm("D")

def whiteFull():
    global countStep
    lists = [4,3,6,8]
    for i in lists:
        if cube[corner[0][0]] == 5 and cube[corner[0][1]]*cube[corner[0][2]] == i:
            algorithm("U' R U' R' F' U2 F")
        elif cube[corner[0][1]] == 5 and cube[corner[0][0]]*cube[corner[0][2]] == i:
            algorithm("U F' U2 F")
        elif cube[corner[0][2]] == 5 and cube[corner[0][0]]*cube[corner[0][1]] == i:
            algorithm("R U' R'")
        elif cube[corner[1][0]] == 5 and cube[corner[1][1]]*cube[corner[1][2]] == i:
            algorithm("R U' R' F' U2 F")
        elif cube[corner[1][1]] == 5 and cube[corner[1][0]]*cube[corner[1][2]] == i:
            algorithm("U R U' R'")
        elif cube[corner[1][2]] == 5 and cube[corner[1][0]]*cube[corner[1][1]] == i:
            algorithm("U' F' U F")
        elif cube[corner[2][0]] == 5 and cube[corner[2][1]]*cube[corner[2][2]] == i:
            algorithm("U2 R U' R' F' U2 F")
        elif cube[corner[2][1]] == 5 and cube[corner[2][0]]*cube[corner[2][2]] == i:
            algorithm("R U2 R'")
        elif cube[corner[2][2]] == 5 and cube[corner[2][0]]*cube[corner[2][1]] == i:
            algorithm("F' U2 F")
        elif cube[corner[3][0]] == 5 and cube[corner[3][1]]*cube[corner[3][2]] == i:
            algorithm("U R U' R' F' U2 F")
        elif cube[corner[3][1]] == 5 and cube[corner[3][0]]*cube[corner[3][2]] == i:
            algorithm("F' U F")
        elif cube[corner[3][2]] == 5 and cube[corner[3][0]]*cube[corner[3][1]] == i:
            algorithm("U' R U2 R'")
        elif cube[corner[4][0]] == 5 and cube[corner[4][1]]*cube[corner[4][2]] == i:
            algorithm("F U F' R U2 R'")
        elif cube[corner[4][1]] == 5 and cube[corner[4][0]]*cube[corner[4][2]] == i:
            algorithm("F U F2 U2 F")
        elif cube[corner[4][2]] == 5 and cube[corner[4][0]]*cube[corner[4][1]] == i:
            algorithm("F U' F' R U' R'")
        elif cube[corner[5][0]] == 5 and cube[corner[5][1]]*cube[corner[5][2]] == i:
            pass
        elif cube[corner[5][1]] == 5 and cube[corner[5][0]]*cube[corner[5][2]] == i:
            algorithm("F' U2 F R U2 R'")
        elif cube[corner[5][2]] == 5 and cube[corner[5][0]]*cube[corner[5][1]] == i:
            algorithm("F' U F U' F' U F")
        elif cube[corner[6][0]] == 5 and cube[corner[6][1]]*cube[corner[6][2]] == i:
            algorithm("B' U B R U2 R'")
        elif cube[corner[6][1]] == 5 and cube[corner[6][0]]*cube[corner[6][2]] == i:
            algorithm("B' U' B R U' R'")
        elif cube[corner[6][2]] == 5 and cube[corner[6][0]]*cube[corner[6][1]] == i:
            algorithm("B' U B F' U2 F")
        elif cube[corner[7][0]] == 5 and cube[corner[7][1]]*cube[corner[7][2]] == i:
            algorithm("B U B' U R U' R'")
        elif cube[corner[7][1]] == 5 and cube[corner[7][0]]*cube[corner[7][2]] == i:
            algorithm("R' U R F' U F")
        elif cube[corner[7][2]] == 5 and cube[corner[7][0]]*cube[corner[7][1]] == i:
            algorithm("R' U' R2 U2 R'")
        algorithm("D")

def secondLayer():
    global countStep
    lists = [1, 3, 2, 4]
    lists1 = [4, 1, 3, 2]
    for i in range(4):
        k = lists[i]
        j = lists1[i]
        if cube[edge[0][0]] == k and cube[edge[0][1]] == j:
            algorithm("U2 F' U F U R U' R'")
        elif cube[edge[0][0]] == j and cube[edge[0][1]] == k:
            algorithm("U R U' R' U' F' U F")
        elif cube[edge[1][0]] == k and cube[edge[1][1]] == j:
            algorithm("U F' U F U R U' R'")
        elif cube[edge[1][0]] == j and cube[edge[1][1]] == k:
            algorithm("R U' R' U' F' U F")
        elif cube[edge[2][0]] == k and cube[edge[2][1]] == j:
            algorithm("U' F' U F U R U' R'")
        elif cube[edge[2][0]] == j and cube[edge[2][1]] == k:
            algorithm("U2 R U' R' U' F' U F")
        elif cube[edge[3][0]] == k and cube[edge[3][1]] == j:
            algorithm("F' U F U R U' R'")
        elif cube[edge[3][0]] == j and cube[edge[3][1]] == k:
            algorithm("U' R U' R' U' F' U F")
        elif cube[edge[4][0]] == k and cube[edge[4][1]] == j:
            algorithm("F U' F' U' L' U L U2 R U' R' U' F' U F")
        elif cube[edge[4][0]] == j and cube[edge[4][1]] == k:
            algorithm("F U' F' U' L' U L U' F' U F U R U' R'")
        elif cube[edge[5][0]] == k and cube[edge[5][1]] == j:
            pass
        elif cube[edge[5][0]] == j and cube[edge[5][1]] == k:
            algorithm("R U' R' U' F' U F U' R U' R' U' F' U F")
        elif cube[edge[6][0]] == k and cube[edge[6][1]] == j:
            algorithm("L U' L' U' B' U B U2 F' U F U R U' R'")
        elif cube[edge[6][0]] == j and cube[edge[6][1]] == k:
            algorithm("L U' L' U' B' U B U R U' R' U' F' U F")
        elif cube[edge[7][0]] == k and cube[edge[7][1]] == j:
            algorithm("R' U R U B U' B' U2 F' U F U R U' R'")
        elif cube[edge[7][0]] == j and cube[edge[7][1]] == k:
            algorithm("R' U R U B U' B' U R U' R' U' F' U F")
        algorithm("E D")

def oll2look():
    global countStep
    # cross yellow
    if cube[1] != 6 and cube[3] != 6 and cube[5] != 6 and cube[7] != 6:
        algorithm("F R U R' U' F' F S R U R' U' F' S'")
    elif cube[1] == 6 and cube[3] != 6 and cube[5] != 6 and cube[7] == 6:
        algorithm("U F R U R' U' F'")
    elif cube[1] != 6 and cube[3] == 6 and cube[5] == 6 and cube[7] != 6:
        algorithm("F R U R' U' F'")
    elif cube[1] == 6 and cube[3] == 6 and cube[5] != 6 and cube[7] != 6:
        algorithm("U2 F S R U R' U' F' S'")
    elif cube[1] == 6 and cube[3] != 6 and cube[5] == 6 and cube[7] != 6:
        algorithm("U F S R U R' U' F' S'")
    elif cube[1] != 6 and cube[3] == 6 and cube[5] != 6 and cube[7] == 6:
        algorithm("U' F S R U R' U' F' S'")
    elif cube[1] != 6 and cube[3] != 6 and cube[5] == 6 and cube[7] == 6:
        algorithm("F S R U R' U' F' S'")

    countY = 0
    for i in [0,2,6,8]:
        if cube[i] == 6:
            countY +=1
    # pi and h
    if countY == 0:
        # h
        if cube[9] ==6 and cube[11] == 6 and cube[18] != 6 and cube[20] != 6 and cube[27] == 6 and cube[29] == 6 and cube[36] != 6 and cube[38] != 6:
            algorithm("R U R' U R U' R' U R U2 R'")
        elif cube[9] !=6 and cube[11] != 6 and cube[18] == 6 and cube[20] == 6 and cube[27] != 6 and cube[29] != 6 and cube[36] == 6 and cube[38] == 6:
            algorithm("U R U R' U R U' R' U R U2 R'")
        # pi
        else:
            for i in range(4):
                if cube[9] == 6 and cube[11] == 6 and cube[18] != 6 and cube[20] == 6 and cube[27] != 6 and cube[29] != 6 and cube[36] == 6 and cube[38] != 6:
                    algorithm("R U2 R2 U' R2 U' R2 U2 R")
                    break
                else:
                    algorithm("U")

    # sune and antisune
    elif countY == 1:
        for i in range(4):
            #sune
            if cube[6] == 6 and cube[20] == 6:
                algorithm("R U R' U R U2 R'")
                break
            #anti sune
            elif cube[2] == 6 and cube[18] == 6:
                algorithm("R U2 R' U' R U' R'")
                break
            else:
                algorithm("U")

    # L, T and U
    elif countY == 2:
        for i in range(4):
            # L
            if cube[0] == 6 and cube[8] == 6 and cube[18] == 6 and cube[29] == 6:
                algorithm("F R' F' R M U R U' R' M'")
                break
            elif cube[0] == 6 and cube[8] == 6 and cube[11] == 6 and cube[36] == 6:
                algorithm("U2 F R' F' R M U R U' R' M'")
                break
            # T
            elif cube[2] == 6 and cube[8] == 6 and cube[18] == 6 and cube[38] == 6:
                algorithm("R M U R' U' R' M' F R F'")
                break
            # U
            elif cube[0] == 6 and cube[2] == 6 and cube[18] == 6 and cube[20] == 6:
                algorithm("R2 D R' U2 R D' R' U2 R'")
                break
            else:
                algorithm("U")

def pll2look():
    global countStep
    if cube[10] == 1:
        algorithm("U'")
    elif cube[28] == 1:
        algorithm("U")
    elif cube[37] == 1:
        algorithm("U2")
    # corner
    list1 = np.array([[1,2,3],[3,0,2],[0,3,1],[2,1,0]])
    lists = [3, 4, 6, 8]
    liste = [0]*4
    for i in range(4):
        for j in range(4):
            if cube[corner[i][1]]*cube[corner[i][2]] == lists[j]:
                liste[i] = j
    algorithm("U'")
    for i in [0,1,3,2]:
        if liste[i] != i:
            if liste[list1[i][0]] == i:
                algorithm("R U R' U' R' F R2 U' R' U' R U R' F'")
                liste[list1[i][0]] = liste[i]
                liste[i] = i
                algorithm("U")
            elif liste[list1[i][1]] == i:
                algorithm("U' R U R' U' R' F R2 U' R' U' R U R' F' U")
                liste[list1[i][1]] = liste[i]
                liste[i] = i
                algorithm("U")
            elif liste[list1[i][2]] == i:
                algorithm("F R U' R' U' R U R' F' R U R' U' R' F R F'")
                liste[list1[i][2]] = liste[i]
                liste[i] = i
                algorithm("U")
        else:
            algorithm("U")

    if cube[9] == 1:
        algorithm("U'")
    elif cube[27] == 1:
        algorithm("U")
    elif cube[36] == 1:
        algorithm("U2")

    # edge
    el = [10, 19, 28, 37]
    elc = [3, 1, 4, 2]
    elc1 = [0] * 4
    ca = 0
    for i in range(4):
        elc1[i] = cube[el[i]]
        if cube[el[i]] == elc[i]:
            ca += 1
    if ca == 0:
        if elc1[0] == 4:
            algorithm("M2 U M2 U2 M2 U M2")
        elif elc1[0] == 2:
            algorithm("U' M' U M2 U M2 U M' U2 M2 U")
        else:
            algorithm("M' U M2 U M2 U M' U2 M2")
    elif ca == 1:
        algox = ["U", "U2", "U'", ""]
        algoy = ["U'", "U2", "U", ""]
        fx = [2, 3, 1, 4]
        fy = [2, 3, 0, 1]
        for i in range(4):
            if elc1[i] == elc[i]:
                if algox[i] != "":
                    algorithm(algox[i])
                if elc1[fy[i]] == fx[i]:
                    algorithm("R U' R U R U R U' R' U' R2")
                    if algoy[i] != "":
                        algorithm(algoy[i])
                    break
                else:
                    algorithm("R2 U R U R' U' R' U' R' U R'")
                    if algoy[i] != "":
                        algorithm(algoy[i])
                    break
    if cube[10] == 1:
        algorithm("U'")
    elif cube[28] == 1:
        algorithm("U")
    elif cube[37] == 1:
        algorithm("U2")

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
    global points,projected_points,angle,angleX,angleY,angleZ,zpos,Text,countStep
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_r:
                prevTime = time.time()
                print("")
                print("Scramble: ", end=" ", flush=True)
                countStep = 0
                Text = "Scramble: "
                randomRot()
                # Text = Text + "*/Step: " + str(countStep) + " (" + str(round(time.time() - prevTime, 5)) + "s)"
            if event.key == pygame.K_f:
                countStep = 0
                prevTime = time.time()
                print("")
                print("Chữ thập trắng: ", end=" ", flush=True)
                Text = Text+"*/White Cross: "
                whiteCross()
                print("")
                print("Tầng 1: ", end=" ", flush=True)
                Text = Text+"*/First Layer: "
                whiteFull()
                print("")
                print("Tầng 2: ", end=" ", flush=True)
                Text = Text+"*/Second Layer: "
                secondLayer()
                print("")
                print("OLL: ", end=" ", flush=True)
                Text = Text+"*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/OLL: "
                oll2look()
                print("")
                print("PLL: ", end=" ", flush=True)
                Text = Text+"*/PLL: "
                pll2look()
                print("")
                print("Số bước: ", countStep)
                print("Thời gian: ", round(time.time()-prevTime,5), "giây")
                Text = Text+"*/Step: " + str(countStep) + " (" + str(round(time.time()-prevTime,5)) +"s)"
            if event.key == pygame.K_g:
                countStep = 0
                prevTime = time.time()
                print("")
                print("Chữ thập trắng: ", end=" ", flush=True)
                Text = Text+"*/White Cross: "
                whiteCross()
                Text = Text + "*/Step: " + str(countStep) + " (" + str(round(time.time() - prevTime, 5)) + "s)"
            if event.key == pygame.K_h:
                countStep = 0
                prevTime = time.time()
                print("")
                print("Tầng 1: ", end=" ", flush=True)
                Text = "First Layer: "
                whiteFull()
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