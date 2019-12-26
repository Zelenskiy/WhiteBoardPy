def coords(canvas, obj):
    #return _C.coords(obj)
    return canvas.bbox(obj)

def center(canvas, obj):
    x1, y1, x2, y2 = coords(canvas, obj)
    return (x1+x2)/2, (y1+y2)/2

def deleteObject(canvas, obj):
    canvas.delete(obj)

def erMove(errSize, canvas, figures, x, y):

    for fig in figures:
        # print(fig[0])

        xCeOb, yCeOb = center(canvas, fig[0])
        if abs(x + errSize - xCeOb) < errSize and abs(y + errSize - yCeOb) < errSize:
            if len(figures) > 0:
                deleteObject(canvas, fig[0])
                figures.remove(fig)

def penMove(color, xStart, yStart, r, canvas, figures, x, y):

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
        if fl == 0:
            xx = x
            yy = int(((x1 * y2 - x2 * y1) + (y1 - y2) * x) / (x1 - x2))
        else:
            yy = x
            xx = int(((x1 * y2 - x2 * y1) + (x2 - x1) * yy) / (y2 - y1))
        if True:
            k = []
            k.append(canvas.create_oval(xx - r, yy - r, xx + r, yy + r,outline=color,
            fill=color, width=1))
            k.append(xx)
            k.append(yy)
            figures.append(k)