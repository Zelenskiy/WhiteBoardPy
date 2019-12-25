# coding: utf-8
import PIL
from tkinter import Button, Pack

from graph import *
from random import randint
from math import sin, cos, pi
import numpy as np
import pyautogui
from PIL import ImageTk

# import imutils
# import cv2

count = 0
figures = []

score = 0
step = 1
Rmin = 10
Rmax = 20
fieldWidth = 300
fieldHeight = 400
flag = 0
tool = 0
r = 4
errSize = 10
xStart = 0
yStart = 0
eraser = None


def mouseDown(event):
    global flag, tool, count, xStart, yStart

    flag = 1
    penColor(100, 45, 0)
    brushColor(100, 45, 0)
    moveTo(event.x, event.y)
    xStart = event.x
    yStart = event.y


def erMove(x, y):
    global count
    brushColor(0, 150, 0)
    moveObjectTo(eraser, x, y)
    for fig in figures:
        # print(fig[0])
        try:
            xCeOb, yCeOb = center(fig[0])
            if abs(x + errSize - xCeOb) < errSize and abs(y + errSize - yCeOb) < errSize:
                if count > 0:
                    deleteObject(fig[0])
                    figures.remove(fig)
                    count -= 1
        except:
            print(fig[0])


def penMove(x, y):
    global count

    x1 = xStart
    y1 = yStart
    x2 = x
    y2 = y
    step = 1
    if abs(x2 - x1) > abs(y2 - y1):
        fl = 0
        if xStart < x:
            myRange = range(xStart, x, step)
        else:
            myRange = range(x, xStart, step)
    else:
        fl = 1
        if yStart < y:
            myRange = range(yStart, y, step)
        else:
            myRange = range(y, yStart, step)
    for x in myRange:
        # y = int(((x1 * y2 - x2 * y1) + (y1 - y2) * x) / (x1 - x2))
        if fl == 0:
            xx = x
            yy = int(((x1 * y2 - x2 * y1) + (y1 - y2) * x) / (x1 - x2))
        else:
            yy = x
            xx = int(((x1 * y2 - x2 * y1) + (x2 - x1) * yy) / (y2 - y1))
    # if True:
    #     xx = x
    #     yy = y
        if True:
            count += 1
            k = []
            k.append(circle(xx, yy, r))
            k.append(xx)
            k.append(yy)
            figures.append(k)


def mouseMove(event):
    global flag, count, xStart, yStart, eraser
    global tool
    global errSize
    penSize(1)
    if tool == 2:
        moveObjectTo(eraser, event.x, event.y)
    if flag == 1 and tool == 1:
        penMove(event.x, event.y)
    if flag == 1 and tool == 2:
        erMove(event.x, event.y)

    xStart = event.x
    yStart = event.y


def mouseUp(event):
    global flag
    global tool
    flag = 0


def keyPressed(event):
    if event.keycode == VK_ESCAPE:
        close()


def btnPenClick():
    print('Pen')
    global tool
    tool = 1
    moveObjectTo(eraser, -100, -100)


def btnHandClick():
    print('Hand')
    global tool
    tool = 0
    moveObjectTo(eraser, -100, -100)


def btnErrClick():
    global tool, eraser
    tool = 2
    brushColor(249, 255, 79)
    eraser = circle(-100, -100, errSize)


def btnFigClick():
    global tool
    tool = 3


def btnScrClick():
    print('btnScrClick')
    image = pyautogui.screenshot(region=(0, 0, 300, 400))
    image.save("pic.png")


def btnTmpClick():
    global count
    if count > 0:
        deleteObject(figures[count][0])
        del figures[count]
        count -= 1
        # print(figures)


def main(self=None):
    global lbl, eraser

    canvasPos(0, 5)
    canvasSize(fieldWidth, fieldHeight)

    windowSize(fieldWidth + 2, fieldHeight + 27)

    pnl = Pack()
    btnPen = Button(text='Перо', command=btnPenClick)
    btnPen.grid(row=1, column=1)
    btnHand = Button(text='Рука', command=btnHandClick)
    btnHand.grid(row=1, column=2)
    btnErr = Button(text='Гумка', command=btnErrClick)
    btnErr.grid(row=1, column=3)
    btnScr = Button(text='ScrShot', command=btnScrClick)
    btnScr.grid(row=1, column=4)
    btnFig = Button(text='Фіг', command=btnFigClick)
    btnFig.grid(row=1, column=5)
    btnTmp = Button(text="", command=btnTmpClick)
    btnTmp.grid(row=1, column=6)

    brushColor(249, 255, 79)
    eraser = circle(-100, -100, errSize)

    onKey(keyPressed)

    onMouseDown(mouseDown)
    onMouseMove(mouseMove)
    onMouseUp(mouseUp)

    # onTimer(update, 10)
    run()


main()
