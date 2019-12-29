from tkinter import *
from tkinter import colorchooser, LAST

from PIL import ImageTk

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

grList=[]
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
brushStyle = ""
lineArrow = ''
lineDot = ''
gridColor = "#D0D0D0"
canvas_width  = 0
canvas_height = 0

xc = 0
yc = 0


def f_quit(event):
    if event.keysym == 'Escape':
        quit()


def mouseDown(event):
    global flag
    flag = 1


def mouseMove(event):
    global flag, count, xStart, yStart, eraser, tool, errSize, color, canvas, xc, yc, line0, \
        xLineStart, yLineStart, cLine0, penWidth, penColor
    if xStart == 0 and yStart == 0 and tool != 3 and tool != 4:
        xStart = event.x
        yStart = event.y

    # penSize(1)
    if tool == 2:
        pass
        # moveObjectTo(eraser, event.x, event.y)
    if tool == 1:
        pass
        # moveObjectTo(pen, event.x, event.y)
    if flag == 1 and tool == 1:
        penMove(penColor, xStart, yStart, penWidth, canvas, figures, event.x, event.y)

    if flag == 1 and tool == 2:
        erMove(errSize, canvas, figures, event.x, event.y)
    if flag == 1 and tool == 7:
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
    #     TODO доробить збільшення полотна при витягуванні вліво та вгору

    if flag == 1 and tool == 3:
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
            cLine0 = {}
            cLine0['x1'] = xLineStart
            cLine0['y1'] = yLineStart
            cLine0['x2'] = event.x
            cLine0['y2'] = event.y

    if flag == 1 and tool == 4:
        if xStart == 0 and yStart == 0:
            xLineStart = event.x
            yLineStart = event.y
            line0 = canvas.create_polygon([xLineStart, yLineStart], [xLineStart, yLineStart], [xLineStart, yLineStart],
                                          [xLineStart, yLineStart],
                                          width=penWidth, outline=penColor, fill=brushStyle)
            cLine0 = {}
        else:
            canvas.coords(line0, xLineStart, yLineStart, xLineStart, event.y, event.x, event.y, event.x, yLineStart)
            cLine0 = {}
            cLine0['x1'] = xLineStart
            cLine0['y1'] = yLineStart
            cLine0['x2'] = event.x
            cLine0['y2'] = event.y
            cLine0['width'] = penWidth
            cLine0['outline'] = penColor
            cLine0['fill'] = brushStyle

    xStart = event.x
    yStart = event.y


def mouseUp(event):
    global xStart, yStart, cLine0, line0, xLineStart, yLineStart
    xStart = 0
    yStart = 0
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
    xLineStart = 0
    yLineStart = 0


def create_canvas(frame):
    canvases.append(Canvas(frame))

def expanse(d):
    global canvas, canvas_width, canvas_height,xc,yc
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
    global canvas, color, canvas_width, canvas_height
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight() - 75
    root.geometry('' + str(screen_width) + 'x' + str(screen_height) + '+-7+0')
    root.title("WhiteBoard")
    frame = Frame(root, relief=RAISED, borderwidth=1)
    frame.pack(fill=BOTH, expand=True)
    canvas = Canvas(frame, bg="#E9FBCA")
    canvas_width  = screen_width + 50
    canvas_height = screen_height + 50
    canvas.place(x=xc, y=yc)
    canvas.config(width=canvas_width, height=canvas_height)
    canvas.config(cursor="tcross")
    grid(canvas, gridColor, screen_width + 50, screen_height + 50, 50, grList)
    btnDown = Button(text='V', width=4, height=1, command=lambda: expanse('u'))
    btnDown.place(x=screen_width // 2, y=screen_height - 60)
    btnRight = Button(text='>', width=2, height=2, command=lambda: expanse('r'))
    btnRight.place(x=screen_width - 25, y=screen_height //2)
    frame1 = Frame(frame, relief=RAISED, borderwidth=1)
    frame1.pack(side=BOTTOM, fill=BOTH)
    images_path = (
    "img/pen.png", "img/err.gif", "img/hand.png", "img/line.png", "img/ClearFill.png", "img/_ClearFill.png",
    "img/palitra.png", "img/width.png", "img/line 2px.png", "img/line 4px.png", "img/line 8px.png",
    "img/line 12px.png", "img/line 16px.png", "img/line 20px.png", "img/line 24px.png", "img/arr.png",
    "img/line 2px.png", "img/lineArr.png", "img/bothArr.png", "img/dot.png", "img/line 2px.png",
    "img/punktir.png", "img/shtrLine.png")
    images = []
    for i in images_path:
        images.append(ImageTk.PhotoImage(file=i))


    def btnHandClick():
        print('Hand')
        global tool
        tool = 7
        noSelectAll(frame1)
        btnHand.config(bg=btnActiveColor)

    def btnLineClick():
        print('Line')
        global tool
        tool = 3
        noSelectAll(frame1)
        btnLine.config(bg=btnActiveColor)

    def btnErClick():
        print('Erazer')
        global tool
        tool = 2
        noSelectAll(frame1)
        btnEr.config(bg=btnActiveColor)

    def btnRectClick():
        print('Rect')
        global tool
        global tool, brushStyle
        if tool == 4:
            if brushStyle == penColor:
                brushStyle = ""
                btnRect.config(image=images[5])
            else:
                brushStyle = penColor
                btnRect.config(image=images[4])
        print('Pen')
        tool = 4
        noSelectAll(frame1)
        btnRect.config(bg=btnActiveColor)

    def btnPenClick():
        global tool
        tool = 1
        noSelectAll(frame1)
        btnPen.config(bg=btnActiveColor)

    def btnColorSelectClick():
        print("Вибір кольору")
        global penColor
        penColor = colorchooser.askcolor()[1]

    def widthClick(d):
        global penWidth
        penWidth = d
        frameWidth.pack_forget()

    def arrowClick(d):
        global lineArrow
        lineArrow = d
        frameArrow.pack_forget()

    def dotClick(d):
        global lineDot
        lineDot = d
        frameDot.pack_forget()

    def btnWidthSelectClick():
        print("Вибір товщини")
        global penWidth
        frameWidth.pack(side=LEFT, padx=2, pady=2)

    def btnArrowSelectClick():
        print("Вибір стрілок")
        frameArrow.pack(side=LEFT, padx=2, pady=2)

    def btnDotSelectClick():
        print("Вибір штриховки")
        frameDot.pack(side=LEFT, padx=2, pady=2)

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
    btnColorSelect = Button(frame1, image=images[6], command=btnColorSelectClick, font="10")
    btnColorSelect.pack(side=LEFT, padx=2, pady=2)
    btnWidthSelect = Button(frame1, image=images[7], command=btnWidthSelectClick, font="10")
    btnWidthSelect.pack(side=LEFT, padx=2, pady=2)
    btnArrowSelect = Button(frame1, image=images[15], command=btnArrowSelectClick, font="10")
    btnArrowSelect.pack(side=LEFT, padx=2, pady=2)
    btnDotSelect = Button(frame1, image=images[19], command=btnDotSelectClick, font="10")
    btnDotSelect.pack(side=LEFT, padx=2, pady=2)
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
    root.bind("<Key>", f_quit)
    canvas.bind("<Button-1>", mouseDown(root))
    canvas.bind("<B1-Motion>", mouseMove)
    canvas.bind("<ButtonRelease-1>", mouseUp)
    color = "blue"
    print(root.wm_geometry())

    root.mainloop()


if __name__ == '__main__':
    main()
