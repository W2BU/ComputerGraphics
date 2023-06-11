import pygame as pg

class RotationContoller:

    def __init__(self, render, rotatingObject):
        self.render = render
        self.rotatingObject = rotatingObject
        self.rotationSpeed = 0.01 

    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_u]:
            self.rotatingObject.rotateX(self.rotationSpeed)
        if key[pg.K_j]:
            self.rotatingObject.rotateX(-self.rotationSpeed)
        if key[pg.K_i]:
            self.rotatingObject.rotateY(self.rotationSpeed)
        if key[pg.K_k]:
            self.rotatingObject.rotateY(-self.rotationSpeed)
        if key[pg.K_o]:
            self.rotatingObject.rotateZ(self.rotationSpeed)
        if key[pg.K_l]:
            self.rotatingObject.rotateZ(-self.rotationSpeed)