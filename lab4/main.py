import pygame as pg
import random as rnd


class ClipWindow:
    def __init__(self, render):
        self.render = render
        self.clippingWindow = []
        self.rectPointHitbox = []
        self.randomLinesVertices = []
        self.clippedLinesVertices = []
        self.samples = 15
        self.RECTSIZE = 15
        self.generateLines()
        self.INSIDE = 0 #0000
        self.LEFT = 1   #0001
        self.RIGHT = 2  #0010
        self.BOTTOM = 4 #0100
        self.TOP = 8    #1000
            
    def generateLines(self):
        for i in range(self.samples):
            self.randomLinesVertices.append(
                ((rnd.randrange(self.render.WIDTH), rnd.randrange(self.render.HEIGHT)),
                 (rnd.randrange(self.render.WIDTH), rnd.randrange(self.render.HEIGHT)))
            )

    def xMin(self):
        return min(self.clippingWindow[0][0], self.clippingWindow[1][0])
    
    def xMax(self):
        return max(self.clippingWindow[0][0], self.clippingWindow[1][0])
    
    def yMin(self):
        return min(self.clippingWindow[0][1], self.clippingWindow[1][1])
    
    def yMax(self):
        return max(self.clippingWindow[0][1], self.clippingWindow[1][1])

    def computeCode(self, point): 
        x, y = point
        code = self.INSIDE 
        if x < self.xMin():      # to the left of rectangle 
            code |= self.LEFT 
        elif x > self.xMax():    # to the right of rectangle 
            code |= self.RIGHT 
        if y < self.yMin():      # below the rectangle 
            code |= self.BOTTOM 
        elif y > self.yMax():    # above the rectangle 
            code |= self.TOP 
        return code

    def draw(self):
        for pair in self.randomLinesVertices:
            pg.draw.line(self.render.display, pg.Color('green'), pair[0], pair[1])
        if len(self.clippingWindow) == 2:
            xt, yt = self.clippingWindow[0]
            xb, yb = self.clippingWindow[1]
            pg.draw.line(self.render.display, pg.Color('red'), (xt, yt), (xt, yb))
            pg.draw.line(self.render.display, pg.Color('red'), (xt, yt), (xb, yt))
            pg.draw.line(self.render.display, pg.Color('red'), (xb, yt), (xb, yb))
            pg.draw.line(self.render.display, pg.Color('red'), (xt, yb), (xb, yb))
            self.cut()
            
        for rect in self.rectPointHitbox:
            pg.draw.rect(self.render.display, pg.Color('red'), rect)
            
    
    def cut(self):
        for line in self.randomLinesVertices:
            x1, y1 = line[0]
            x2, y2 = line[1]
            code1 = self.computeCode(line[0])
            code2 = self.computeCode(line[1])
            accept = False

            while True: 
                # If both endpoints lie within rectangle 
                if code1 == 0 and code2 == 0: 
                    accept = True
                    break
                # If both endpoints are outside rectangle 
                elif (code1 & code2) != 0: 
                    break
                # Some segment lies within the rectangle 
                else: 
                    x = 1.0
                    y = 1.0
                    if code1 != 0: 
                        code_out = code1 
                    else: 
                        code_out = code2 
                    # Find intersection point 
                    # using formulas y = y1 + slope * (x - x1),  
                    # x = x1 + (1 / slope) * (y - y1) 
                    if code_out & self.TOP: 
                        # point is above the clip rectangle 
                        x = x1 + ((x2 - x1) / (y2 - y1)) * (self.yMax() - y1) 
                        y = self.yMax()
        
                    elif code_out & self.BOTTOM: 
                        # point is below the clip rectangle 
                        x = x1 + ((x2 - x1) / (y2 - y1)) * (self.yMin() - y1) 
                        y = self.yMin() 
        
                    elif code_out & self.RIGHT: 
                        # point is to the right of the clip rectangle 
                        y = y1 + ((y2 - y1) / (x2 - x1)) * (self.xMax() - x1) 
                        x = self.xMax()
        
                    elif code_out & self.LEFT:
                        # point is to the left of the clip rectangle 
                        y = y1 + ((y2 - y1) / (x2 - x1)) * (self.xMin() - x1)  
                        x = self.xMin()
        
                    # Now intersection point x, y is found 
                    # We replace point outside clipping rectangle 
                    # by intersection point 
                    if code_out == code1: 
                        x1 = x 
                        y1 = y 
                        code1 = self.computeCode((x1, y1)) 
                    else: 
                        x2 = x 
                        y2 = y 
                        code2 = self.computeCode((x2, y2))
            if accept:
                pg.draw.line(self.render.display, pg.Color('red'), (x1, y1), (x2, y2))
        
    def control(self):
        changedPlace = False
        key = pg.mouse.get_pressed()
        if key[0]:
            mousePos = pg.mouse.get_pos()
            for index, knot in enumerate(self.rectPointHitbox):
                if knot.collidepoint(mousePos) and key[0]:
                    changedPlace = True
                    self.rectPointHitbox[index] = pg.Rect(mousePos[0] - self.RECTSIZE, mousePos[1] - self.RECTSIZE, self.RECTSIZE * 2, self.RECTSIZE * 2)
                    self.clippingWindow[index] = mousePos
            if not changedPlace and len(self.clippingWindow) < 2:
                self.rectPointHitbox.append(pg.Rect(mousePos[0] - self.RECTSIZE, mousePos[1] - self.RECTSIZE, self.RECTSIZE * 2, self.RECTSIZE * 2))
                self.clippingWindow.append(mousePos)
        if key[2]:
            mousePos = pg.mouse.get_pos()
            for index, knot in enumerate(self.rectPointHitbox):
                if knot.collidepoint(mousePos) and key[2]:
                    self.rectPointHitbox.pop(index)
                    self.clippingWindow.pop(index) 
            


class Render:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1280, 720
        self.FPS = 60
        self.display = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.createObjects()

    def createObjects(self):
        self.cutWindow = ClipWindow(self)
    
    def draw(self):
        self.display.fill(pg.Color('white'))
        self.cutWindow.draw()


    def run(self):
        while True:
            self.draw()
            self.cutWindow.control()
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    exit()
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    rndr = Render()
    rndr.run()