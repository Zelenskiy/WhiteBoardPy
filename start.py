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


def btnScrInsertInCanvasClick(root, floatWindow, winVar):
    print('btnClick')

    width = 600
    winVar['window_width'] = root.winfo_width()
    winVar['window_height'] = root.winfo_height()
    x0 = -winVar['xc'] + winVar['window_width'] - width - 40
    y0 = -winVar['yc'] + 20
    name = 'tmp/' + datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S") + '.png'
    image = (pyautogui.screenshot(region=(0, 0, winVar['screen_width'], winVar['screen_height'] + 75)))
    image.save(name)

    k = winVar['screen_width'] / (winVar['screen_height'] + 75)
    height = int(width / k)
    image = image.resize((width, height), Image.ANTIALIAS)
    root.wm_state('normal')
    winVar['images'].append(ImageTk.PhotoImage(image))
    k = []
    c = {}
    c['name'] = name
    c['x'] = x0
    c['y'] = y0
    c['width'] = width
    c['height'] = height
    k.append(winVar['canvas'].create_image(x0, y0, image=winVar['images'][-1], state=NORMAL, anchor=NW))
    k.append("image")
    k.append(c)
    winVar['figures'].append(k)
    print(winVar['images'])

    floatWindow.destroy()


def btnScrClick(root, winVar):
    print("out-", winVar['figures'])
    print('btnScrClick')
    root.wm_state('iconic')
    floatWindow = Tk()
    floatWindow.geometry("40x35+20+20")
    btnScrInsertInCanvas = Button(floatWindow, text='Sr',
                                  command=lambda root=root, floatWindow=floatWindow,
                                                 winVar=winVar: btnScrInsertInCanvasClick(root, floatWindow, winVar))
    floatWindow.overrideredirect(1)
    floatWindow.wm_attributes("-topmost", True)
    btnScrInsertInCanvas.pack(fill=BOTH, expand=True)


def save(winVar):
    data = {}
    data['figures'] = winVar['figures']
    data['penColor'] = winVar['penColor']
    data['brushColor'] = winVar['brushColor']
    data['penWidth'] = winVar['penWidth']
    data['fonColor'] = winVar['fonColor']
    data['canvas_width'] = winVar['canvas_width']
    data['canvas_height'] = winVar['canvas_height']
    data['xc'] = winVar['xc']
    data['yc'] = winVar['yc']

    with open("test.wb", "wb") as fp:
        pickle.dump(data, fp)


def load(root, winVar):
    winVar['canvas'].delete(ALL)
    winVar['figures'] = []
    winVar['images'] = []
    # winVar['tool'] = 1
    btnPenClick()
    with open("test.wb", "rb") as fp:  # Unpickling
        data = pickle.load(fp)
    winVar['figures'] = data['figures']
    winVar['penColor'] = data['penColor']
    winVar['brushColor'] = data['brushColor']
    winVar['penWidth'] = data['penWidth']
    winVar['fonColor'] = data['fonColor']
    winVar['canvas_width'] = data['canvas_width']
    winVar['canvas_height'] = data['canvas_height']
    winVar['xc'] = data['xc']
    winVar['yc'] = data['yc']
    # change size and position canvas
    winVar['canvas'].place(x=winVar['xc'], y=winVar['yc'])
    winVar['canvas'].config(width=winVar['canvas_width'], height=winVar['canvas_height'])
    grid(winVar)

    for fig in winVar['figures']:
        f = fig[2]
        if fig[1] == 'oval':
            fig[0] = winVar['canvas'].create_oval(f['x1'], f['y1'], f['x2'], f['y2'], outline=f['outline'],
                                                  fill=f['fill'], width=f['width'])
        elif fig[1] == 'line':
            winVar['canvas'].create_line(f['x1'], f['y1'], f['x2'], f['y2'],
                                         arrow=f['arrow'], dash=f['dash'], fill=f['fill'], width=f['width'])


        elif fig[1] == 'rectangle':
            fig[0] = winVar['canvas'].create_polygon(f['x1'], f['y1'], f['x2'], f['y2'], f['x3'], f['y3'], f['x4'],
                                                     f['y4'],
                                                     width=f['width'], fill=f['fill'],
                                                     outline=f['outline'])
        elif fig[1] == 'image':
            width = f['width']
            height = f['height']
            image = Image.open(f['name'])
            image = image.resize((width, height), Image.ANTIALIAS)
            winVar['images'].append(ImageTk.PhotoImage(image))
            fig[0] = winVar['canvas'].create_image(f['x'], f['y'], image=winVar['images'][-1], state=NORMAL, anchor=NW)


