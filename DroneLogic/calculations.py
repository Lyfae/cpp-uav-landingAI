import math

def distance(x2,x1,y2,y1):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

def arcCos(d1,d2):
    pi = math.pi
    a = d1/d2
    theta =math.acos(a)
    return theta *180 / pi
