from tkinter import *
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

r = 2
errSize = 10
figures = []
flag = 0
tool = 0

xStart = 0
yStart = 0
canvas = None
color = None


def f_quit(event):
    print(event.keysym)


def btnPenClick():
    print('Pen')
    global tool, eraser, pen
    tool = 1


def btnErClick():
    print('Erazer')
    global tool, eraser, pen
    tool = 2


def mouseDown(event):
    global flag, tool, count, xStart, yStart
    flag = 1


def mouseMove(event):
    global flag, count, xStart, yStart, eraser, tool, errSize, color
    if xStart == 0 and yStart == 0:
        xStart = event.x
        yStart = event.y
    print('mmmmmmmmmmmm')

    # penSize(1)
    if tool == 2:
        pass
        # moveObjectTo(eraser, event.x, event.y)
    if tool == 1:
        pass
        # moveObjectTo(pen, event.x, event.y)
    if flag == 1 and tool == 1:
        penMove(color, xStart, yStart, r, canvas, figures, event.x, event.y)
        pass
    if flag == 1 and tool == 2:
        erMove(errSize, canvas, figures, event.x, event.y)
        pass
    xStart = event.x
    yStart = event.y


def mouseUp(event):
    global xStart, yStart
    print('uuuuuuuuuu')
    xStart = 0
    yStart = 0


def main():
    global canvas, color
    root = Tk()
    # ex = Example(root)
    root.geometry("400x250+300+300")

    root.title("WhiteBoard")

    frame = Frame(root, relief=RAISED, borderwidth=1)
    frame.pack(fill=BOTH, expand=True)
    frame1 = Frame(frame, relief=RAISED, borderwidth=1)
    frame1.pack(fill=X)

    btnPen = Button(frame1, text='Перо', command=btnPenClick, font="10")
    btnPen.pack(side=LEFT)
    btnEr = Button(frame1, text='Гумка', command=btnErClick, font="10")
    btnEr.pack(side=LEFT)

    canvas = Canvas(frame)
    canvas.pack(fill=BOTH, expand=1)

    canvas.bind("<Key>", f_quit)
    canvas.bind("<Button-1>", mouseDown(root))
    canvas.bind("<B1-Motion>", mouseMove)
    canvas.bind("<ButtonRelease-1>", mouseUp)

    color = "blue"

    root.mainloop()


if __name__ == '__main__':
    main()