def f_quit(event):
    if event.keysym == 'Escape':
        quit()


def mouseDown(event, winVar):
    if winVar['tool'] == 8:
        # select object

        for fig in winVar['figures']:
            x1, y1, x2, y2 = coords(winVar['canvas'], fig[0])
            if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
                if winVar['selFig'] == {}:
                    pass
                else:
                    winVar['canvas'].coords(winVar['selFig']['0'], x1 - 1, y1 - 1, x2 + 1, y2 + 1)
                    # winVar['canvas'].coords(selFig['SE'], max(x2, x1) - 20, max(y2, y1) - 20, max(x2, x1), max(y2, y1))

                    winVar['canvas'].coords(winVar['selFig']['D'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,
                                            abs(y1 + y2) // 2 + 10)
                    # winVar['canvas'].coords(selFig['NW'], x1 - 10, y1 - 10, x1 + 10, y1 + 10)
                    # winVar['canvas'].coords(selFig['NE'], x2 - 10, y1 - 10, x2 + 10, y1 + 10)
                    # winVar['canvas'].coords(selFig['SW'], x1 - 10, y2 - 10, x1 + 10, y2 + 10)
                    # winVar['canvas'].coords(selFig['S'], abs(x1 + x2) // 2 - 10, y2 - 10, abs(x1 + x2) // 2 + 10, y2 + 10)
                    # winVar['canvas'].coords(selFig['E'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10, abs(y1 + y2) // 2 + 10)

                    winVar['selFig']['Obj'] = fig
                fl = True
                break

    # repeat code
    fl = False
    if winVar['tool'] == 8:

        # change cursor
        print(winVar['selFig'])
        if winVar['selFig']['0'] != None:
            try:
                x1, y1, x2, y2 = coords(winVar['canvas'], winVar['selFig']['0'])
                if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
                    winVar['canvas'].config(cursor="fleur")
                else:
                    winVar['canvas'].config(cursor="tcross")
            except:
                pass
    if not fl:
        pass
        # selFig = {}


def mouseMove(event, winVar):
    xx = ""
    if winVar['xStart'] == 0 and winVar['yStart'] == 0 and winVar['tool'] != 3 and winVar['tool'] != 4:
        winVar['xStart'] = event.x
        winVar['yStart'] = event.y

    if winVar['tool'] == 1:
        penMove(winVar, event.x, event.y)
        # penMove(penColor, xStart, yStart, penWidth, canvas, figures, event.x, event.y)

    elif winVar['tool'] == 2:
        erMove(winVar, event.x, event.y)
        # erMove(errSize, canvas, figures, event.x, event.y)
    elif winVar['tool'] == 7:
        dx = event.x - winVar['xStart']
        dy = event.y - winVar['yStart']
        winVar['xc'] += dx
        if winVar['xc'] > 0:
            winVar['xc'] -= dx
        winVar['yc'] += dy
        if winVar['yc'] > 0:
            winVar['yc'] -= dy
        winVar['canvas'].place(x=winVar['xc'], y=winVar['yc'])
        if winVar['xc'] + (0) > 0:
            pass
    #     TODO make for expanding if drag canvas out borger

    elif winVar['tool'] == 3:
        # line
        if winVar['xStart'] == 0 and winVar['yStart'] == 0:
            winVar['xLineStart'] = event.x
            winVar['yLineStart'] = event.y
            winVar['line0'] = winVar['canvas'].create_line(winVar['xLineStart'], winVar['yLineStart'],
                                                           winVar['xLineStart'],
                                                           winVar['yLineStart'], width=winVar['penWidth'],
                                                           fill=winVar['penColor'], arrow=winVar['lineArrow'],
                                                           dash=winVar['lineDot'])
            winVar['cLine0'] = {}
            winVar['cLine0']['x1'] = winVar['xLineStart']
            winVar['cLine0']['y1'] = winVar['yLineStart']
            winVar['cLine0']['x2'] = winVar['xLineStart']
            winVar['cLine0']['y2'] = winVar['yLineStart']
            winVar['cLine0']['width'] = winVar['penWidth']
            winVar['cLine0']['fill'] = winVar['penColor']
            winVar['cLine0']['arrow'] = winVar['lineArrow']
            winVar['cLine0']['dash'] = winVar['lineDot']

        else:
            winVar['canvas'].coords(winVar['line0'], winVar['xLineStart'], winVar['yLineStart'], event.x, event.y)
            winVar['cLine0']['x1'] = winVar['xLineStart']
            winVar['cLine0']['y1'] = winVar['yLineStart']
            winVar['cLine0']['x2'] = event.x
            winVar['cLine0']['y2'] = event.y

    elif winVar['tool'] == 4:
        # rectangle
        if winVar['xStart'] == 0 and winVar['yStart'] == 0:
            winVar['xLineStart'] = event.x
            winVar['yLineStart'] = event.y
            winVar['line0'] = winVar['canvas'].create_polygon([winVar['xLineStart'], winVar['yLineStart']],
                                                              [winVar['xLineStart'], winVar['yLineStart']],
                                                              [winVar['xLineStart'], winVar['yLineStart']],
                                                              [winVar['xLineStart'], winVar['yLineStart']],
                                                              width=winVar['penWidth'], outline=winVar['penColor'],
                                                              fill=winVar['brushColor'])
            winVar['cLine0'] = {}
        else:
            winVar['canvas'].coords(winVar['line0'], winVar['xLineStart'], winVar['yLineStart'], winVar['xLineStart'],
                                    event.y, event.x, event.y, event.x, winVar['yLineStart'])
            winVar['cLine0'] = {}
            winVar['cLine0']['x1'] = winVar['xLineStart']
            winVar['cLine0']['y1'] = winVar['yLineStart']
            winVar['cLine0']['x2'] = event.x
            winVar['cLine0']['y2'] = winVar['yLineStart']
            winVar['cLine0']['x3'] = event.x
            winVar['cLine0']['y3'] = event.y
            winVar['cLine0']['x4'] = winVar['xLineStart']
            winVar['cLine0']['y4'] = event.y

            winVar['cLine0']['width'] = winVar['penWidth']
            winVar['cLine0']['outline'] = winVar['penColor']
            winVar['cLine0']['fill'] = winVar['brushColor']
    elif winVar['tool'] == 8:
        # draging figure

        xo1, yo1, xo2, yo2 = coords(winVar['canvas'], winVar['selFig']['Obj'][0])
        if math.sqrt((event.x - xo2) ** 2 + (event.y - yo2) ** 2) < 20:
            print("!!!!!!!!!!!!!!!!!!!!!!")
            x1 = winVar['selFig']['Obj'][2]['x1']
            y1 = winVar['selFig']['Obj'][2]['y1']
            x2 = winVar['selFig']['Obj'][2]['x2']
            y2 = winVar['selFig']['Obj'][2]['y2']

            if x2 > x1 and y2 > y1:
                print(11111111)
                winVar['canvas'].coords(winVar['selFig']['Obj'][0], x1, y1, event.x, event.y)
                winVar['canvas'].coords(winVar['selFig']['0'], xo1 - 1, yo1 - 1, event.x + 1, event.y + 1)
                winVar['canvas'].coords(winVar['selFig']['D'], event.x - 10, (yo1 + event.y) // 2 - 10, event.x + 10,
                                        (yo1 + event.y) // 2 + 10)
                winVar['selFig']['Obj'][2]['x2'] = event.x
                winVar['selFig']['Obj'][2]['y2'] = event.y
            elif x2 < x1 and y2 > y1:
                winVar['canvas'].coords(winVar['selFig']['Obj'][0], event.x, y1, x2, event.y)
                winVar['canvas'].coords(winVar['selFig']['0'], xo1 - 1, yo1 - 1, event.x + 1, event.y + 1)
                winVar['canvas'].coords(winVar['selFig']['D'], event.x - 10, (yo1 + event.y) // 2 - 10, event.x + 10,
                                        (yo1 + event.y) // 2 + 10)
                winVar['selFig']['Obj'][2]['x1'] = event.x
                winVar['selFig']['Obj'][2]['y2'] = event.y
            elif x2 < x1 and y2 < y1:
                winVar['canvas'].coords(winVar['selFig']['Obj'][0], event.x, event.y, x2, y2)
                winVar['canvas'].coords(winVar['selFig']['0'], xo1 - 1, yo1 - 1, event.x + 1, event.y + 1)
                winVar['canvas'].coords(winVar['selFig']['D'], event.x - 10, (yo1 + event.y) // 2 - 10, event.x + 10,
                                        (yo1 + event.y) // 2 + 10)
                winVar['selFig']['Obj'][2]['x1'] = event.x
                winVar['selFig']['Obj'][2]['y1'] = event.y
            elif x2 > x1 and y2 < y1:
                winVar['canvas'].coords(winVar['selFig']['Obj'][0], x1, event.y, event.x, y2)
                winVar['canvas'].coords(winVar['selFig']['0'], xo1 - 1, yo1 - 1, event.x + 1, event.y + 1)
                winVar['canvas'].coords(winVar['selFig']['D'], event.x - 10, (yo1 + event.y) // 2 - 10, event.x + 10,
                                        (yo1 + event.y) // 2 + 10)
                winVar['selFig']['Obj'][2]['x2'] = event.x
                winVar['selFig']['Obj'][2]['y1'] = event.y

            # x3 = event.x
            # y3 = event.y
            # winVar['canvas'].coords(selFig['Obj'][0], x1, y1, x2, y2)
            # winVar['canvas'].coords(selFig['0'], x1 - 1, y1 - 1, x2 + 1, y2 + 1)
            # selFig['Obj'][2]['x1'] = x1
            # selFig['Obj'][2]['y1'] = y1
            # selFig['Obj'][2]['x2'] = x2
            # selFig['Obj'][2]['y2'] = y2

            xx = "resize"
        else:
            x1, y1, x2, y2 = coords(winVar['canvas'], winVar['selFig']['Obj'][0])
            if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
                # draging
                if winVar['selFig']['Obj'][1] == 'rectangle':
                    x1 = winVar['selFig']['Obj'][2]['x1']
                    y1 = winVar['selFig']['Obj'][2]['y1']
                    x2 = winVar['selFig']['Obj'][2]['x2']
                    y2 = winVar['selFig']['Obj'][2]['y2']
                    x3 = winVar['selFig']['Obj'][2]['x3']
                    y3 = winVar['selFig']['Obj'][2]['y3']
                    x4 = winVar['selFig']['Obj'][2]['x4']
                    y4 = winVar['selFig']['Obj'][2]['y4']
                    dx = event.x - winVar['xStart']
                    dy = event.y - winVar['yStart']
                    winVar['selFig']['Obj'][2]['x1'] = x1 + dx
                    winVar['selFig']['Obj'][2]['y1'] = y1 + dy
                    winVar['selFig']['Obj'][2]['x2'] = x2 + dx
                    winVar['selFig']['Obj'][2]['y2'] = y2 + dy
                    winVar['selFig']['Obj'][2]['x3'] = x3 + dx
                    winVar['selFig']['Obj'][2]['y3'] = y3 + dy
                    winVar['selFig']['Obj'][2]['x4'] = x4 + dx
                    winVar['selFig']['Obj'][2]['y4'] = y4 + dy
                    # moveObjectBy(canvas,  winVar['selFig']['Obj'][0], dx, dy)
                    # winVar['canvas'].coords( winVar['selFig']['0'], x1 - 1, y1 - 1, x3 + 1, y3 + 1)
                    # winVar['canvas'].coords( winVar['selFig']['SE'], max(x3,x1) - 10, max(y3,y1) - 10, max(x3,x1) + 10, max(y3,y1) + 10)
                elif winVar['selFig']['Obj'][1] == 'line':
                    x1 = winVar['selFig']['Obj'][2]['x1']
                    y1 = winVar['selFig']['Obj'][2]['y1']
                    x3 = winVar['selFig']['Obj'][2]['x2']
                    y3 = winVar['selFig']['Obj'][2]['y2']
                    dx = event.x - winVar['xStart']
                    dy = event.y - winVar['yStart']
                    winVar['selFig']['Obj'][2]['x1'] = x1 + dx
                    winVar['selFig']['Obj'][2]['y1'] = y1 + dy
                    winVar['selFig']['Obj'][2]['x2'] = x3 + dx
                    winVar['selFig']['Obj'][2]['y2'] = y3 + dy
                elif winVar['selFig']['Obj'][1] == 'image':
                    x = winVar['selFig']['Obj'][2]['x']
                    y = winVar['selFig']['Obj'][2]['y']
                    w = winVar['selFig']['Obj'][2]['width']
                    h = winVar['selFig']['Obj'][2]['height']
                    dx = event.x - winVar['xStart']
                    dy = event.y - winVar['yStart']
                    winVar['selFig']['Obj'][2]['x'] = x + dx
                    winVar['selFig']['Obj'][2]['y'] = y + dy
                    winVar['selFig']['Obj'][2]['width'] = w
                    winVar['selFig']['Obj'][2]['height'] = h
                    winVar['canvas'].coords(winVar['selFig']['Obj'][0], x + dx, y + dy)
                    winVar['canvas'].coords(winVar['selFig']['0'], coords(winVar['canvas'], winVar['selFig']['Obj'][0]))
                    x1, y1, x2, y2 = coords(winVar['canvas'], winVar['selFig']['Obj'][0])
                    winVar['canvas'].coords(winVar['selFig']['D'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,
                                            abs(y1 + y2) // 2 + 10)

                if xx != "resize" and winVar['selFig']['Obj'][1] != 'image':
                    moveObjectBy(winVar['canvas'], winVar['selFig']['Obj'][0], dx, dy)
                    winVar['canvas'].coords(winVar['selFig']['0'], coords(winVar['canvas'], winVar['selFig']['Obj'][0]))
                    x1, y1, x2, y2 = coords(winVar['canvas'], winVar['selFig']['Obj'][0])
                    winVar['canvas'].coords(winVar['selFig']['D'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,
                                            abs(y1 + y2) // 2 + 10)
                    # winVar['canvas'].coords( winVar['selFig']['SE'], max(x3, x1) - 10, max(y3, y1) - 10, max(x3, x1) + 10, max(y3, y1) + 10)

    if winVar['tool'] != 8:
        if winVar['selFig'] != {}:
            winVar['canvas'].coords(winVar['selFig'], 100000, 100000, 1000001, 100001)
            # selFig = {}

    winVar['xStart'] = event.x
    winVar['yStart'] = event.y


def mouseMoveNoButton(event, winVar):
    if winVar['tool'] == 8:
        # change cursor
        try:

            if not winVar['selFig']['Obj'] is None:
                x1, y1, x2, y2 = coords(winVar['canvas'], winVar['selFig']['0'])
                if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
                    winVar['canvas'].config(cursor="fleur")
                else:
                    winVar['canvas'].config(cursor="tcross")
        except:
            pass


def mouseUp(event, winVar):
    # global xStart, yStart, cLine0, line0, xLineStart, yLineStart, selFig
    winVar['xStart'] = 0
    winVar['yStart'] = 0
    fl = False
    if winVar['tool'] == 3 or winVar['tool'] == 4:
        k = []
        k.append(winVar['line0'])
        if winVar['tool'] == 3:
            k.append("line")
        else:
            k.append("rectangle")
        k.append(winVar['cLine0'])
        winVar['figures'].append(k)
        print(winVar['figures'])
    print(winVar['selFig']['D'])
    if coords(winVar['canvas'], winVar['selFig']['D']) != None:
        x1, y1, x2, y2 = coords(winVar['canvas'], winVar['selFig']['D'])
        if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
            winVar['canvas'].delete(winVar['selFig']['Obj'][0])
            winVar['canvas'].coords(winVar['selFig']['0'], 10000, 10000, 10001, 10001)
            winVar['canvas'].coords(winVar['selFig']['D'], 10000, 10000, 10001, 10001)
            winVar['figures'].remove(winVar['selFig']['Obj'])

    winVar['xLineStart'] = 0
    winVar['yLineStart'] = 0


#
# def create_canvas(frame):
#     canvases.append(Canvas(frame))


def makeSelFig(winVar, x1, y1, x2, y2, Obj):
    canvas = winVar['canvas']
    # selFig = {}
    winVar['selFig']['0'] = winVar['canvas'].create_rectangle(x1 - 1, y1 - 1, x2 + 1, y2 + 1, width=1, outline="red",
                                                              dash=(5, 5))
    # selFig['0'].config(cursor="fleur")
    # selFig['NW'] = winVar['canvas'].create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, width=1, outline="red",                                      fill="yellow")
    # selFig['NE'] = winVar['canvas'].create_oval(x2 - 10, y1 - 10, x2 + 10, y1 + 10, width=1, outline="red",                                      fill="yellow")
    # selFig['SE'] = winVar['canvas'].create_rectangle(x2 - 20, y2 - 20, x2 + 1, y2 + 1, width=1, outline="red")

    # selFig['SW'] = winVar['canvas'].create_oval(x1 - 10, y2 - 10, x1 + 10, y2 + 10, width=1, outline="red",                                      fill="yellow")
    # selFig['S'] = winVar['canvas'].create_rectangle(abs(x1 + x2) // 2 - 10, y2 - 10, abs(x1 + x2) // 2 + 10,                                     y2 + 10, width=1, outline="red", fill="yellow")
    # selFig['E'] = winVar['canvas'].create_rectangle(x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,                                          abs(y1 + y2) // 2 + 10, width=1, outline="red", fill="yellow")
    winVar['selFig']['D'] = winVar['canvas'].create_rectangle(x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,
                                                              abs(y1 + y2) // 2 + 10, width=1,
                                                              outline="red", fill="red")
    winVar['selFig']['Obj'] = Obj


def expanse(d, winVar):
    # global canvas, canvas_width, canvas_height, xc, yc
    if d == 'u':
        winVar['canvas_height'] += 100
        winVar['yc'] -= 100
    else:
        winVar['canvas_width'] += 100
        winVar['xc'] -= 100
    winVar['canvas'].config(width=winVar['canvas_width'], height=winVar['canvas_height'])
    winVar['canvas'].place(x=winVar['xc'], y=winVar['yc'])


def noSelectAll(frame1):
    for associated_widget in frame1.winfo_children():
        associated_widget.configure(bg='white')

#
# def btnPenClick(root, winVar):
#     winVar['tool'] = 1
#
#     noSelectAll(root.winfo_children()[1])
#     print(root.winfo_children())
#     btnPen.config(bg=winVar['btnActiveColor'])
#     deleteSelectionLinks()


def main():
    winVar = {}
    root = Tk()

    winVar['screen_width'] = root.winfo_screenwidth() - 200  # TODO
    winVar['screen_height'] = root.winfo_screenheight() - 75
    # TODO
    root.geometry('' + str(winVar['screen_width']) + 'x' + str(winVar['screen_height']) + '+200+0')
    # root.geometry('' + str(winVar['screen_width']) + 'x' + str(winVar['screen_height']) + '+-7+0')
    root.title("WhiteBoard")
    frame = Frame(root, relief=RAISED, borderwidth=1)
    frame.pack(fill=BOTH, expand=True)

    winVar['fonColor'] = "#E9FBCA"
    winVar['brushColor'] = ""
    winVar['btnActiveColor'] = "#331177"
    winVar['canvas'] = Canvas(frame, bg=winVar['fonColor'])
    winVar['window_height'] = root.winfo_height()
    winVar['window_width'] = root.winfo_width()

    winVar['xc'] = 0
    winVar['yc'] = 0
    winVar['canvas_height'] = winVar['screen_height'] + 50
    winVar['canvas_width'] = winVar['screen_width'] + 50
    winVar['canvas'].config(cursor="tcross")
    winVar['canvas'].config(width=winVar['canvas_width'], height=winVar['canvas_height'])
    winVar['canvas'].place(x=winVar['xc'], y=winVar['yc'])
    winVar['canvases'] = []
    winVar['cLine0'] = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0}

    winVar['cpFigures'] = []
    winVar['errSize'] = 10
    winVar['figures'] = []

    winVar['gridColor'] = "#D0D0D0"
    winVar['grList'] = []

    winVar['lineArrow'] = ""
    winVar['lineDot'] = ''
    winVar['penColor'] = "#0000FF"
    winVar['penWidth'] = 2
    winVar['selFig'] = {}
    winVar['step'] = 50
    winVar['tool'] = 1

    winVar['xLineStart'] = 0
    winVar['xStart'] = 0

    winVar['yLineStart'] = 0
    winVar['yStart'] = 0
    winVar['images'] = []

    grid(winVar)
    # Кнопки розширення полотна
    btnDown = Button(text='V', width=4, height=1, command=lambda d='u', winVar=winVar: expanse(d, winVar))
    btnRight = Button(text='>', width=2, height=2, command=lambda d='r', winVar=winVar: expanse(d, winVar))

    btnDown.place(x=winVar['screen_width'] // 2, y=winVar['screen_height'] - 60)
    btnRight.place(x=winVar['screen_width'] - 25, y=winVar['screen_height'] // 2)

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

    def on_move_or_resize(event, root, winVar):
        # If windows is resizing
        w = root.winfo_width()
        h = root.winfo_height()
        winVar['window_width'], winVar['window_height'] = w, h
        btnDown.place(x=w // 2, y=h - 60)
        btnRight.place(x=w - 25, y=h // 2)

    def btnHandClick():
        print('Hand')
        winVar['tool'] = 7
        noSelectAll(frame1)
        btnHand.config(bg=winVar['btnActiveColor'])
        deleteSelectionLinks()

    def btnAddPageClick(root):
        print('Add Page')
        deleteSelectionLinks()
        print("selFig ->", winVar['selFig'])
        print("LEN ->", len(winVar['selFig']))

    def btnLineClick():
        print('Line')
        winVar['tool'] = 3
        noSelectAll(frame1)
        btnLine.config(bg=winVar['btnActiveColor'])
        deleteSelectionLinks()

    def btnErClick():
        print('Erazer')
        winVar['tool'] = 2
        noSelectAll(frame1)
        btnEr.config(bg=winVar['btnActiveColor'])
        deleteSelectionLinks()

    def btnRectClick():
        print('Rect')

        if winVar['tool'] == 4:
            if winVar['brushColor'] == winVar['penColor']:
                winVar['brushColor'] = ""
                btnRect.config(image=images[5])
            else:
                winVar['brushColor'] = winVar['penColor']
                btnRect.config(image=images[4])
        print('Pen')
        winVar['tool'] = 4
        noSelectAll(frame1)
        btnRect.config(bg=winVar['btnActiveColor'])
        deleteSelectionLinks()

        # selFig = {}

    def deleteSelectionLinks():
        deleteObject(winVar['canvas'], winVar['selFig']['0'])
        deleteObject(winVar['canvas'], winVar['selFig']['D'])

    def btnPenClick(root, winVar):
        winVar['tool'] = 1
        noSelectAll(frame1)
        btnPen.config(bg=winVar['btnActiveColor'])
        deleteSelectionLinks()

    def btnArClick():
        winVar['tool'] = 8
        noSelectAll(frame1)
        btnAr.config(bg=winVar['btnActiveColor'])
        deleteSelectionLinks()
        makeSelFig(winVar, 10000, 10000, 10001, 10001, None)

    def btnColorSelectClick():
        print("Select color")
        winVar['penColor'] = colorchooser.askcolor()[1]
        deleteSelectionLinks()

    def widthClick(d, winVar):
        winVar['penWidth'] = d
        frameWidth.pack_forget()
        deleteSelectionLinks()

    def arrowClick(d, winVar):
        winVar['lineArrow'] = d
        frameArrow.pack_forget()
        deleteSelectionLinks()

    def dotClick(d, winVar):
        winVar['lineDot'] = d
        frameDot.pack_forget()
        deleteSelectionLinks()

    def btnWidthSelectClick():
        print("Select width")
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

    # Buttons for main panel
    btnAr = Button(frame1, image=images[28], command=btnArClick, font="10")
    btnAr.pack(side=LEFT, padx=2, pady=2)
    btnPen = Button(frame1, image=images[0], command=lambda root=root, winVar=winVar: btnPenClick(root, winVar),
                    font="10")
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
    btnScr = Button(frame1, image=images[26], command=lambda: btnScrClick(root, winVar))
    btnScr.pack(side=LEFT, padx=2, pady=2)
    btnAddPage = Button(frame1, image=images[27], command=lambda: btnAddPageClick(root, winVar), font="10")
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

    btnSave = Button(frame1, image=images[25], command=lambda winVar=winVar: save(winVar), font="10")
    btnSave.pack(side=LEFT, padx=2, pady=2)
    btnLoad = Button(frame1, image=images[24], command=lambda root=root, winVar=winVar: load(root, winVar), font="10")
    btnLoad.pack(side=LEFT, padx=2, pady=2)

    # Panel select width arrow
    frameWidth = Frame(frame1)
    frameWidth.pack_forget()
    btnWidth2 = Button(frameWidth, image=images[8], command=lambda: widthClick(2, winVar), font="10")
    btnWidth2.pack(side=LEFT, padx=2, pady=2)
    btnWidth4 = Button(frameWidth, image=images[9], command=lambda: widthClick(4, winVar), font="10")
    btnWidth4.pack(side=LEFT, padx=2, pady=2)
    btnWidth8 = Button(frameWidth, image=images[10], command=lambda: widthClick(6, winVar), font="10")
    btnWidth8.pack(side=LEFT, padx=2, pady=2)
    btnWidth12 = Button(frameWidth, image=images[11], command=lambda: widthClick(8, winVar), font="10")
    btnWidth12.pack(side=LEFT, padx=2, pady=2)
    btnWidth16 = Button(frameWidth, image=images[12], command=lambda: widthClick(10, winVar), font="12")
    btnWidth16.pack(side=LEFT, padx=2, pady=2)
    btnWidth20 = Button(frameWidth, image=images[13], command=lambda: widthClick(12, winVar), font="14")
    btnWidth20.pack(side=LEFT, padx=2, pady=2)
    btnWidth24 = Button(frameWidth, image=images[14], command=lambda: widthClick(16), font="16")
    btnWidth24.pack(side=LEFT, padx=2, pady=2)
    frameArrow = Frame(frame1)
    frameArrow.pack_forget()
    btnArrow1 = Button(frameArrow, image=images[16], command=lambda d='', winVar=winVar: arrowClick(d, winVar),
                       font="10")
    btnArrow1.pack(side=LEFT, padx=2, pady=2)
    btnArrow2 = Button(frameArrow, image=images[17], command=lambda d=LAST, winVar=winVar: arrowClick(d, winVar),
                       font="10")
    btnArrow2.pack(side=LEFT, padx=2, pady=2)
    btnArrow3 = Button(frameArrow, image=images[18], command=lambda d=BOTH, winVar=winVar: arrowClick(d, winVar),
                       font="10")
    btnArrow3.pack(side=LEFT, padx=2, pady=2)
    frameDot = Frame(frame1)
    frameDot.pack_forget()
    btnArrow1 = Button(frameDot, image=images[20], command=lambda d='', winVar=winVar: dotClick(d, winVar), font="10")
    btnArrow1.pack(side=LEFT, padx=2, pady=2)
    btnArrow2 = Button(frameDot, image=images[21], command=lambda d=(5, 5), winVar=winVar: dotClick(d, winVar),
                       font="10")
    btnArrow2.pack(side=LEFT, padx=2, pady=2)
    btnArrow3 = Button(frameDot, image=images[22], command=lambda d=(10, 2), winVar=winVar: dotClick(d, winVar),
                       font="10")
    btnArrow3.pack(side=LEFT, padx=2, pady=2)
    frameOptions = Frame(frame1)
    frameOptions.pack_forget()
    chbGrid = Checkbutton(frameOptions, text='grid')
    chbGrid.pack(side=LEFT, padx=2, pady=2)

    makeSelFig(winVar, 10000, 10000, 10001, 10001, None)

    root.bind("<Key>", f_quit)
    winVar['canvas'].bind("<Button-1>", lambda event, winVar=winVar: mouseDown(event, winVar))
    winVar['canvas'].bind("<B1-Motion>", lambda event, winVar=winVar: mouseMove(event, winVar))
    winVar['canvas'].bind("<Motion>", lambda event, winVar=winVar: mouseMoveNoButton(event, winVar))
    # lambda event, b="white": change_bg(event, b)
    winVar['canvas'].bind("<ButtonRelease-1>", lambda event, winVar=winVar: mouseUp(event, winVar))
    root.bind('<Configure>', lambda event, root=root, winVar=winVar: on_move_or_resize(event, root, winVar))

    winVar['color'] = "blue"
    # TODO check directories tmp and lessons. If no - create them

    print(root.wm_geometry())

    root.mainloop()


if __name__ == '__main__':
    main()
