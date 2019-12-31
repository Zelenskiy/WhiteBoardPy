import numpy as np
import math
from tkinter import *
from tkinter import colorchooser, LAST
from datetime import datetime

import pyautogui
from PIL import ImageTk, Image
import pickle
import imutils
import cv2

from draw import *

from sys import platform

if platform == "win32" or platform == "cygwin":
    VK_SPACE = 0x20
    VK_PRIOR = 0x21  # PAGE UP key
    VK_NEXT = 0x22  # PAGE DOWN key
    VK_END = 0x23  # END key
    VK_HOME = 0x24  # HOME key
    VK_LEFT = 0x25
    VK_UP = 0x26
    VK_RIGHT = 0x27
    VK_DOWN = 0x28
    VK_INSERT = 0x2D  # INS key
    VK_DELETE = 0x2E  # DELETE key
    VK_BACK = 0x08  # BACKSPACE key
    VK_TAB = 0x09  # TAB key
    VK_RETURN = 0x0D  # RETURN key
    VK_ESCAPE = 0x1B  # ESC key
elif platform == "linux":
    VK_SPACE = 0x41
    VK_PRIOR = 0x70  # PAGE UP key
    VK_NEXT = 0x75  # PAGE DOWN key
    VK_END = 0x73  # END key
    VK_HOME = 0x6E  # HOME key
    VK_LEFT = 0x71
    VK_UP = 0x6F
    VK_RIGHT = 0x72
    VK_DOWN = 0x74
    VK_INSERT = 0x76  # INS key
    VK_DELETE = 0x77  # DELETE key
    VK_BACK = 0x16  # BACKSPACE key
    VK_TAB = 0x17  # TAB key
    VK_RETURN = 0x24  # RETURN key
    VK_ESCAPE = 0x09  # ESC key

grList = []
errSize = 10
figures = []
canvases = []
cpFigures = []
flag = 0
tool = 1
xStart = 0
yStart = 0
canvas = None
color = None
xLineStart = 0
yLineStart = 0
line0 = None
cLine0 = None
penWidth = 2
penColor = "#0000FF"
btnActiveColor = "#331177"
brushColor = ""
lineArrow = ''
lineDot = ''
gridColor = "#D0D0D0"
canvas_width = 0
canvas_height = 0
fonColor = "#E9FBCA"
screen_width = 0
screen_height = 0
root = None
selFig = {}

xc = 0
yc = 0


def btnScrClick(w):
    global screen_width, screen_height, canvas, figures

    def btnClick():
        print('btnClick')
        width = 600
        x0 = 500
        y0 = 10
        # floatWindow.geometry('+{}+{}'.format(-100, -100))
        # floatWindow.geometry("40x35+100+100")
        name = 'tmp/' + datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S") + '.png'
        image = pyautogui.screenshot(region=(0, 0, screen_width, screen_height + 75))
        image.save(name)
        k = screen_width / (screen_height + 75)
        height = int(width / k)
        image = image.resize((width, height), Image.ANTIALIAS)
        w.wm_state('normal')
        w.output = ImageTk.PhotoImage(image)
        im = canvas.create_image(x0, y0, image=w.output, state=NORMAL, anchor=NW)
        canvas.update()
        floatWindow.destroy()
        # canvas.create_window(20, 20)
        k = []
        c = {}
        c['name'] = name
        c['x'] = x0
        c['y'] = y0
        c['width'] = width
        c['height'] = height
        k.append(im)
        k.append("image")
        k.append(c)
        figures.append(k)
        print(figures)

    print('btnScrClick')
    w.wm_state('iconic')
    floatWindow = Tk()
    floatWindow.geometry("40x35+20+20")
    # floatWindow.wm_state('icon')
    # window without border

    btn = Button(floatWindow, text='Sr', command=btnClick)
    # btn.config(bg='systemTransparent')

    floatWindow.overrideredirect(1)
    floatWindow.wm_attributes("-topmost", True)

    # floatWindow.attributes("-transparentcolor", "white")

    btn.pack(fill=BOTH, expand=True)

    # w.wm_state('normal')


