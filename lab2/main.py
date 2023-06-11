import pygame as pg
import numpy as np


class Bezier:
    def __init__(self, render):
        self.knots = []
        self.lineVertices = []
        self.clippedLineVertices = []
        self.render = render
        self.samples = 100
        self.RECTSIZE = 15
            
    def pointOnCurve(self, b, t):
        q = b.copy()
        for k in range(1, len(b)):
            for i in range(len(b) - k):
                q[i] = (1-t) * q[i][0] + t * q[i+1][0], (1-t) * q[i][1] + t * q[i+1][1]
        return round(q[0][0]), round(q[0][1])
    
    def drawCurve(self, surf, b, samples, color, thickness):
        pts = [self.pointOnCurve(b, i/samples) for i in range(samples+1)]
        pg.draw.lines(surf, color, False, pts, thickness)

    def redraw(self):
        for knot in self.knots:
            pg.draw.rect(self.render.screen, pg.Color('blue'), knot)
        if len(self.lineVertices) >= 2:
            for vertex in self.lineVertices:
                pg.draw.lines(self.render.screen, pg.Color('green'), 0, self.lineVertices, 3)
            self.drawCurve(self.render.screen, self.lineVertices, self.samples, pg.Color('grey'), 3)

    def addKnot(self, coords):
        x, y = coords
        self.knots.append(pg.Rect(x - self.RECTSIZE, y - self.RECTSIZE, self.RECTSIZE * 2, self.RECTSIZE * 2))
        self.lineVertices.append((x, y))
    
    def control(self):
        changedPlace = False
        key = pg.mouse.get_pressed()
        if key[0]:
            mousePos = pg.mouse.get_pos()
            for index, knot in enumerate(self.knots):
                if knot.collidepoint(mousePos) and key[0]:
                    changedPlace = True
                    self.knots[index] = pg.Rect(mousePos[0] - self.RECTSIZE, mousePos[1] - self.RECTSIZE, self.RECTSIZE * 2, self.RECTSIZE * 2)
                    self.lineVertices[index] = mousePos
            if not changedPlace:
                self.addKnot(mousePos)
        if key[2]:
            mousePos = pg.mouse.get_pos()
            for index, knot in enumerate(self.knots):
                if knot.collidepoint(mousePos) and key[2]:
                    self.knots.pop(index)
                    self.lineVertices.pop(index)              

class Render:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1280, 720
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.createObjects()

    def createObjects(self):
        self.bezier = Bezier(self)
    
    def draw(self):
        self.screen.fill(pg.Color('white'))
        self.bezier.redraw()

    def run(self):
        while True:
            self.draw()
            self.bezier.control()
            [exit() for e in pg.event.get() if e.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    rndr = Render()
    rndr.run()