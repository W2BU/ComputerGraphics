import pygame as pg
import numpy as np
from matrixfunctions import *
import ast

class Object:
    def __init__(self, render):
        self.render = render
        self.vertices = np.array([[0, 2, 0, 1], [2, 0, 0, 1], [0, 0, 1, 1], [0, 1, 2, 1]])
        self.faces = np.array([(0, 1, 2, 3)])
        self.coloredFaces = [(pg.Color('Black'), face) for face in self.faces]
        self.font = pg.sysfont.SysFont('Arial', 30, bold = True)
        self.label = ''
        self.vertices = np.append(self.vertices, self.interpolate(), 0)
        
    def interpolate(self):
        points = 20 # per line
        res = []
        for i in range(points + 1):
            for j in range(points + 1):
                u = i / points
                v = j / points
                point = self.vertices[0] * (1 - u) * (1 - v) + self.vertices[1] * (1 - u) * v + self.vertices[2] * u * (1 - v) + self.vertices[3] * u * v
                res.append([point[0], point[1], point[2], point[3]])
        return np.array([np.array(v) for v in res])
                
    def draw(self):
        self.project()

    def project(self):
        vertices = self.vertices @ self.render.camera.cameraMatrix()
        vertices = vertices @ self.render.projection.projectionMatrix
        vertices /= vertices[:, -1].reshape(-1,1)
        vertices = vertices @ self.render.projection.toScreenMatrix
        vertices = vertices[:, :2]

        for index, coloredFace in enumerate(self.coloredFaces):
            color, face = coloredFace
            polygon = vertices[face]
            if not np.any(polygon == self.render.H_WIDTH | (polygon == self.render.H_HEIGHT)):
                pg.draw.polygon(self.render.screen, color, polygon, 3)
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color('gray'))
                    self.render.screen.blit(text, polygon[-1])
        for vertex in vertices:
            if not np.any(polygon == self.render.H_WIDTH | (polygon == self.render.H_HEIGHT)):
                pg.draw.circle(self.render.screen, pg.Color('orange'), vertex, 6)



    def scale(self, scalar):
        self.vertices = self.vertices @ scale(scalar)

    def rotateX(self, angle):
        self.vertices = self.vertices @ rotateX(angle)

    def rotateY(self, angle):
        self.vertices = self.vertices @ rotateY(angle)

    def rotateZ(self, angle):
        self.vertices = self.vertices @ rotateZ(angle)
    
    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)

    def parseCoordinates(self, str):
        inputStr = []
        try:
            inputStr = ast.literal_eval(str)
            if len(inputStr):
                for i, vertex in enumerate(inputStr):
                    self.vertices[i] = np.array(vertex)
                self.vertices = self.vertices[:4]
                interpolated = self.interpolate()
                self.vertices = np.append(self.vertices, interpolated, 0)
            return "Success"
        except:
            return "Wrong input"

class Axes(Object):
    def __init__(self, render):
        super().__init__(render)
        self.vertices = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.coloredFaces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.label = 'XYZ'