def save():
    global figures, penColor, brushColor, penWidth, fonColor, canvas_width, canvas_height, xc, yc
    data = {}
    data['figures'] = figures
    data['penColor'] = penColor
    data['brushColor'] = brushColor
    data['penWidth'] = penWidth
    data['fonColor'] = fonColor
    data['canvas_width'] = canvas_width
    data['canvas_height'] = canvas_height
    data['xc'] = xc
    data['yc'] = yc

    with open("test.wb", "wb") as fp:
        pickle.dump(data, fp)


def load(canv, root):
    global figures, penColor, brushColor, penWidth, fonColor, canvas_width, canvas_height, xc, yc, \
        grList, selFig, tool
    canv.delete(ALL)
    figures = []
    # selFig = {}
    tool = 1

    with open("test.wb", "rb") as fp:  # Unpickling
        data = pickle.load(fp)
    figures = data['figures']
    penColor = data['penColor']
    brushColor = data['brushColor']
    penWidth = data['penWidth']
    fonColor = data['fonColor']
    canvas_width = data['canvas_width']
    canvas_height = data['canvas_height']
    xc = data['xc']
    yc = data['yc']
    # change size and position canvas
    canv.place(x=xc, y=yc)
    canv.config(width=canvas_width, height=canvas_height)
    grid(canvas, gridColor, canvas_width + 50, canvas_height + 50, 50, grList)

    for fig in figures:
        f = fig[2]
        if fig[1] == 'oval':
            fig[0] = canv.create_oval(f['x1'], f['y1'], f['x2'], f['y2'], outline=f['outline'],
                                      fill=f['fill'], width=f['width'])
        elif fig[1] == 'line':
            canv.create_line(f['x1'], f['y1'], f['x2'], f['y2'], width=f['width'], fill=f['fill'],
                             arrow=f['arrow'], dash=f['dash'])
        elif fig[1] == 'rectangle':
            fig[0] = canv.create_polygon(f['x1'], f['y1'], f['x2'], f['y2'], f['x3'], f['y3'], f['x4'], f['y4'],
                                         width=f['width'], fill=f['fill'],
                                         outline=f['outline'])
        elif fig[1] == 'image':
            width = f['width']
            height = f['height']
            image = Image.open(f['name'])
            image = image.resize((width, height), Image.ANTIALIAS)
            root.output = ImageTk.PhotoImage(image)
            fig[0] = canv.create_image(f['x'], f['y'], image=root.output, state=NORMAL, anchor=NW)


def f_quit(event):
    if event.keysym == 'Escape':
        quit()


