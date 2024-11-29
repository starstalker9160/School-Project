import pygame as pg
from src.colours import *
from random import randint

class Functions():
    @staticmethod
    def in_range(x:float, y:float, r:float) -> bool:
        return all(y[i][0] - r < x[i][0] < y[i][0] + r for i in range(3))

    @staticmethod
    def hexToRgb(hex_: str) -> tuple:
        return tuple(int(hex_.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    def randColour(self) -> tuple:
        return [self.hexToRgb(P1), self.hexToRgb(P2), self.hexToRgb(P3), self.hexToRgb(P4)][randint(0, 3)]

    def matrixMult(self, a:list, b:list) -> list:
        rows_a = len(a)
        cols_a = len(a[0])
        cols_b = len(b[0])

        result = [[sum(a[i][k] * b[k][j] for k in range(cols_a)) for j in range(cols_b)] for i in range(rows_a)]
        return result


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
            pg.draw.rect(self.screen, Functions.hexToRgb(DISBL), self.rect)
        else:
            if self.toggle == 1:
                pg.draw.rect(self.screen, Functions.hexToRgb(GREEN), self.rect)
            else:
                pg.draw.rect(self.screen, Functions.hexToRgb(RED), self.rect)


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
