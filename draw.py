from pyautogui import Point
import math

_viewPort = None


class Polyline:
    def __init__(self, **kwargs):
        self.points = []
        # kwargs["color"] = kwargs.get("color", "black")
        self.color = kwargs.get("color", "black")
        self.width = kwargs.get("width", 1)

    def add_point(self, x, y):
        p = Point(x, y)
        self.points.append(p)

    def remove(self):
        self.points = []

    def draw(self, canvas):
        if self.points != []:
            line = []
            x0 = self.points[0].x
            y0 = self.points[0].y
            for point in self.points:
                line.append(canvas.create_line(x0, y0, point.x, point.y, fill=self.color, width=4))
                x0 = point.x
                y0 = point.y
        return line


def coords(canvas, obj):
    # return _C.coords(obj)
    return canvas.bbox(obj)


def moveObjectBy(canvas, obj, dx, dy):
    canvas.move(obj, dx, dy)


def grid(self):
    for y in range(0, self.canvas_width * 100, self.step):
        self.grList.append(self.canvas.create_line(0, y, self.canvas_width * 100, y, fill=self.gridColor, dash=(2, 8)))
    for x in range(0, self.canvas_height * 100, self.step):
        self.grList.append(self.canvas.create_line(x, 0, x, self.canvas_height * 100, fill=self.gridColor, dash=(2, 8)))


def center(canvas, obj):
    x1, y1, x2, y2 = coords(canvas, obj)
    return (x1 + x2) / 2, (y1 + y2) / 2


def deleteObject(canvas, obj):
    canvas.delete(obj)


def draw_rectangle(self, event):
    if self.xStart == 0 and self.yStart == 0:
        self.xLineStart = event.x
        self.yLineStart = event.y
        self.line0 = self.canvas.create_polygon([self.xLineStart, self.yLineStart],
                                                [self.xLineStart, self.yLineStart],
                                                [self.xLineStart, self.yLineStart],
                                                [self.xLineStart, self.yLineStart],
                                                width=self.penWidth, outline=self.penColor,
                                                fill=self.brushColor)
        self.cLine0 = {'x1':0, 'y1':0, 'x2':0, 'y2':0, 'x3':0, 'y3':0, 'x4':0, 'y4':0}
    else:
        self.cLine0 = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0, 'x3': 0, 'y3': 0, 'x4': 0, 'y4': 0}
        x1 = self.xLineStart
        y1 = self.yLineStart
        x2 = event.x
        y2 = self.yLineStart
        x3 = event.x
        y3 = event.y
        x4 = self.xLineStart
        y4 = event.y
        if x1 < x3 and y3 > y1:
            self.cLine0['x1'] = x1
            self.cLine0['y1'] = y1
            self.cLine0['x2'] = x2
            self.cLine0['y2'] = y2
            self.cLine0['x3'] = x3
            self.cLine0['y3'] = y3
            self.cLine0['x4'] = x4
            self.cLine0['y4'] = y4
        elif x3 < x1 and y3 > y1:
            self.cLine0['x1'] = x2
            self.cLine0['y1'] = y2
            self.cLine0['x2'] = x3
            self.cLine0['y2'] = y3
            self.cLine0['x3'] = x4
            self.cLine0['y3'] = y4
            self.cLine0['x4'] = x1
            self.cLine0['y4'] = y1
        elif x3 < x1 and y1 > y3:
            self.cLine0['x1'] = x3
            self.cLine0['y1'] = y3
            self.cLine0['x2'] = x4
            self.cLine0['y2'] = y4
            self.cLine0['x3'] = x1
            self.cLine0['y3'] = y1
            self.cLine0['x4'] = x2
            self.cLine0['y4'] = y2
        elif x1 < x3 and y1 > y3:
            self.cLine0['x1'] = x4
            self.cLine0['y1'] = y4
            self.cLine0['x2'] = x1
            self.cLine0['y2'] = y1
            self.cLine0['x3'] = x2
            self.cLine0['y3'] = y2
            self.cLine0['x4'] = x3
            self.cLine0['y4'] = y3
        self.cLine0['width'] = self.penWidth
        self.cLine0['outline'] = self.penColor
        self.cLine0['fill'] = self.brushColor
        self.canvas.coords(self.line0, self.cLine0['x1'], self.cLine0['y1'], self.cLine0['x2'],
                           self.cLine0['y2'],
                           self.cLine0['x3'], self.cLine0['y3'], self.cLine0['x4'], self.cLine0['y4'])