def mouseDown(event):
    global selFig, canvas, figures
    if tool == 8:
        # select object

        for fig in figures:
            x1, y1, x2, y2 = coords(canvas, fig[0])
            if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
                if selFig == {}:
                    pass
                else:
                    canvas.coords(selFig['0'], x1 - 1, y1 - 1, x2 + 1, y2 + 1)
                    # canvas.coords(selFig['SE'], max(x2, x1) - 20, max(y2, y1) - 20, max(x2, x1), max(y2, y1))

                    canvas.coords(selFig['D'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,abs(y1 + y2) // 2 + 10)
                    # canvas.coords(selFig['NW'], x1 - 10, y1 - 10, x1 + 10, y1 + 10)
                    # canvas.coords(selFig['NE'], x2 - 10, y1 - 10, x2 + 10, y1 + 10)
                    # canvas.coords(selFig['SW'], x1 - 10, y2 - 10, x1 + 10, y2 + 10)
                    # canvas.coords(selFig['S'], abs(x1 + x2) // 2 - 10, y2 - 10, abs(x1 + x2) // 2 + 10, y2 + 10)
                    # canvas.coords(selFig['E'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10, abs(y1 + y2) // 2 + 10)

                    selFig['Obj'] = fig
                fl = True
                break

    # repeat code
    fl = False
    if tool == 8:

        # change cursor
        print(selFig)
        if selFig['0'] != None:
            try:
                x1, y1, x2, y2 = coords(canvas, selFig['0'])
                if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
                    canvas.config(cursor="fleur")
                else:
                    canvas.config(cursor="tcross")
            except:
                pass
    if not fl:
        pass
        # selFig = {}


def mouseMove(event):
    global count, xStart, yStart, eraser, tool, errSize, color, canvas, xc, yc, line0, \
        xLineStart, yLineStart, cLine0, penWidth, penColor, selFig, selObj
    xx = ""

    if xStart == 0 and yStart == 0 and tool != 3 and tool != 4:
        xStart = event.x
        yStart = event.y

    if tool == 1:
        penMove(penColor, xStart, yStart, penWidth, canvas, figures, event.x, event.y)

    elif tool == 2:
        erMove(errSize, canvas, figures, event.x, event.y)
    elif tool == 7:
        dx = event.x - xStart
        dy = event.y - yStart
        xc += dx
        if xc > 0:
            xc -= dx
        yc += dy
        if yc > 0:
            yc -= dy
        canvas.place(x=xc, y=yc)
        if xc + (0) > 0:
            pass
    #     TODO make for expanding if drag canvas out borger

    elif tool == 3:
        if xStart == 0 and yStart == 0:
            xLineStart = event.x
            yLineStart = event.y
            line0 = canvas.create_line(xLineStart, yLineStart, xLineStart, yLineStart, width=penWidth,
                                       fill=penColor, arrow=lineArrow, dash=lineDot)
            cLine0 = {}
            cLine0['x1'] = xLineStart
            cLine0['y1'] = yLineStart
            cLine0['x2'] = xLineStart
            cLine0['y2'] = yLineStart
            cLine0['width'] = penWidth
            cLine0['fill'] = penColor
            cLine0['arrow'] = lineArrow
            cLine0['dash'] = lineDot

        else:
            canvas.coords(line0, xLineStart, yLineStart, event.x, event.y)
            cLine0['x1'] = xLineStart
            cLine0['y1'] = yLineStart
            cLine0['x2'] = event.x
            cLine0['y2'] = event.y

    elif tool == 4:
        if xStart == 0 and yStart == 0:
            xLineStart = event.x
            yLineStart = event.y
            line0 = canvas.create_polygon([xLineStart, yLineStart], [xLineStart, yLineStart], [xLineStart, yLineStart],
                                          [xLineStart, yLineStart],
                                          width=penWidth, outline=penColor, fill=brushColor)
            cLine0 = {}
        else:
            canvas.coords(line0, xLineStart, yLineStart, xLineStart, event.y, event.x, event.y, event.x, yLineStart)
            cLine0 = {}
            cLine0['x1'] = xLineStart
            cLine0['y1'] = yLineStart
            cLine0['x2'] = event.x
            cLine0['y2'] = yLineStart
            cLine0['x3'] = event.x
            cLine0['y3'] = event.y
            cLine0['x4'] = xLineStart
            cLine0['y4'] = event.y

            cLine0['width'] = penWidth
            cLine0['outline'] = penColor
            cLine0['fill'] = brushColor
    elif tool == 8:
        # draging figure

        xo1, yo1, xo2, yo2 = coords(canvas, selFig['Obj'][0])
        if math.sqrt((event.x - xo2) ** 2 + (event.y - yo2) ** 2) < 20:
            print("!!!!!!!!!!!!!!!!!!!!!!")
            x1 = selFig['Obj'][2]['x1']
            y1 = selFig['Obj'][2]['y1']
            x2 = selFig['Obj'][2]['x2']
            y2 = selFig['Obj'][2]['y2']

            if x2 > x1 and y2 > y1:
                print(11111111)
                canvas.coords(selFig['Obj'][0], x1, y1, event.x, event.y)
                canvas.coords(selFig['0'], x1 - 1, y1 - 1, event.x + 1, event.y + 1)
                selFig['Obj'][2]['x2'] = event.x
                selFig['Obj'][2]['y2'] = event.y
            elif x2 < x1 and y2 > y1:
                canvas.coords(selFig['Obj'][0], event.x, y1, x2, event.y)
                canvas.coords(selFig['0'], event.x - 1, y1 - 1, x2 + 1, event.y + 1)
                selFig['Obj'][2]['x1'] = event.x
                selFig['Obj'][2]['y2'] = event.y
            elif x2 < x1 and y2 > y1:
                pass
            elif x2 < x1 and y2 < y1:
                pass
            elif x2 > x1 and y2 < y1:
                pass

            # x3 = event.x
            # y3 = event.y
            # canvas.coords(selFig['Obj'][0], x1, y1, x2, y2)
            # canvas.coords(selFig['0'], x1 - 1, y1 - 1, x2 + 1, y2 + 1)
            # selFig['Obj'][2]['x1'] = x1
            # selFig['Obj'][2]['y1'] = y1
            # selFig['Obj'][2]['x2'] = x2
            # selFig['Obj'][2]['y2'] = y2

            xx = "resize"
        else:
            x1, y1, x2, y2 = coords(canvas, selFig['Obj'][0])
            if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
                if selFig['Obj'][1] == 'rectangle':
                    x1 = selFig['Obj'][2]['x1']
                    y1 = selFig['Obj'][2]['y1']
                    x2 = selFig['Obj'][2]['x2']
                    y2 = selFig['Obj'][2]['y2']
                    x3 = selFig['Obj'][2]['x3']
                    y3 = selFig['Obj'][2]['y3']
                    x4 = selFig['Obj'][2]['x4']
                    y4 = selFig['Obj'][2]['y4']
                    dx = event.x - xStart
                    dy = event.y - yStart
                    selFig['Obj'][2]['x1'] = x1 + dx
                    selFig['Obj'][2]['y1'] = y1 + dy
                    selFig['Obj'][2]['x2'] = x2 + dx
                    selFig['Obj'][2]['y2'] = y2 + dy
                    selFig['Obj'][2]['x3'] = x3 + dx
                    selFig['Obj'][2]['y3'] = y3 + dy
                    selFig['Obj'][2]['x4'] = x4 + dx
                    selFig['Obj'][2]['y4'] = y4 + dy
                    # moveObjectBy(canvas, selFig['Obj'][0], dx, dy)
                    # canvas.coords(selFig['0'], x1 - 1, y1 - 1, x3 + 1, y3 + 1)
                    # canvas.coords(selFig['SE'], max(x3,x1) - 10, max(y3,y1) - 10, max(x3,x1) + 10, max(y3,y1) + 10)
                elif selFig['Obj'][1] == 'line':
                    x1 = selFig['Obj'][2]['x1']
                    y1 = selFig['Obj'][2]['y1']
                    x3 = selFig['Obj'][2]['x2']
                    y3 = selFig['Obj'][2]['y2']
                    dx = event.x - xStart
                    dy = event.y - yStart
                    selFig['Obj'][2]['x1'] = x1 + dx
                    selFig['Obj'][2]['y1'] = y1 + dy
                    selFig['Obj'][2]['x2'] = x3 + dx
                    selFig['Obj'][2]['y2'] = y3 + dy
                elif selFig['Obj'][1] == 'image':
                    x = selFig['Obj'][2]['x']
                    y = selFig['Obj'][2]['y']
                    w = selFig['Obj'][2]['width']
                    h = selFig['Obj'][2]['height']
                    dx = event.x - xStart
                    dy = event.y - yStart
                    selFig['Obj'][2]['x'] = x + dx
                    selFig['Obj'][2]['y'] = y + dy
                    selFig['Obj'][2]['width'] = w
                    selFig['Obj'][2]['height'] = w
                    canvas.coords(selFig['Obj'][0], x + dx, y + dy)
                    canvas.coords(selFig['0'], coords(canvas, selFig['Obj'][0]))
                    x1, y1, x2, y2 = coords(canvas, selFig['Obj'][0])
                    canvas.coords(selFig['D'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10, abs(y1 + y2) // 2 + 10)

                if xx != "resize" and selFig['Obj'][1] != 'image':
                    moveObjectBy(canvas, selFig['Obj'][0], dx, dy)
                    canvas.coords(selFig['0'], coords(canvas, selFig['Obj'][0]))
                    x1,y1,x2,y2 = coords(canvas, selFig['Obj'][0])
                    canvas.coords(selFig['D'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,abs(y1 + y2) // 2 + 10)
                    # canvas.coords(selFig['SE'], max(x3, x1) - 10, max(y3, y1) - 10, max(x3, x1) + 10, max(y3, y1) + 10)



    if tool != 8:
        if selFig != {}:
            canvas.coords(selFig, 100000, 100000, 1000001, 100001)
            # selFig = {}

    xStart = event.x
    yStart = event.y


def mouseMoveNoButton(event):
    global selFig, tool
    if tool == 8:
        # change cursor
        try:

            if not selFig['Obj'] is None:
                x1, y1, x2, y2 = coords(canvas, selFig['0'])
                if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
                    canvas.config(cursor="fleur")
                else:
                    canvas.config(cursor="tcross")
        except:
            pass


def mouseUp(event):
    global xStart, yStart, cLine0, line0, xLineStart, yLineStart, selFig
    xStart = 0
    yStart = 0
    fl = False
    if tool == 3 or tool == 4:
        k = []
        k.append(line0)
        if tool == 3:
            k.append("line")
        else:
            k.append("rectangle")
        k.append(cLine0)
        figures.append(k)
        print(figures)

    x1, y1, x2, y2 = coords(canvas, selFig['D'])
    if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
        canvas.delete(selFig['Obj'][0])
        canvas.coords(selFig['0'],10000, 10000, 10001, 10001)
        canvas.coords(selFig['D'],10000, 10000, 10001, 10001)
        figures.remove(selFig['Obj'])


    # if tool == 8:
    #     # select object
    #
    #     for fig in figures:
    #         x1, y1, x2, y2 = coords(canvas, fig[0])
    #         if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
    #             # deleteObject(canvas, selFig)
    #             if selFig == {}:
    #                 pass
    #                 # makeSelFig(10000, 10000, 10001, 10001, fig)
    #             else:
    #                 canvas.coords(selFig['0'], x1 - 1, y1 - 1, x2 + 1, y2 + 1)
    #                 # canvas.coords(selFig['NW'], x1 - 10, y1 - 10, x1 + 10, y1 + 10)
    #                 # canvas.coords(selFig['NE'], x2 - 10, y1 - 10, x2 + 10, y1 + 10)
    #                 canvas.coords(selFig['SE'], x2 - 10, y2 - 10, x2 + 10, y2 + 10)
    #                 # canvas.coords(selFig['SW'], x1 - 10, y2 - 10, x1 + 10, y2 + 10)
    #                 # canvas.coords(selFig['S'], abs(x1 + x2) // 2 - 10, y2 - 10, abs(x1 + x2) // 2 + 10, y2 + 10)
    #                 # canvas.coords(selFig['E'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10, abs(y1 + y2) // 2 + 10)
    #
    #                 selFig['Obj'] = fig
    #             fl = True
    #             print("selFig ->", selFig)
    #             print("LEN ->", len(selFig))
    #             break
    #
    #
    # # repeat code
    # if tool == 8:
    #     # change cursor
    #     print (selFig)
    #     if selFig['0'] != None:
    #         try:
    #             x1, y1, x2, y2 = coords(canvas, selFig['0'])
    #             if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
    #                 canvas.config(cursor="fleur")
    #             else:
    #                 canvas.config(cursor="tcross")
    #         except:
    #             pass
    # if not fl:
    #     pass
    #     #selFig = {}
    xLineStart = 0
    yLineStart = 0


def create_canvas(frame):
    canvases.append(Canvas(frame))


def makeSelFig(x1, y1, x2, y2, Obj):
    global canvas, selFig
    # selFig = {}
    selFig['0'] = canvas.create_rectangle(x1 - 1, y1 - 1, x2 + 1, y2 + 1, width=1, outline="red", dash=(5, 5))
    # selFig['0'].config(cursor="fleur")
    # selFig['NW'] = canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, width=1, outline="red",                                      fill="yellow")
    # selFig['NE'] = canvas.create_oval(x2 - 10, y1 - 10, x2 + 10, y1 + 10, width=1, outline="red",                                      fill="yellow")
    # selFig['SE'] = canvas.create_rectangle(x2 - 20, y2 - 20, x2 + 1, y2 + 1, width=1, outline="red")

    # selFig['SW'] = canvas.create_oval(x1 - 10, y2 - 10, x1 + 10, y2 + 10, width=1, outline="red",                                      fill="yellow")
    # selFig['S'] = canvas.create_rectangle(abs(x1 + x2) // 2 - 10, y2 - 10, abs(x1 + x2) // 2 + 10,                                     y2 + 10, width=1, outline="red", fill="yellow")
    # selFig['E'] = canvas.create_rectangle(x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,                                          abs(y1 + y2) // 2 + 10, width=1, outline="red", fill="yellow")
    selFig['D'] = canvas.create_rectangle(x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,abs(y1 + y2) // 2 + 10, width=1, outline="red", fill="red")
    selFig['Obj'] = Obj


def expanse(d):
    global canvas, canvas_width, canvas_height, xc, yc
    if d == 'u':
        canvas_height += 100
        yc -= 100
    else:
        canvas_width += 100
        xc -= 100
    canvas.config(width=canvas_width, height=canvas_height)
    canvas.place(x=xc, y=yc)


def noSelectAll(frame1):
    for associated_widget in frame1.winfo_children():
        associated_widget.configure(bg='white')


def main():
    global canvas, color, canvas_width, canvas_height, screen_width, screen_height, selFig
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight() - 75
    root.geometry('' + str(screen_width) + 'x' + str(screen_height) + '+-7+0')
    root.title("WhiteBoard")
    frame = Frame(root, relief=RAISED, borderwidth=1)
    frame.pack(fill=BOTH, expand=True)
    canvas = Canvas(frame, bg=fonColor)
    canvas_width = screen_width + 50
    canvas_height = screen_height + 50
    canvas.place(x=xc, y=yc)
    canvas.config(width=canvas_width, height=canvas_height)
    canvas.config(cursor="tcross")
    grid(canvas, gridColor, screen_width + 50, screen_height + 50, 50, grList)
    # Кнопки розширення полотна
    btnDown = Button(text='V', width=4, height=1, command=lambda: expanse('u'))
    btnRight = Button(text='>', width=2, height=2, command=lambda: expanse('r'))

    btnDown.place(x=screen_width // 2, y=screen_height - 60)
    btnRight.place(x=screen_width - 25, y=screen_height // 2)

    frame1 = Frame(frame, relief=RAISED, borderwidth=1)
    frame1.pack(side=BOTTOM, fill=BOTH)
    images_path = {
        0: "img/pen.png", 1: "img/err.gif", 2: "img/hand.png", 3: "img/line.png", 4: "img/ClearFill.png",
        5: "img/_ClearFill.png", 6: "img/palitra.png", 7: "img/width.png", 8: "img/line 2px.png",
        9: "img/line 4px.png", 10: "img/line 8px.png", 11: "img/line 12px.png", 12: "img/line 16px.png",
        13: "img/line 20px.png", 14: "img/line 24px.png", 15: "img/arr.png", 16: "img/line 2px.png",
        17: "img/lineArr.png", 18: "img/bothArr.png", 19: "img/dot.png", 20: "img/line 2px.png",
        21: "img/punktir.png", 22: "img/shtrLine.png", 23: "img/options.png", 24: "img/open.png",
        25: "img/save.png", 26: "img/shot.png", 27: "img/add.png", 28: "img/ar.png", }
    images = []
    for i in images_path:
        images.append(ImageTk.PhotoImage(file=images_path[i]))

    def on_move_or_resize():
        # If windows is resizing
        w = root.winfo_width()
        h = root.winfo_height()
        btnDown.place(x=w // 2, y=h - 60)
        btnRight.place(x=w - 25, y=h // 2)

    def btnHandClick():
        print('Hand')
        global tool
        tool = 7
        noSelectAll(frame1)
        btnHand.config(bg=btnActiveColor)
        deleteSelectionLinks()

    def btnAddPageClick(root):
        global selFig
        print('Add Page')
        deleteSelectionLinks()
        print("selFig ->", selFig)
        print("LEN ->", len(selFig))

    def btnLineClick():
        print('Line')
        global tool
        tool = 3
        noSelectAll(frame1)
        btnLine.config(bg=btnActiveColor)
        deleteSelectionLinks()

    def btnErClick():
        print('Erazer')
        global tool
        tool = 2
        noSelectAll(frame1)
        btnEr.config(bg=btnActiveColor)
        deleteSelectionLinks()

    def btnRectClick():
        print('Rect')
        global tool
        global tool, brushColor
        if tool == 4:
            if brushColor == penColor:
                brushColor = ""
                btnRect.config(image=images[5])
            else:
                brushColor = penColor
                btnRect.config(image=images[4])
        print('Pen')
        tool = 4
        noSelectAll(frame1)
        btnRect.config(bg=btnActiveColor)
        deleteSelectionLinks()

        # selFig = {}

    def deleteSelectionLinks():
        global selFig, canvas
        deleteObject(canvas, selFig['0'])
        deleteObject(canvas, selFig['D'])
        # deleteObject(canvas, selFig['NW'])
        # deleteObject(canvas, selFig['NE'])
        # deleteObject(canvas, selFig['SE'])
        # deleteObject(canvas, selFig['SW'])
        # deleteObject(canvas, selFig['S'])
        # deleteObject(canvas, selFig['E'])

    def btnPenClick():
        global tool
        tool = 1
        noSelectAll(frame1)
        btnPen.config(bg=btnActiveColor)
        deleteSelectionLinks()

    def btnArClick():
        global tool, selFig
        tool = 8
        noSelectAll(frame1)
        btnAr.config(bg=btnActiveColor)
        deleteSelectionLinks()
        makeSelFig(10000, 10000, 10001, 10001, None)

    def btnColorSelectClick():
        print("Select color")
        global penColor
        penColor = colorchooser.askcolor()[1]
        deleteSelectionLinks()

    def widthClick(d):
        global penWidth
        penWidth = d
        frameWidth.pack_forget()
        deleteSelectionLinks()

    def arrowClick(d):
        global lineArrow
        lineArrow = d
        frameArrow.pack_forget()
        deleteSelectionLinks()

    def dotClick(d):
        global lineDot, selFig
        lineDot = d
        frameDot.pack_forget()
        deleteSelectionLinks()

    def btnWidthSelectClick():
        print("Select width")
        global penWidth
        frameWidth.pack(side=LEFT, padx=2, pady=2)
        deleteSelectionLinks()

    def btnOptionsClick():
        print("Settings")
        frameOptions.pack(side=LEFT, padx=2, pady=2)
        deleteSelectionLinks()

    def btnArrowSelectClick():
        print("Select arrow")
        frameArrow.pack(side=LEFT, padx=2, pady=2)
        deleteSelectionLinks()

    def btnDotSelectClick():
        print("Select dash")
        frameDot.pack(side=LEFT, padx=2, pady=2)
        deleteSelectionLinks()
        # image = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))
        #
        # image = ImageTk.PhotoImage(image)
        # root.image = image
        # im = canvas.create_image(50, 10, image=image, state=NORMAL, anchor=NW)
        # canvas.create_line(22,33,444,444)
        # canvas.update()

    # Buttons for main panel
    btnAr = Button(frame1, image=images[28], command=btnArClick, font="10")
    btnAr.pack(side=LEFT, padx=2, pady=2)
    btnPen = Button(frame1, image=images[0], command=btnPenClick, font="10")
    btnPen.pack(side=LEFT, padx=2, pady=2)
    btnEr = Button(frame1, image=images[1], command=btnErClick, font="10")
    btnEr.pack(side=LEFT, padx=2, pady=2)
    btnHand = Button(frame1, image=images[2], command=btnHandClick, font="10")
    btnHand.pack(side=LEFT, padx=2, pady=2)
    btnLine = Button(frame1, image=images[3], command=btnLineClick, font="10")
    btnLine.pack(side=LEFT, padx=2, pady=2)
    btnRect = Button(frame1, image=images[5], command=btnRectClick, font="10")
    btnRect.pack(side=LEFT, padx=2, pady=2)
    btnOptions = Button(frame1, image=images[23], command=btnOptionsClick, font="10")
    btnOptions.pack(side=LEFT, padx=2, pady=2)
    btnScr = Button(frame1, image=images[26], command=lambda: btnScrClick(root), font="10")
    btnScr.pack(side=LEFT, padx=2, pady=2)
    btnAddPage = Button(frame1, image=images[27], command=lambda: btnAddPageClick(root), font="10")
    btnAddPage.pack(side=LEFT, padx=2, pady=2)

    # Buttons for main panel switching another panels
    btnColorSelect = Button(frame1, image=images[6], command=btnColorSelectClick, font="10")
    btnColorSelect.pack(side=LEFT, padx=2, pady=2)
    btnWidthSelect = Button(frame1, image=images[7], command=btnWidthSelectClick, font="10")
    btnWidthSelect.pack(side=LEFT, padx=2, pady=2)
    btnArrowSelect = Button(frame1, image=images[15], command=btnArrowSelectClick, font="10")
    btnArrowSelect.pack(side=LEFT, padx=2, pady=2)
    btnDotSelect = Button(frame1, image=images[19], command=btnDotSelectClick, font="10")
    btnDotSelect.pack(side=LEFT, padx=2, pady=2)

    btnSave = Button(frame1, image=images[25], command=save, font="10")
    btnSave.pack(side=LEFT, padx=2, pady=2)
    btnLoad = Button(frame1, image=images[24], command=lambda: load(canvas, root), font="10")
    btnLoad.pack(side=LEFT, padx=2, pady=2)

    # Panel select width arrow
    frameWidth = Frame(frame1)
    frameWidth.pack_forget()
    btnWidth2 = Button(frameWidth, image=images[8], command=lambda: widthClick(2), font="10")
    btnWidth2.pack(side=LEFT, padx=2, pady=2)
    btnWidth4 = Button(frameWidth, image=images[9], command=lambda: widthClick(4), font="10")
    btnWidth4.pack(side=LEFT, padx=2, pady=2)
    btnWidth8 = Button(frameWidth, image=images[10], command=lambda: widthClick(6), font="10")
    btnWidth8.pack(side=LEFT, padx=2, pady=2)
    btnWidth12 = Button(frameWidth, image=images[11], command=lambda: widthClick(8), font="10")
    btnWidth12.pack(side=LEFT, padx=2, pady=2)
    btnWidth16 = Button(frameWidth, image=images[12], command=lambda: widthClick(10), font="12")
    btnWidth16.pack(side=LEFT, padx=2, pady=2)
    btnWidth20 = Button(frameWidth, image=images[13], command=lambda: widthClick(12), font="14")
    btnWidth20.pack(side=LEFT, padx=2, pady=2)
    btnWidth24 = Button(frameWidth, image=images[14], command=lambda: widthClick(16), font="16")
    btnWidth24.pack(side=LEFT, padx=2, pady=2)
    frameArrow = Frame(frame1)
    frameArrow.pack_forget()
    btnArrow1 = Button(frameArrow, image=images[16], command=lambda: arrowClick(''), font="10")
    btnArrow1.pack(side=LEFT, padx=2, pady=2)
    btnArrow2 = Button(frameArrow, image=images[17], command=lambda: arrowClick(LAST), font="10")
    btnArrow2.pack(side=LEFT, padx=2, pady=2)
    btnArrow3 = Button(frameArrow, image=images[18], command=lambda: arrowClick(BOTH), font="10")
    btnArrow3.pack(side=LEFT, padx=2, pady=2)
    frameDot = Frame(frame1)
    frameDot.pack_forget()
    btnArrow1 = Button(frameDot, image=images[20], command=lambda: dotClick(''), font="10")
    btnArrow1.pack(side=LEFT, padx=2, pady=2)
    btnArrow2 = Button(frameDot, image=images[21], command=lambda: dotClick((5, 5)), font="10")
    btnArrow2.pack(side=LEFT, padx=2, pady=2)
    btnArrow3 = Button(frameDot, image=images[22], command=lambda: dotClick((20, 20)), font="10")
    btnArrow3.pack(side=LEFT, padx=2, pady=2)
    frameOptions = Frame(frame1)
    frameOptions.pack_forget()
    chbGrid = Checkbutton(frameOptions, text='grid')
    chbGrid.pack(side=LEFT, padx=2, pady=2)

    makeSelFig(10000, 10000, 10001, 10001, None)

    root.bind("<Key>", f_quit)
    canvas.bind("<Button-1>", mouseDown)
    canvas.bind("<B1-Motion>", mouseMove)
    canvas.bind("<Motion>", mouseMoveNoButton)
    canvas.bind("<ButtonRelease-1>", mouseUp)
    root.bind('<Configure>', lambda e: on_move_or_resize())

    color = "blue"
    # TODO check directories tmp and lessons. If no - create them

    print(root.wm_geometry())

    root.mainloop()


if __name__ == '__main__':
    main()
