import pygame
from src.colours import *
from random import randint

class Functions():
    @staticmethod
    def randColour():
        return [RED, YELLOW, GREEN, INDIGO, BLUE, MAGENTA][randint(0, 5)]

    @staticmethod
    def in_range(x, y, r):
        return all(y[i][0] - r < x[i][0] < y[i][0] + r for i in range(3))

    def matrixMult(self, a, b):
        r_A = len(a)
        c_A = len(a[0])
        c_B = len(b[0])

        c = [[0 for r in range(c_B)] for c in range(r_A)]

        for x in range(r_A):
            for y in range(c_B):
                for z in range(c_A):
                    c[x][y] += a[x][z] * b[z][y]

        return c


class ToggleButt():
    def __init__(self, rect, screen, toggle, disabled):
        self.rect = rect
        self.screen = screen
        self.toggle = toggle
        self.disabled = disabled

    def clicked(self):
        if self.toggle == 0:
            self.toggle = 1
            return True
        else:
            self.toggle = 0
            return False

    def draw(self):
        if self.disabled == True:
            pygame.draw.rect(self.screen, D_GRAY, self.rect)
        else:
            if self.toggle == 1:
                pygame.draw.rect(self.screen, GREEN, self.rect)
            else:
                pygame.draw.rect(self.screen, RED, self.rect)


class Importer():
    def loadObj(f):
        try:
            content = open(f, 'r').read()
        except TypeError:
            print("An error has occured.")
            exit()
        
        lines = content.split('\n')
        verts = []
        faces = []

        for line in lines:
            if line.startswith('f '):
                line = line.split(' ')
                line.pop(0)
                line_list = []
                for index, face in enumerate(line):
                    if face == '':
                        line.remove(face)
                    else:
                        face = face.replace('//', '/')
                        line[index] = list(map(int, face.split('/')))[0] - 1
                        line_list.append(line[index])

                faces.append(line_list)

            elif line.startswith('v '):
                line = line.replace('  ', ' ')
                line = line.split(' ')
                line.pop(0)
                line = list(map(float, line))
                for index, item in enumerate(line):
                    line[index] = [item]
                verts.append(line)

        return (verts, faces)
