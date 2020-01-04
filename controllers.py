from draw import *

def border_polyline(points):
    print(points)
    if points == []:
        return 0,0,0,0
    x_min = points[0].x
    y_min = points[0].y
    x_max = points[0].x
    y_max = points[0].y
    for p in points:
        if p.x > x_max:
            x_max = p.x
        if p.y > y_max:
            y_max = p.y
        if p.x < x_min:
            x_min = p.x
        if p.y < y_min:
            y_min = p.y

    return x_min, y_min, x_max, y_max