def draw_line(self, event):
    if self.xStart == 0 and self.yStart == 0:
        self.xLineStart = event.x
        self.yLineStart = event.y
        self.line0 = self.canvas.create_line(self.xLineStart, self.yLineStart,
                                             self.xLineStart,
                                             self.yLineStart, width=self.penWidth,
                                             fill=self.penColor, arrow=self.lineArrow,
                                             dash=self.lineDot)
        self.cLine0 = {}
        self.cLine0['x1'] = self.xLineStart
        self.cLine0['y1'] = self.yLineStart
        self.cLine0['x2'] = self.xLineStart
        self.cLine0['y2'] = self.yLineStart
        self.cLine0['width'] = self.penWidth
        self.cLine0['fill'] = self.penColor
        self.cLine0['arrow'] = self.lineArrow
        self.cLine0['dash'] = self.lineDot

    else:
        self.canvas.coords(self.line0, self.xLineStart, self.yLineStart, event.x, event.y)
        self.cLine0['x1'] = self.xLineStart
        self.cLine0['y1'] = self.yLineStart
        self.cLine0['x2'] = event.x
        self.cLine0['y2'] = event.y


def erMove(self, x, y):
    for fig in self.figures:
        # print(fig[0])
        if fig[1] == "polyline":
            x1,y1,x2,y2 = border_polyline(fig[2])
            xCeOb, yCeOb = (x1+x2)//2, (y1+y2)//2
        else:
            xCeOb, yCeOb = center(self.canvas, fig[0])
        if abs(x + self.errSize - xCeOb) < self.errSize and abs(y + self.errSize - yCeOb) < self.errSize:
            if len(self.figures) > 0:
                deleteObject(self.canvas, fig[0])
                self.figures.remove(fig)


def border_polyline(points):
    # print(points)
    if points == []:
        return 0, 0, 0, 0
    x_min = points[0].x
    y_min = points[0].y
    x_max = points[0].x
    y_max = points[0].y
    for p in points:
        if p.x > x_max:
            x_max = p.x
        if p.y > y_max:
            y_max = p.y
        if p.x < x_min:
            x_min = p.x
        if p.y < y_min:
            y_min = p.y

    return x_min, y_min, x_max, y_max


def penMove(self, x, y):
    if self.xStart == x and self.yStart == y:
        return
    if self.xStart == 0 and self.yStart == 0:
        pass
    else:
        self.poly.append(Point(x, y))
        self.poly.append(Point(x, y))
        self.f0 = self.canvas.create_line(self.poly, fill=self.penColor, width=self.penWidth)


