import math

from draw import grid, coords, border_polyline, erMove, penMove, deleteObject, moveObjectBy, draw_line, draw_rectangle, resize_object, move_object

from tkinter import colorchooser, LAST, Tk, Frame, BOTH, RAISED, Canvas, Button, BOTTOM, IntVar, Checkbutton, ALL, \
    NORMAL, NW, LEFT
from datetime import datetime
from pyautogui import Point
from PIL import ImageTk, Image
import pickle

from sys import platform



class App:
    def expanse(self, d):
        # global canvas, canvas_width, canvas_height, xc, yc
        if d == 'u':
            self.canvas_height += 100
            self.yc -= 100
        else:
            self.canvas_width += 100
            self.xc -= 100
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)
        self.canvas.place(x=self.xc, y=self.yc)

    def __init__(self, master):

        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        # TODO -200, -75 remove
        master.geometry('' + str(self.screen_width - 200) + 'x' + str(self.screen_height - 75) + '+200+0')

        master.title("WhiteBoard")
        self.frame = Frame(root, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=True)

        self.selFigIndex = -1
        self.f0 = []
        self.poly = []
        self.flag = 0
        self.tool = 1
        self.fonColor = "#E9FBCA"
        self.brushColor = ""
        self.btnActiveColor = "#331177"
        self.canvas = Canvas(self.frame, bg=self.fonColor)
        self.window_height = master.winfo_height()
        self.window_width = master.winfo_width()
        self.down_x = 0
        self.down_y = 0

        self.xc = 0
        self.yc = 0
        self.canvas_height = self.screen_height + 50
        self.canvas_width = self.screen_width + 50
        self.canvas.config(cursor="tcross")
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)
        self.canvas.place(x=self.xc, y=self.yc)
        # self.canvases = []
        # self.Line0 = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0}
        #
        # self.Figures = []
        # self.errSize = 10
        # self.figures = []
        #
        # self.gridColor = "#D0D0D0"
        # self.grList = []
        # self.down_x = 0
        # self.down_y = 0
        #
        # self.lineArrow = ""
        # self.lineDot = ''
        # self.penColor = "#0000FF"
        # self.penColorOld = "#0000FF"
        # self.penWidth = 2
        # self.penWidthOld = 2
        # self.selFig = {}
        # self.step = 50
        # self.tool = 1
        #
        # self.xLineStart = 0
        # self.xStart = 0
        #
        # self.yLineStart = 0
        # self.yStart = 0
        # self.images = []
        #
        # grid(self)
        # # Buttons expanding canvas
        # self.btnDown = Button(text='V', width=4, height=2, command=lambda d='u': self.expanse(d))
        # self.btnRight = Button(text='>', width=4, height=2, command=lambda d='r': self.expanse(d))
        #
        # self.btnDown.place(x=self.screen_width // 2, y=self.screen_height - 80)
        # # self.btnRight.place(x=self.screen_width - 95, y=self.screen_height // 2)
        # self.btnRight.place(anchor='e')
        # self.frame1 = Frame(self.frame, relief=RAISED, borderwidth=1)
        # self.frame1.pack(side=BOTTOM, fill=BOTH)
        # self.images_btn = {
        #     0: ImageTk.PhotoImage(file="img/pen.png"), 1: ImageTk.PhotoImage(file="img/err.png"),
        #     2: ImageTk.PhotoImage(file="img/hand.png"), 3: ImageTk.PhotoImage(file="img/line.png"),
        #     4: ImageTk.PhotoImage(file="img/ClearFill.png"),
        #     5: ImageTk.PhotoImage(file="img/_ClearFill.png"), 6: ImageTk.PhotoImage(file="img/palitra.png"),
        #     7: ImageTk.PhotoImage(file="img/width.png"), 8: ImageTk.PhotoImage(file="img/line 2px.png"),
        #     9: ImageTk.PhotoImage(file="img/line 4px.png"), 10: ImageTk.PhotoImage(file="img/line 8px.png"),
        #     11: ImageTk.PhotoImage(file="img/line 12px.png"), 12: ImageTk.PhotoImage(file="img/line 16px.png"),
        #     13: ImageTk.PhotoImage(file="img/line 20px.png"), 14: ImageTk.PhotoImage(file="img/line 24px.png"),
        #     15: ImageTk.PhotoImage(file="img/arr.png"), 16: ImageTk.PhotoImage(file="img/line 2px.png"),
        #     17: ImageTk.PhotoImage(file="img/lineArr.png"), 18: ImageTk.PhotoImage(file="img/bothArr.png"),
        #     19: ImageTk.PhotoImage(file="img/dot.png"), 20: ImageTk.PhotoImage(file="img/line 2px.png"),
        #     21: ImageTk.PhotoImage(file="img/punktir.png"), 22: ImageTk.PhotoImage(file="img/shtrLine.png"),
        #     23: ImageTk.PhotoImage(file="img/options.png"), 24: ImageTk.PhotoImage(file="img/open.png"),
        #     25: ImageTk.PhotoImage(file="img/save.png"), 26: ImageTk.PhotoImage(file="img/shot.png"),
        #     27: ImageTk.PhotoImage(file="img/add.png"), 28: ImageTk.PhotoImage(file="img/ar.png"),
        #     29: ImageTk.PhotoImage(file="img/errFon.png"), }
        # # Buttons for main panel
        # self.btnAr = Button(self.frame1, image=self.images_btn[28], command=self.btnArClick, font="10")
        # self.btnAr.pack(side=LEFT, padx=2, pady=2)
        # self.btnPen = Button(self.frame1, image=self.images_btn[0], command=self.btnPenClick, font="10")
        # self.btnPen.pack(side=LEFT, padx=2, pady=2)
        # self.btnEr = Button(self.frame1, image=self.images_btn[1], command=self.btnErClick, font="10")
        # self.btnEr.pack(side=LEFT, padx=2, pady=2)
        # self.btnErFon = Button(self.frame1, image=self.images_btn[29], command=self.btnErFonClick, font="10")
        # self.btnErFon.pack(side=LEFT, padx=2, pady=2)
        #
        # self.btnHand = Button(self.frame1, image=self.images_btn[2], command=self.btnHandClick, font="10")
        # self.btnHand.pack(side=LEFT, padx=2, pady=2)
        # self.btnLine = Button(self.frame1, image=self.images_btn[3], command=self.btnLineClick, font="10")
        # self.btnLine.pack(side=LEFT, padx=2, pady=2)
        # self.btnRect = Button(self.frame1, image=self.images_btn[5], command=self.btnRectClick, font="10")
        # self.btnRect.pack(side=LEFT, padx=2, pady=2)
        # self.btnOptions = Button(self.frame1, image=self.images_btn[23], command=self.btnOptionsClick, font="10")
        # self.btnOptions.pack(side=LEFT, padx=2, pady=2)
        # self.btnScr = Button(self.frame1, image=self.images_btn[26], command=lambda root=master: self.btnScrClick(root))
        # self.btnScr.pack(side=LEFT, padx=2, pady=2)
        # self.btnAddPage = Button(self.frame1, image=self.images_btn[27], command=lambda: self.btnAddPageClick(root),
        #                          font="10")
        # self.btnAddPage.pack(side=LEFT, padx=2, pady=2)
        #
        # # Buttons for main panel switching another panels
        # self.btnColorSelect = Button(self.frame1, image=self.images_btn[6], command=self.btnColorSelectClick, font="10")
        # self.btnColorSelect.pack(side=LEFT, padx=2, pady=2)
        # self.btnWidthSelect = Button(self.frame1, image=self.images_btn[7], command=self.btnWidthSelectClick, font="10")
        # self.btnWidthSelect.pack(side=LEFT, padx=2, pady=2)
        # self.btnArrowSelect = Button(self.frame1, image=self.images_btn[15], command=self.btnArrowSelectClick,
        #                              font="10")
        # self.btnArrowSelect.pack(side=LEFT, padx=2, pady=2)
        # self.btnDotSelect = Button(self.frame1, image=self.images_btn[19], command=self.btnDotSelectClick, font="10")
        # self.btnDotSelect.pack(side=LEFT, padx=2, pady=2)
        #
        # self.btnSave = Button(self.frame1, image=self.images_btn[25], command=self.save, font="10")
        # self.btnSave.pack(side=LEFT, padx=2, pady=2)
        # self.btnLoad = Button(self.frame1, image=self.images_btn[24], command=self.load,
        #                       font="10")
        # self.btnLoad.pack(side=LEFT, padx=2, pady=2)
        #
        # # Panel select width arrow
        # self.frameWidth = Frame(self.frame1)
        # self.frameWidth.pack_forget()
        # self.btnWidth2 = Button(self.frameWidth, image=self.images_btn[8], command=lambda: self.widthClick(2),
        #                         font="10")
        # self.btnWidth2.pack(side=LEFT, padx=2, pady=2)
        # self.btnWidth4 = Button(self.frameWidth, image=self.images_btn[9], command=lambda: self.widthClick(4),
        #                         font="10")
        # self.btnWidth4.pack(side=LEFT, padx=2, pady=2)
        # self.btnWidth8 = Button(self.frameWidth, image=self.images_btn[10], command=lambda: self.widthClick(6),
        #                         font="10")
        # self.btnWidth8.pack(side=LEFT, padx=2, pady=2)
        # self.btnWidth12 = Button(self.frameWidth, image=self.images_btn[11], command=lambda: self.widthClick(8),
        #                          font="10")
        # self.btnWidth12.pack(side=LEFT, padx=2, pady=2)
        # self.btnWidth16 = Button(self.frameWidth, image=self.images_btn[12], command=lambda: self.widthClick(10),
        #                          font="12")
        # self.btnWidth16.pack(side=LEFT, padx=2, pady=2)
        # self.btnWidth20 = Button(self.frameWidth, image=self.images_btn[13], command=lambda: self.widthClick(12),
        #                          font="14")
        # self.btnWidth20.pack(side=LEFT, padx=2, pady=2)
        # self.btnWidth24 = Button(self.frameWidth, image=self.images_btn[14], command=lambda: self.widthClick(16),
        #                          font="16")
        # self.btnWidth24.pack(side=LEFT, padx=2, pady=2)
        # self.frameArrow = Frame(self.frame1)
        # self.frameArrow.pack_forget()
        # self.btnArrow1 = Button(self.frameArrow, image=self.images_btn[16],
        #                         command=lambda d='': self.arrowClick(d),
        #                         font="10")
        # self.btnArrow1.pack(side=LEFT, padx=2, pady=2)
        # self.btnArrow2 = Button(self.frameArrow, image=self.images_btn[17],
        #                         command=lambda d=LAST, self=self: self.arrowClick(d),
        #                         font="10")
        # self.btnArrow2.pack(side=LEFT, padx=2, pady=2)
        # self.btnArrow3 = Button(self.frameArrow, image=self.images_btn[18],
        #                         command=lambda d=BOTH, self=self: self.arrowClick(d),
        #                         font="10")
        # self.btnArrow3.pack(side=LEFT, padx=2, pady=2)
        # self.frameDot = Frame(self.frame1)
        # self.frameDot.pack_forget()
        # self.btnArrow1 = Button(self.frameDot, image=self.images_btn[20], command=lambda d='': self.dotClick(d),
        #                         font="10")
        # self.btnArrow1.pack(side=LEFT, padx=2, pady=2)
        # self.btnArrow2 = Button(self.frameDot, image=self.images_btn[21],
        #                         command=lambda d=(5, 5): self.dotClick(d),
        #                         font="10")
        # self.btnArrow2.pack(side=LEFT, padx=2, pady=2)
        # self.btnArrow3 = Button(self.frameDot, image=self.images_btn[22],
        #                         command=lambda d=(10, 2): self.dotClick(d),
        #                         font="10")
        # self.btnArrow3.pack(side=LEFT, padx=2, pady=2)
        #
        # # ================= Options =======================
        # self.gr = IntVar()
        # self.gr.set(1)
        # self.full_screen = IntVar()
        # self.full_screen.set(0)
        #
        # self.frameOptions = Frame(self.frame1)
        # self.frameOptions.pack_forget()
        # self.chbGrid = Checkbutton(self.frameOptions, text='grid', variable=self.gr, command=self.grid_hide)
        # self.chbGrid.pack(side=LEFT, padx=2, pady=2)
        # self.chbFullScreen = Checkbutton(self.frameOptions, text='full', variable=self.full_screen,
        #                                  command=lambda master=master: self.full_screenClick(master))
        # self.chbFullScreen.pack(side=LEFT, padx=2, pady=2)
        # # ================= End Options =======================

        master.bind("<Key>", self.key_press)
        self.canvas.bind("<Button-1>", self.mouseDown)
        self.canvas.bind("<B1-Motion>", self.mouseMove)
        # self.canvas.bind("<Motion>",  self.mouseMoveNoButton)
        self.canvas.bind("<ButtonRelease-1>",  self.mouseUp)
        master.bind('<Configure>', lambda event, root=master: self.on_move_or_resize(event, root))
        #
        # # self.color = "blue"
        # # TODO check directories tmp and lessons. If no - create them
        #
        # # ================= start settings =====================
        # self.btnPen.config(bg=self.btnActiveColor)
        # self.makeSelFig(10000, 10000, 10001, 10001, None)
        # self.full_screenClick(master)
        # self.grid_hide()

        # ======================================================

    def grid_hide(self):
        if self.gr.get() == 1:
            grid(self)
        else:
            for l in self.grList:
                deleteObject(self.canvas, l)
        self.frameOptions.pack_forget()

    def full_screenClick(self, master):
        # print(self.full_screen.get())
        if self.full_screen.get() == 1:
            master.wm_attributes("-fullscreen", "true")
        else:
            master.wm_attributes("-fullscreen", "false")
        self.frameOptions.pack_forget()

    def makeSelFig(self, x1, y1, x2, y2, Obj):
        self.selFig['0'] = self.canvas.create_rectangle(x1 - 1, y1 - 1, x2 + 1, y2 + 1, width=1,
                                                        outline="red",
                                                        dash=(5, 5))

        self.selFig['D'] = self.canvas.create_rectangle(x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,
                                                        abs(y1 + y2) // 2 + 10, width=1,
                                                        outline="red", fill="red")
        self.selFig['Obj'] = Obj

    def on_move_or_resize(self, event, master):
        # If windows is resizing
        w = master.winfo_width()
        h = master.winfo_height()
        self.window_width, self.window_height = w, h
        self.btnDown.place(x=w // 2, y=h - 85)
        self.btnRight.place(x=w - 20, y=h // 2)

    def btnHandClick(self):
        # print('Hand')
        self.tool = 7
        self.noSelectAll()
        self.btnHand.config(bg=self.btnActiveColor)
        self.deleteSelectionLinks()

    def btnAddPageClick(self, root):
        # print('Add Page')
        self.deleteSelectionLinks()

    def btnLineClick(self):
        # print('Line')
        self.penWidth = self.penWidthOld
        self.penColor = self.penColorOld
        self.tool = 3
        self.noSelectAll()
        self.btnLine.config(bg=self.btnActiveColor)
        self.deleteSelectionLinks()

    def btnErClick(self):
        # print('Erazer')
        self.tool = 2
        self.noSelectAll()
        self.btnEr.config(bg=self.btnActiveColor)
        self.deleteSelectionLinks()

    def btnErFonClick(self):
        # print("draw background color")

        self.tool = 1
        self.penWidthOld = self.penWidth
        self.penColorOld = self.penColor
        self.penWidth = self.errSize
        self.penColor = self.fonColor

        self.noSelectAll()
        self.btnErFon.config(bg=self.btnActiveColor)
        self.deleteSelectionLinks()

    def btnRectClick(self):
        # print('Rect')
        self.penWidth = self.penWidthOld
        self.penColor = self.penColorOld
        if self.tool == 4:
            if self.brushColor == self.penColor:
                self.brushColor = ""
                self.btnRect.config(image=self.images_btn[5])
            else:
                self.brushColor = self.penColor
                self.btnRect.config(image=self.images_btn[4])
        self.tool = 4
        self.noSelectAll()
        self.btnRect.config(bg=self.btnActiveColor)
        self.deleteSelectionLinks()

        # selFig = {}

    def noSelectAll(self):
        for associated_widget in self.frame1.winfo_children():
            associated_widget.configure(bg='white')

    def deleteSelectionLinks(self):
        deleteObject(self.canvas, self.selFig['0'])
        deleteObject(self.canvas, self.selFig['D'])

    def btnPenClick(self):
        self.tool = 1
        self.penWidth = self.penWidthOld
        self.penColor = self.penColorOld
        self.noSelectAll()
        self.btnPen.config(bg=self.btnActiveColor)
        self.deleteSelectionLinks()
        self.makeSelFig(10000, 10000, 10001, 10001, None)

    def btnArClick(self):
        self.tool = 8
        self.noSelectAll()
        self.btnAr.config(bg=self.btnActiveColor)
        self.deleteSelectionLinks()
        self.makeSelFig(10000, 10000, 10001, 10001, None)

    def btnColorSelectClick(self):
        # print("Select color")
        self.penColor = colorchooser.askcolor()[1]
        self.penColorOld = colorchooser.askcolor()[1]
        self.deleteSelectionLinks()

    def widthClick(self, d):
        self.penWidth = d
        self.frameWidth.pack_forget()
        self.deleteSelectionLinks()

    def arrowClick(self, d):
        self.lineArrow = d
        self.frameArrow.pack_forget()
        self.deleteSelectionLinks()

    def dotClick(self, d):
        self.lineDot = d
        self.frameDot.pack_forget()
        self.deleteSelectionLinks()

    def btnWidthSelectClick(self):
        # print("Select width")
        self.frameWidth.pack(side=LEFT, padx=2, pady=2)
        self.deleteSelectionLinks()

    def btnOptionsClick(self):
        # print("Settings")
        self.frameOptions.pack(side=LEFT, padx=2, pady=2)
        self.deleteSelectionLinks()

    def btnArrowSelectClick(self):
        # print("Select arrow")
        self.frameArrow.pack(side=LEFT, padx=2, pady=2)
        self.deleteSelectionLinks()

    def btnDotSelectClick(self):
        # print("Select dash")
        self.frameDot.pack(side=LEFT, padx=2, pady=2)
        self.deleteSelectionLinks()

    def key_press(self, event):
        if event.keysym == 'Escape':
            quit()
        elif event.keysym == 'Home':
            self.xc = 0
            self.yc = 0
            self.canvas.place(x=self.xc, y=self.yc)
        elif event.keysym == 'Down':  # moving canvas up
            self.yc -= 50

            if -self.yc + self.window_height > self.canvas_height:
                self.yc = -self.canvas_height + self.window_height
            self.canvas.place(x=self.xc, y=self.yc)

        elif event.keysym == 'Up':  # moving canvas down
            self.yc += 50
            if self.yc > 0:
                self.yc = 0
            self.canvas.place(x=self.xc, y=self.yc)
        elif event.keysym == 'Left':
            self.xc += 50
            if self.xc > 0:
                self.xc = 0
            self.canvas.place(x=self.xc, y=self.yc)
        elif event.keysym == 'Right':
            self.xc -= 50

            if -self.xc + self.window_width > self.canvas_width:
                self.xc = -self.canvas_width + self.window_width
            self.canvas.place(x=self.xc, y=self.yc)
        else:
            pass
            # print(event.keysym)

    def mouseDown(self, event):
        print("Down")
        print(event.x)
        if self.tool == 1:
            self.poly = []
            self.f0 = []
            self.f0.append([])
            self.down_x = event.x
            self.down_y = event.y
            self.poly.append(Point(event.x, event.y))
            # self.f0.append(self.canvas.create_line(self.down_x,self.down_y,event.x, event.y, fill="blue", width=2))
            # self.poly.append(Point(event.x,event.y))
            # self.f0 = self.canvas.create_line(event.x, event.y, event.x, event.y, fill="blue", width=2)

            # elif self.tool == 8:  # select object
        #     for fig in reversed(self.figures):
        #         # print(fig)
        #         if fig[1] != 'polyline':
        #             x1, y1, x2, y2 = coords(self.canvas, fig[0])
        #         else:
        #             x1, y1, x2, y2 = border_polyline(fig[2])
        #         if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
        #             self.canvas.config(cursor="fleur")
        #             if self.selFig != {}:
        #                 self.canvas.coords(self.selFig['0'], x1 - 1, y1 - 1, x2 + 1, y2 + 1)
        #                 self.canvas.coords(self.selFig['D'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,
        #                                    abs(y1 + y2) // 2 + 10)
        #
        #
        #                 self.selFig['Obj'] = fig
        #             fl = True
        #             break
        #         else:
        #             self.canvas.config(cursor="tcross")
        #
        #     self.f0 = []
        # # repeat code
        # fl = False
        # # change cursor


    def mouseMove(self, event):
        # print(event.x)
        if self.tool == 1:
            self.poly.append(Point(event.x, event.y))
            self.f0.append(self.canvas.create_line(self.down_x,self.down_y,event.x, event.y, fill="blue", width=2))

        # if self.xStart == 0 and self.yStart == 0 and self.tool != 3 and self.tool != 4:
        #     self.xStart = event.x
        #     self.yStart = event.y
        # if self.tool == 1:
        #     penMove(self, event.x, event.y)
        # elif self.tool == 2:
        #     erMove(self, event.x, event.y)
        # elif self.tool == 7:
        #     dx = event.x - self.xStart
        #     dy = event.y - self.yStart
        #     self.xc += dx
        #     if self.xc > 0:
        #         self.xc -= dx
        #     self.yc += dy
        #     if self.yc > 0:
        #         self.yc -= dy
        #     self.canvas.place(x=self.xc, y=self.yc)
        # elif self.tool == 3:
        #     draw_line(self, event)
        # elif self.tool == 4:
        #     draw_rectangle(self, event)
        # elif self.tool == 8:
        #     f = False
        #     if self.flag == 0 or self.flag == 2:
        #         f = resize_object(self, event)
        #     if not f and (self.flag == 0 or self.flag == 1 or self.flag == 3):
        #         if self.selFig['Obj'] != None:
        #             if self.selFig['Obj'][1] == 'polyline':
        #                 x1, y1, x2, y2 = coords(self.canvas, self.selFig['Obj'][0])
        #                 if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
        #                     f = move_object(self, event)
        #             else:
        #                 x1, y1, x2, y2 = coords(self.canvas, self.selFig['Obj'][0])
        #                 if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
        #                     f = move_object(self,event)
        self.down_x = event.x
        self.down_y = event.y

    def mouseMoveNoButton(self, event):
        return
        if self.tool == 8:
            # change cursor
            try:

                if not self.selFig['Obj'] is None:
                    x1, y1, x2, y2 = coords(self.canvas, self.selFig['0'])
                    xo1, yo1, xo2, yo2 = coords(self.canvas, self.selFig['Obj'][0])
                    if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
                        if math.sqrt((event.x - xo2) ** 2 + (event.y - yo2) ** 2) < 50 or self.flag == 1:
                            self.canvas.config(cursor='bottom_right_corner')
                        else:
                            self.canvas.config(cursor="fleur")
                    else:
                        self.canvas.config(cursor="tcross")


            except:
                pass
        else:
            self.canvas.config(cursor="tcross")

    def mouseUp(self, event):
        print("Up")
        fl = False
        if self.tool == 1:
            self.xStart = 0
            self.yStart = 0
            for l in self.f0:
                deleteObject(self.canvas, l)
            self.f0.clear()

            self.f0.append(self.canvas.create_line(self.poly, fill="blue", width=2))


        #     if self.down_x == event.x and self.down_y == event.y:
        #         k = []
        #         r = self.penWidth
        #         k.append(
        #             self.canvas.create_oval(event.x - r // 4, event.y - r // 4,
        #                                     event.x + r // 4, event.y + r // 4,
        #                                     fill=self.penColor,
        #                                     width=self.penWidth, outline=self.penColor)
        #         )
        #         k.append("oval")
        #         k.append(self.poly)
        #         c = {}
        #         c['fill'] = self.penColor
        #         c['width'] = self.penWidth
        #         c['outline'] = self.penColor
        #         k.append(c)
        #         self.figures.append(k)
        #     else:
        #         k = []
        #         k.append(self.f0)
        #         k.append("polyline")
        #         k.append(self.poly)
        #         c = {}
        #         c['fill'] = self.penColor
        #         c['width'] = self.penWidth
        #         c['outline'] = self.penColor
        #         k.append(c)
        #         self.figures.append(k)
        # elif self.tool == 3 or self.tool == 4:
        #     k = []
        #     k.append(self.line0)
        #     if self.tool == 3:
        #         k.append("line")
        #     else:
        #         k.append("rectangle")
        #     k.append(self.cLine0)
        #     self.figures.append(k)
        #
        # if coords(self.canvas, self.selFig['D']) != None:  # remove figure
        #     x1, y1, x2, y2 = coords(self.canvas, self.selFig['D'])
        #     if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
        #         self.canvas.delete(self.selFig['Obj'][0])
        #
        #         self.canvas.coords(self.selFig['0'], 10000, 10000, 10001, 10001)
        #         self.canvas.coords(self.selFig['D'], 10000, 10000, 10001, 10001)
        #         self.figures.remove(self.selFig['Obj'])
        #         # self.selFig = {}
        #
        # if self.tool == 8 and self.flag == 2 and self.selFig['Obj'][1] == 'image':
        #     # print("resizing")
        #     x, y, xo2, yo2 = coords(self.canvas, self.selFig['0'])
        #     width = xo2 - x
        #     height = yo2 - y
        #     name = self.selFig['Obj'][2]['name']
        #     deleteObject(self.canvas, self.selFig['Obj'][0])
        #     image = Image.open(name)
        #     image = image.resize((width, height), Image.ANTIALIAS)
        #     self.images.append(ImageTk.PhotoImage(image))
        #     self.selFig['Obj'][0] = self.canvas.create_image(x, y, image=self.images[-1], state=NORMAL, anchor=NW)
        #     self.selFig['Obj'][2]['width'] = width
        #     self.selFig['Obj'][2]['height'] = height
        #
        # self.xLineStart = 0
        # self.yLineStart = 0
        # self.flag = 0

    def btnScrInsertInCanvasClick(self, root, floatWindow):
        # print('btnClick')
        floatWindow.wm_attributes("-alpha", "0.0")
        width = 600
        self.window_width = root.winfo_width()
        self.window_height = root.winfo_height()
        x0 = -self.xc + self.window_width - width - 40
        y0 = -self.yc + 20
        name = 'tmp/' + datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S") + '.png'
        image = (pyautogui.screenshot(region=(0, 0, self.screen_width, self.screen_height)))
        image.save(name)

        k = self.screen_width / (self.screen_height + 75)
        height = int(width / k)
        image = image.resize((width, height), Image.ANTIALIAS)
        root.wm_state('normal')
        self.images.append(ImageTk.PhotoImage(image))
        k = []
        c = {}
        c['name'] = name
        c['x'] = x0
        c['y'] = y0
        c['width'] = width
        c['height'] = height
        k.append(self.canvas.create_image(x0, y0, image=self.images[-1], state=NORMAL, anchor=NW))
        k.append("image")
        k.append(c)
        self.figures.append(k)

        floatWindow.destroy()

    def btnScrClick(self, root):
        # print('btnScrClick')
        root.wm_state('iconic')
        floatWindow = Tk()
        floatWindow.geometry("40x35+20+20")
        btnScrInsertInCanvas = Button(floatWindow, text='Sr',
                                      command=lambda root=root, floatWindow=floatWindow: self.btnScrInsertInCanvasClick(
                                          root, floatWindow))
        floatWindow.overrideredirect(1)
        floatWindow.wm_attributes("-topmost", True)
        floatWindow.wm_attributes("-alpha", "0.5")
        btnScrInsertInCanvas.pack(fill=BOTH, expand=True)
        self.btnPenClick()

    def grid(self):
        for y in range(0, self.canvas_width * 100, self.step):
            self.grList.append(
                self.canvas.create_line(0, y, self.canvas_width * 100, y, fill=self.gridColor, dash=(2, 8)))
        for x in range(0, self.canvas_height * 100, self.step):
            self.grList.append(
                self.canvas.create_line(x, 0, x, self.canvas_height * 100, fill=self.gridColor, dash=(2, 8)))

    def erMove(self, x, y):
        for fig in self.figures:
            # #print(fig[0])

            xCeOb, yCeOb = center(self.canvas, fig[0])
            if abs(x + self.errSize - xCeOb) < self.errSize and abs(y + self.errSize - yCeOb) < self.errSize:
                if len(self.figures) > 0:
                    deleteObject(self.canvas, fig[0])
                    self.figures.remove(fig)

    def save(self):
        data = {}
        data['figures'] = self.figures
        data['penColor'] = self.penColor
        data['brushColor'] = self.brushColor
        data['penWidth'] = self.penWidth
        data['fonColor'] = self.fonColor
        data['canvas_width'] = self.canvas_width
        data['canvas_height'] = self.canvas_height
        data['xc'] = self.xc
        data['yc'] = self.yc

        with open("test.wb", "wb") as fp:
            pickle.dump(data, fp)

    def load(self):
        self.canvas.delete(ALL)
        self.figures = []
        self.images = []

        self.btnPenClick()
        with open("test.wb", "rb") as fp:  # Unpickling
            data = pickle.load(fp)
        self.figures = data['figures']
        self.penColor = data['penColor']
        self.brushColor = data['brushColor']
        self.penWidth = data['penWidth']
        self.fonColor = data['fonColor']
        self.canvas_width = data['canvas_width']
        self.canvas_height = data['canvas_height']
        self.xc = data['xc']
        self.yc = data['yc']
        # change size and position canvas
        self.canvas.place(x=self.xc, y=self.yc)
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)
        grid(self)
        self.f0 = []

        for fig in self.figures:
            f = fig[2]
            if fig[1] == 'oval':
                fig[0] = self.canvas.create_oval(f['x1'], f['y1'], f['x2'], f['y2'], outline=f['outline'],
                                                 fill=f['fill'], width=f['width'])
            elif fig[1] == 'line':
                fig[0] = self.canvas.create_line(f['x1'], f['y1'], f['x2'], f['y2'],
                                                 arrow=f['arrow'], dash=f['dash'], fill=f['fill'], width=f['width'])


            elif fig[1] == 'rectangle':
                fig[0] = self.canvas.create_polygon(f['x1'], f['y1'], f['x2'], f['y2'], f['x3'], f['y3'], f['x4'],
                                                    f['y4'],
                                                    width=f['width'], fill=f['fill'],
                                                    outline=f['outline'])
            elif fig[1] == 'image':
                width = f['width']
                height = f['height']
                image = Image.open(f['name'])
                image = image.resize((width, height), Image.ANTIALIAS)
                self.images.append(ImageTk.PhotoImage(image))
                fig[0] = self.canvas.create_image(f['x'], f['y'], image=self.images[-1], state=NORMAL, anchor=NW)
            elif fig[1] == 'polyline':
                self.f0 = self.canvas.create_line(fig[2], fill=fig[3]['fill'], width=fig[3]['width'])

if __name__ == '__main__':
    root = Tk()
    root.wm_attributes("-fullscreen", "false")

    app = App(root)

    root.mainloop()
