_viewPort = None


def coords(canvas, obj):
    # return _C.coords(obj)
    return canvas.bbox(obj)


def moveObjectBy(canvas, obj, dx, dy):
  canvas.move(obj, dx, dy)

def transformCoord(x, y):
    global _viewPort
    if _viewPort:
        x1, x2, y1, y2 = _viewPort
        w, h = windowSize()
        x = (x - x1) * w / (x2 - x1)
        y = (y2 - y) * h / (y2 - y1)
    return x, y


def grid(winVar):
    for y in range(0, winVar['canvas_width']*100, winVar['step']):
        winVar['grList'].append(winVar['canvas'].create_line(0, y, winVar['canvas_width']*100, y, fill=winVar['gridColor'], dash=(2,8)))
    for x in range(0, winVar['canvas_height']*100, winVar['step']):
        winVar['grList'].append(winVar['canvas'].create_line(x, 0, x, winVar['canvas_height']*100, fill=winVar['gridColor'], dash=(2,8)))


def center(canvas, obj):
    x1, y1, x2, y2 = coords(canvas, obj)
    return (x1 + x2) / 2, (y1 + y2) / 2


def deleteObject(canvas, obj):
    canvas.delete(obj)


# def erMove(errSize, canvas, figures, x, y):
def erMove(winVar, x, y):
    for fig in winVar['figures']:
        # print(fig[0])

        xCeOb, yCeOb = center(winVar['canvas'], fig[0])
        if abs(x + winVar['errSize'] - xCeOb) < winVar['errSize'] and abs(y + winVar['errSize'] - yCeOb) < winVar['errSize']:
            if len(winVar['figures']) > 0:
                deleteObject(winVar['canvas'], fig[0])
                winVar['figures'].remove(fig)


# def penMove(color, xStart, yStart, r, canvas, figures, x, y):
def penMove(winVar,  x, y):
    r = winVar['penWidth']
    x1 = winVar['xStart']
    y1 = winVar['yStart']
    x2 = x
    y2 = y
    step = 1
    if abs(x2 - x1) > abs(y2 - y1):
        fl = 0
        if winVar['xStart'] < x:
            myRange = range(winVar['xStart'], x, step)
        else:
            myRange = range(x, winVar['xStart'], step)
    else:
        fl = 1
        if winVar['yStart'] < y:
            myRange = range(winVar['yStart'], y, step)
        else:
            myRange = range(y, winVar['yStart'], step)
    for x in myRange:
        if fl == 0:
            xx = x
            yy = int(((x1 * y2 - x2 * y1) + (y1 - y2) * x) / (x1 - x2))
        else:
            yy = x
            xx = int(((x1 * y2 - x2 * y1) + (x2 - x1) * yy) / (y2 - y1))
        if True:
            k = []
            k.append(winVar['canvas'].create_oval(xx - r // 2, yy - r // 2, xx + r // 2, yy + r // 2, outline=winVar['penColor'],
                                        fill=winVar['penColor'], width=1))
            k.append("oval")
            c = {}
            c['x1'] = xx - r // 2
            c['y1'] = yy - r // 2
            c['x2'] = xx + r // 2
            c['y2'] = yy + r // 2
            c['outline'] = winVar['color']
            c['fill'] = winVar['color']
            c['width'] = 1
            k.append(c)
            winVar['figures'].append(k)