def resize_object(self, event):
    f = False
    if self.selFig['0'] != None and self.selFig['Obj'] != None:
        x1, y1, x2, y2 = coords(self.canvas, self.selFig['0'])
        # x1, y1, x2, y2 = self.canvas.coords(self.selFig['Obj'][0])
        if self.selFig['Obj'][1] == 'line':
            x1, y1, x2, y2 = self.canvas.coords(self.selFig['Obj'][0])
            if math.sqrt((event.x - x1) ** 2 + (event.y - y1) ** 2) < 50:  # 1 vertic
                self.flag = 2
                self.canvas.config(cursor='bottom_right_corner')
                self.canvas.coords(self.selFig['Obj'][0], event.x, event.y, x2, y2)
                self.selFig['Obj'][2]['x1'] = event.x
                self.selFig['Obj'][2]['y1'] = event.y
                self.selFig['Obj'][2]['x2'] = x2
                self.selFig['Obj'][2]['y2'] = y2
                self.canvas.coords(self.selFig['0'], event.x - 1, event.y - 1, x2 + 1, y2 + 1)
                x1, y1, x2, y2 = self.canvas.coords(self.selFig['Obj'][0])
                self.canvas.coords(self.selFig['D'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,
                                   abs(y1 + y2) // 2 + 10)

                f = True
            elif math.sqrt((event.x - x2) ** 2 + (event.y - y2) ** 2) < 50:  # 2 vertic
                self.flag = 2
                self.canvas.config(cursor='bottom_right_corner')
                self.canvas.coords(self.selFig['Obj'][0], x1, y1, event.x, event.y)
                self.selFig['Obj'][2]['x1'] = x1
                self.selFig['Obj'][2]['y1'] = y1
                self.selFig['Obj'][2]['x2'] = event.x
                self.selFig['Obj'][2]['y2'] = event.y
                self.canvas.coords(self.selFig['0'], x1 - 1, y1 - 1, event.x + 1, event.y + 1)
                x1, y1, x2, y2 = self.canvas.coords(self.selFig['Obj'][0])
                self.canvas.coords(self.selFig['D'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,
                                   abs(y1 + y2) // 2 + 10)
                f = True
        elif self.selFig['Obj'][1] == 'rectangle':
            xo1, yo1, xo2, yo2 = coords(self.canvas, self.selFig['0'])
            if math.sqrt((event.x - xo2) ** 2 + (event.y - yo2) ** 2) < 50:
                self.flag = 2
                x1 = self.selFig['Obj'][2]['x1']
                y1 = self.selFig['Obj'][2]['y1']
                self.canvas.coords(self.selFig['Obj'][0],
                                   x1, y1, event.x, y1,
                                   event.x, event.y, x1, event.y)
                self.canvas.coords(self.selFig['0'], x1 - 1, y1 - 1, event.x + 1, event.y + 1)
                self.canvas.coords(self.selFig['D'], event.x - 10, (y1 + event.y) // 2 - 10,
                                   event.x + 10, (y1 + event.y) // 2 + 10)
                self.selFig['Obj'][2]['x2'] = event.x
                self.selFig['Obj'][2]['y2'] = y1
                self.selFig['Obj'][2]['x3'] = event.x
                self.selFig['Obj'][2]['y3'] = event.y
                self.selFig['Obj'][2]['x4'] = x1
                self.selFig['Obj'][2]['y4'] = event.y
                f = True
        elif self.selFig['Obj'][1] == 'image':
            xo1, yo1, xo2, yo2 = coords(self.canvas, self.selFig['0'])
            if math.sqrt((event.x - xo2) ** 2 + (event.y - yo2) ** 2) < 50:
                self.flag = 2
                x = self.selFig['Obj'][2]['x']
                y = self.selFig['Obj'][2]['y']
                self.canvas.coords(self.selFig['0'], x - 1, y - 1, event.x + 1, event.y + 1)
                self.canvas.coords(self.selFig['D'], event.x - 10, (y + event.y) // 2 - 10,
                                   event.x + 10,
                                   (y + event.y) // 2 + 10)
                f = True
    return f


def move_object(self, event):
    f = False
    if self.selFig['0'] != None:
        self.flag = 1
        if self.selFig['Obj'][1] == 'rectangle':
            x1 = self.selFig['Obj'][2]['x1']
            y1 = self.selFig['Obj'][2]['y1']
            x2 = self.selFig['Obj'][2]['x2']
            y2 = self.selFig['Obj'][2]['y2']
            x3 = self.selFig['Obj'][2]['x3']
            y3 = self.selFig['Obj'][2]['y3']
            x4 = self.selFig['Obj'][2]['x4']
            y4 = self.selFig['Obj'][2]['y4']
            dx = event.x - self.xStart
            dy = event.y - self.yStart
            self.selFig['Obj'][2]['x1'] = x1 + dx
            self.selFig['Obj'][2]['y1'] = y1 + dy
            self.selFig['Obj'][2]['x2'] = x2 + dx
            self.selFig['Obj'][2]['y2'] = y2 + dy
            self.selFig['Obj'][2]['x3'] = x3 + dx
            self.selFig['Obj'][2]['y3'] = y3 + dy
            self.selFig['Obj'][2]['x4'] = x4 + dx
            self.selFig['Obj'][2]['y4'] = y4 + dy
            moveObjectBy(self.canvas, self.selFig['Obj'][0], dx, dy)
            self.canvas.coords(self.selFig['0'],
                               coords(self.canvas, self.selFig['Obj'][0]))
            x1, y1, x2, y2 = coords(self.canvas, self.selFig['Obj'][0])
            self.canvas.coords(self.selFig['D'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,
                               abs(y1 + y2) // 2 + 10)

            f = True
        elif self.selFig['Obj'][1] == 'line':
            x1 = self.selFig['Obj'][2]['x1']
            y1 = self.selFig['Obj'][2]['y1']
            x3 = self.selFig['Obj'][2]['x2']
            y3 = self.selFig['Obj'][2]['y2']
            dx = event.x - self.xStart
            dy = event.y - self.yStart
            self.selFig['Obj'][2]['x1'] = x1 + dx
            self.selFig['Obj'][2]['y1'] = y1 + dy
            self.selFig['Obj'][2]['x2'] = x3 + dx
            self.selFig['Obj'][2]['y2'] = y3 + dy
            moveObjectBy(self.canvas, self.selFig['Obj'][0], dx, dy)
            self.canvas.coords(self.selFig['0'],
                               coords(self.canvas, self.selFig['Obj'][0]))
            x1, y1, x2, y2 = coords(self.canvas, self.selFig['Obj'][0])
            self.canvas.coords(self.selFig['D'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,
                               abs(y1 + y2) // 2 + 10)

            f = True
        elif self.selFig['Obj'][1] == 'image':
            self.flag = 3
            x = self.selFig['Obj'][2]['x']
            y = self.selFig['Obj'][2]['y']
            w = self.selFig['Obj'][2]['width']
            h = self.selFig['Obj'][2]['height']
            dx = event.x - self.xStart
            dy = event.y - self.yStart
            self.selFig['Obj'][2]['x'] = x + dx
            self.selFig['Obj'][2]['y'] = y + dy
            self.selFig['Obj'][2]['width'] = w
            self.selFig['Obj'][2]['height'] = h
            self.canvas.coords(self.selFig['Obj'][0], x + dx, y + dy)
            self.canvas.coords(self.selFig['0'],
                               coords(self.canvas, self.selFig['Obj'][0]))
            x1, y1, x2, y2 = coords(self.canvas, self.selFig['Obj'][0])
            self.canvas.coords(self.selFig['D'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,
                               abs(y1 + y2) // 2 + 10)
            f = True
        elif self.selFig['Obj'][1] == 'polyline':
            self.flag = 3
            dx = event.x - self.xStart
            dy = event.y - self.yStart
            poly2 = []
            for p in self.selFig['Obj'][2]:
                poly2.append(Point(p.x + dx, p.y + dy))
            self.selFig['Obj'][2] = poly2

            self.canvas.move(self.selFig['Obj'][0], dx, dy)
            x1, y1, x2, y2 = coords(self.canvas, self.selFig['Obj'][0])
            self.canvas.coords(self.selFig['0'], x1, y1, x2, y2)
            self.canvas.coords(self.selFig['D'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,
                               abs(y1 + y2) // 2 + 10)
            f = True
    return f
