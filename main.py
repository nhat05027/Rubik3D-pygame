import pygame
import numpy as np
from math import *
import time

WHITE = (255, 255, 255)
RED = (245, 71, 72)
GREEN = (121, 212, 94)
BLUE = (49, 191, 243)
YELLOW = (247, 253, 4)
ORANGE = (251, 147, 0)
BLACK = (0, 0, 0)
COLOR = [BLACK, RED, ORANGE, BLUE, GREEN, WHITE, YELLOW]

WIDTH, HEIGHT = 600, 600
pygame.display.set_caption("3D")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
scale = 30
circle_pos = [WIDTH/2, HEIGHT/2]  # x, y
angle = 0.02
angleX = 0
angleY = 0
angleZ = 0
speedRotation = 0.005
isBusy = 0
c = 0

cube = [6, 6, 6, 6, 6, 6, 6, 6, 6, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5]

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

def drawCube(x, y, z, t, points, color):
    pygame.draw.polygon(screen, color,
                        (points[x], points[y], points[z], points[t]), 0)
    pygame.draw.polygon(screen, BLACK,
                        (points[x], points[y], points[z], points[t]), 1)
def drawFace(color):
    if color == 2:
        for i in range(3):
            k = i
            drawCube(k, k + 1, k + 5, k + 4, projected_points, COLOR[cube[38+i*3]])
            k = i + 4
            drawCube(k, k + 1, k + 5, k + 4, projected_points, COLOR[cube[37+i*3]])
            k = i + 8
            drawCube(k, k + 1, k + 5, k + 4, projected_points, COLOR[cube[36+i*3]])
    elif color == 1:
        for i in range(3):
            k = i + 48
            drawCube(k, k + 1, k + 5, k + 4, projected_points, COLOR[cube[18+i*3]])
            k = i + 52
            drawCube(k, k + 1, k + 5, k + 4, projected_points, COLOR[cube[19+i*3]])
            k = i + 56
            drawCube(k, k + 1, k + 5, k + 4, projected_points, COLOR[cube[20+i*3]])
    elif color == 3:
        for i in range(3):
            k = i
            drawCube(k, k + 1, k + 17, k + 16, projected_points, COLOR[cube[9+i*3]])
            k = i + 16
            drawCube(k, k + 1, k + 17, k + 16, projected_points, COLOR[cube[10+i*3]])
            k = i + 32
            drawCube(k, k + 1, k + 17, k + 16, projected_points, COLOR[cube[11+i*3]])
    elif color == 4:
        for i in range(3):
            k = i +12
            drawCube(k, k + 1, k + 17, k + 16, projected_points, COLOR[cube[29+i*3]])
            k = i + 28
            drawCube(k, k + 1, k + 17, k + 16, projected_points, COLOR[cube[28+i*3]])
            k = i + 44
            drawCube(k, k + 1, k + 17, k + 16, projected_points, COLOR[cube[27+i*3]])
    elif color == 6:
        for i in range(3):
            k = i*4
            drawCube(k, k + 4, k + 20, k + 16, projected_points, COLOR[cube[i]])
            k = i*4 + 16
            drawCube(k, k + 4, k + 20, k + 16, projected_points, COLOR[cube[i+3]])
            k = i*4 + 32
            drawCube(k, k + 4, k + 20, k + 16, projected_points, COLOR[cube[i+6]])

    elif color == 5:
        for i in range(3):
            k = i*4 +3
            drawCube(k, k + 4, k + 20, k + 16, projected_points, COLOR[cube[i+51]])
            k = i*4 + 19
            drawCube(k, k + 4, k + 20, k + 16, projected_points, COLOR[cube[i+48]])
            k = i*4 + 35
            drawCube(k, k + 4, k + 20, k + 16, projected_points, COLOR[cube[i+45]])

clock = pygame.time.Clock()
def pygameMain():
    global points,projected_points,angle,angleX,angleY,angleZ,zpos
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

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

    i = 0
    for point in points:
        rotated2d = point.reshape((3, 1))
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