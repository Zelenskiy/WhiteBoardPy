from pyautogui import Point

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


def erMove(self, x, y):
    for fig in self.figures:
        # print(fig[0])

        xCeOb, yCeOb = center(self.canvas, fig[0])
        if abs(x + self.errSize - xCeOb) < self.errSize and abs(y + self.errSize - yCeOb) < self.errSize:
            if len(self.figures) > 0:
                deleteObject(self.canvas, fig[0])
                self.figures.remove(fig)


# def penMove(color, xStart, yStart, r, canvas, figures, x, y):
def _penMove(self, x, y):
    r = self.penWidth
    x1 = self.xStart
    y1 = self.yStart
    x2 = x
    y2 = y
    step = 1
    if abs(x2 - x1) > abs(y2 - y1):
        fl = 0
        if self.xStart < x:
            myRange = range(self.xStart, x, step)
        else:
            myRange = range(x, self.xStart, step)
    else:
        fl = 1
        if self.yStart < y:
            myRange = range(self.yStart, y, step)
        else:
            myRange = range(y, self.yStart, step)
    for x in myRange:
        if fl == 0:
            xx = x
            yy = int(((x1 * y2 - x2 * y1) + (y1 - y2) * x) / (x1 - x2))
        else:
            yy = x
            xx = int(((x1 * y2 - x2 * y1) + (x2 - x1) * yy) / (y2 - y1))
        if True:
            k = []
            k.append(self.canvas.create_oval(xx - r // 2, yy - r // 2, xx + r // 2, yy + r // 2, outline=self.penColor,
                                             fill=self.penColor, width=1))
            k.append("oval")
            c = {}
            c['x1'] = xx - r // 2
            c['y1'] = yy - r // 2
            c['x2'] = xx + r // 2
            c['y2'] = yy + r // 2
            c['outline'] = self.color
            c['fill'] = self.color
            c['width'] = 1
            k.append(c)
            self.figures.append(k)


def penMove(self, x, y):
    if self.xStart == 0 and self.yStart == 0:
         pass
    else:
        # [[4471, 'line', {'x1': 166, 'y1': 269, 'x2': 242, 'y2': 334, 'width': 2, 'fill': '#0000FF', 'arrow': '', 'dash': ''}],
        #  [4472, 'rectangle', {'x1': 174, 'y1': 361, 'x2': 273, 'y2': 361, 'x3': 273, 'y3': 433, 'x4': 174, 'y4': 433, 'width': 2,       'outline': '#0000FF', 'fill': ''}], {}]

        self.poly.append(Point(x, y))
        p1 = self.poly.copy()
        p2 = self.poly.copy()
        p2.reverse()
        p3 = p1 + p2
        deleteObject(self.canvas, self.f0[-1])
        self.f0[-1] = self.canvas.create_polygon(p3, fill=self.penColor, width=self.penWidth,
                                             outline=self.penColor)
