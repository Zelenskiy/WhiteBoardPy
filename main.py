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
r = 10
errSize = 10


def mouseDown(event):
    global flag, tool, count

    flag = 1
    penColor(100, 45, 0)
    brushColor(100, 45, 0)
    moveTo(event.x, event.y)
    # circle(event.x, event.y, r)
    # if tool == 3:
    #     flag = 0
    #     global circl
    #     count += 1
    #     k = []
    #     k.append(circle(event.x, event.y, r))
    #     k.append(event.x)
    #     k.append(event.y)
    #     figures[count] = k
    #
    #     print(figures)


def mouseMove(event):
    global flag, count
    global tool
    global errSize
    penSize(1)
    if flag == 1 and tool == 1:
        count += 1
        k = []
        k.append(circle(event.x, event.y,r))
        # k.append(lineTo(event.x, event.y))
        k.append(event.x)
        k.append(event.y)
        figures.append(k)

    if flag == 1 and tool == 2:
        for fig in figures:
            if (abs(event.x - fig[1]) < errSize) and (abs(event.y - fig[2]) < errSize):
                if count > 0:
                    deleteObject(fig[0])
                    figures.remove(fig)
                    count -= 1
                break


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


def btnHandClick():
    print('Hand')
    global tool
    tool = 0


def btnErrClick():
    global tool
    tool = 2


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
    global lbl

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

    onKey(keyPressed)

    onMouseDown(mouseDown)
    onMouseMove(mouseMove)
    onMouseUp(mouseUp)

    # onTimer(update, 10)
    run()


main()
