import pygame as pg
from cube import *
from projection import *
from camera import *
from rotationcontroller import *
import pygame_gui as pgg

class GUI:
    def __init__(self, render):
        self.render = render;
        self.manager = pgg.UIManager((self.render.WIDTH, self.render.HEIGHT))
        self.box2 = pgg.elements.UIButton(text = "Redraw", relative_rect=pg.Rect((1100, 100), (100, 50)), manager = self.manager)
        self.textBox1 = pgg.elements.UITextEntryBox(initial_text = "input 4 points as [[x1, y1, z1], [x2, y2, z2]...]", relative_rect = pg.Rect((1050, 200), (200, 150)), manager = self.manager)
        self.statusBox = pgg.elements.UITextBox(html_text = "Status", relative_rect = pg.Rect((1050, 400), (200, 50)), manager = self.manager)
    def draw(self):
        self.manager.draw_ui(self.render.display)


class Render:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1280, 720
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.display = pg.display.set_mode(self.RES)
        self.screen = pg.Surface((1000, 720))
        self.clock = pg.time.Clock()
        self.createObjects()
        

    def createObjects(self):
        self.camera = Camera(self, [0.6, 0.5, -5])
        self.projection = Projection(self)
        self.object = Object(self)
        self.rotationController = RotationContoller(self, self.object)
        self.axes = Axes(self)
        self.gui = GUI(self)
    
    def draw(self):
        self.screen.fill(pg.Color('white'))
        self.display.fill(pg.Color('grey'))
        self.object.draw()
        self.axes.draw()
        self.gui.draw()
        self.display.blit(self.screen, (0, 0))

    def run(self):
        while True:
            self.draw()
            self.camera.control()
            self.rotationController.control()
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    exit()
                if e.type == pgg.UI_BUTTON_PRESSED and e.ui_element == self.gui.box2:
                    self.gui.statusBox.html_text = self.object.parseCoordinates(self.gui.textBox1.get_text())
                    self.gui.statusBox.rebuild()
                self.gui.manager.process_events(e)
            self.gui.manager.update(self.clock.tick(self.FPS))
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    rendr = Render()
    rendr.run()