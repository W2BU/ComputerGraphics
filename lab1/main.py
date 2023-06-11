import pygame as pg
from cube import *
from projection import *
from camera import *
from rotationcontroller import *


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
        self.camera = Camera(self, [0.5, 1, -4])
        self.projection = Projection(self)
        self.object = Object(self)
        self.rotationController = RotationContoller(self, self.object)
        self.object.translate([0.2, 0.4, 0.2])
        self.axes = Axes(self)
    
    def draw(self):
        self.screen.fill(pg.Color('white'))
        self.object.draw()
        self.axes.draw()

    def run(self):
        while True:
            self.draw()
            self.camera.control()
            self.rotationController.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    rendr = Render()
    rendr.run()