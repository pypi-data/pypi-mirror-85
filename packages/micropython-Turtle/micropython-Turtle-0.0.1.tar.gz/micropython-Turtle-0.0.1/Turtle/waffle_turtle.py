import math
import screen
from Turtle import init_turtle as iturtle
from Turtle import globalvar as gl

def errorthrow(a,b):
    if a < 0 or b < 0 or a > 128 or b > 160:
        print("Turtle beyond the screen.")
        raise ValueError("x must be below 128,y must be below 160")

def forward(distance):
    iturtle.Isinit()
    x = gl.globalvar[1][0]
    y = gl.globalvar[1][1]
    p = screen.Point(x, y)
    x_next = x + distance * math.sin(math.radians(gl.angle))
    y_next = y + distance * math.cos(math.radians(gl.angle))
    errorthrow(x_next, y_next)
    p3 = screen.Point((int)(x_next+0.5), (int)(y_next+0.5))
    if gl.status == 'pendown':
        gl.globalvar[0][0] = gl.globalvar[1][0]
        gl.globalvar[0][1] = gl.globalvar[1][1]
        gl.globalvar[0][2] = gl.globalvar[1][2]
        gl.globalvar[0][3] = gl.globalvar[1][3]
        gl.globalvar[0][4] = gl.globalvar[1][4]
        gl.globalvar[1][0] = (int)(x_next+0.5)
        gl.globalvar[1][1] = (int)(y_next+0.5)
        gl.globalvar[1][2] = gl.angle
        gl.globalvar[1][3] = 1
        gl.globalvar[1][4] = gl.pencolor
    elif gl.status == 'penup':
        gl.globalvar[0][0] = gl.globalvar[1][0]
        gl.globalvar[0][1] = gl.globalvar[1][1]
        gl.globalvar[0][2] = gl.globalvar[1][2]
        gl.globalvar[0][3] = gl.globalvar[1][3]
        gl.globalvar[0][4] = gl.globalvar[1][4]
        gl.globalvar[1][0] = (int)(x_next+0.5)
        gl.globalvar[1][1] = (int)(y_next+0.5)
        gl.globalvar[1][2] = gl.angle
        gl.globalvar[1][3] = 0
        gl.globalvar[1][4] = gl.pencolor    
    if gl.visable == True: 
        if gl.globalvar[0][3] == 1:
            screen.triangle(p, 6, 8, gl.globalvar[0][2], 0xffff)
            screen.triangle(p3, 6, 8, gl.angle, gl.pencolor)
            screen.line(p, p3, gl.globalvar[0][4])
        elif gl.status == "pendown":
            screen.triangle(p3, 6, 8, gl.angle, gl.pencolor)
    elif gl.visable == False:
        if gl.globalvar[0][3] == 1:
            screen.line(p, p3, gl.globalvar[0][4])            

def backward(distance):
    iturtle.Isinit()
    x = gl.globalvar[1][0]
    y = gl.globalvar[1][1]
    p = screen.Point(x, y)
    x_next = x - distance * math.sin(math.radians(gl.angle))
    y_next = y - distance * math.cos(math.radians(gl.angle))
    errorthrow(x_next, y_next)
    p3 = screen.Point((int)(x_next+0.5), (int)(y_next+0.5))
    if gl.status == 'pendown':
        gl.globalvar[0][0] = gl.globalvar[1][0]
        gl.globalvar[0][1] = gl.globalvar[1][1]
        gl.globalvar[0][2] = gl.globalvar[1][2]
        gl.globalvar[0][3] = gl.globalvar[1][3]
        gl.globalvar[0][4] = gl.globalvar[1][4]
        gl.globalvar[1][0] = (int)(x_next+0.5)
        gl.globalvar[1][1] = (int)(y_next+0.5)
        gl.globalvar[1][2] = gl.angle
        gl.globalvar[1][3] = 1
        gl.globalvar[1][4] = gl.pencolor
    elif gl.status == 'penup':
        gl.globalvar[0][0] = gl.globalvar[1][0]
        gl.globalvar[0][1] = gl.globalvar[1][1]
        gl.globalvar[0][2] = gl.globalvar[1][2]
        gl.globalvar[0][3] = gl.globalvar[1][3]
        gl.globalvar[0][4] = gl.globalvar[1][4]
        gl.globalvar[1][0] = (int)(x_next+0.5)
        gl.globalvar[1][1] = (int)(y_next+0.5)
        gl.globalvar[1][2] = gl.angle
        gl.globalvar[1][3] = 0
        gl.globalvar[1][4] = gl.pencolor     
    if gl.visable == True: 
        if gl.globalvar[0][3] == 1:
            screen.triangle(p, 6, 8, gl.globalvar[0][2], 0xffff)
            screen.triangle(p3, 6, 8, gl.angle, gl.pencolor)
            screen.line(p, p3, gl.globalvar[0][4])
        elif gl.status == "pendown":
            screen.triangle(p3, 6, 8, gl.angle, gl.pencolor)
    elif gl.visable == False:
        if gl.globalvar[0][3] == 1:
            screen.line(p, p3, gl.globalvar[0][4]) 

def left(angle):
    iturtle.Isinit()
    gl.angle += angle
    x = gl.globalvar[1][0]
    y = gl.globalvar[1][1]
    p = screen.Point(x, y)
    gl.globalvar[0][0] = gl.globalvar[1][0]
    gl.globalvar[0][1] = gl.globalvar[1][1]
    gl.globalvar[0][2] = gl.globalvar[1][2]
    gl.globalvar[0][3] = gl.globalvar[1][3]
    gl.globalvar[0][4] = gl.globalvar[1][4]
    gl.globalvar[1][2] = gl.angle
    if gl.visable == True:
        if gl.status == 'pendown':
            screen.triangle(p, 6, 8, gl.globalvar[0][2], 0xffff)
            screen.triangle(p, 6, 8, gl.angle, gl.pencolor)

def right(angle):
    iturtle.Isinit()
    if gl.angle - angle < 0:
        gl.angle = gl.angle - angle + 360
    else:
        gl.angle -= angle
    x = gl.globalvar[1][0]
    y = gl.globalvar[1][1]
    p = screen.Point(x, y)
    gl.globalvar[0][0] = gl.globalvar[1][0]
    gl.globalvar[0][1] = gl.globalvar[1][1]
    gl.globalvar[0][2] = gl.globalvar[1][2]
    gl.globalvar[0][3] = gl.globalvar[1][3]
    gl.globalvar[0][4] = gl.globalvar[1][4]
    gl.globalvar[1][2] = gl.angle
    if gl.visable == True:
        if gl.status == 'pendown':
            screen.triangle(p, 6, 8, gl.globalvar[0][2], 0xffff)
            screen.triangle(p, 6, 8, gl.angle, gl.pencolor)

def setheading(angle):
    iturtle.Isinit()
    while angle < 0:
        angle += 360
    gl.angle = angle
    x = gl.globalvar[1][0]
    y = gl.globalvar[1][1]
    p = screen.Point(x, y)
    gl.globalvar[0][0] = gl.globalvar[1][0]
    gl.globalvar[0][1] = gl.globalvar[1][1]
    gl.globalvar[0][2] = gl.globalvar[1][2]
    gl.globalvar[0][3] = gl.globalvar[1][3]
    gl.globalvar[0][4] = gl.globalvar[1][4]
    gl.globalvar[1][2] = gl.angle
    if gl.visable == True:
        if gl.status == 'pendown':
            screen.triangle(p, 6, 8, gl.globalvar[0][2], 0xffff)
            screen.triangle(p, 6, 8, gl.angle, gl.pencolor)

def goto(a, b):
    iturtle.Isinit()
    x = gl.globalvar[1][0]
    y = gl.globalvar[1][1]
    p = screen.Point(x, y)
    errorthrow(a, b)
    p3 = screen.Point(a, b)
    if gl.status == 'pendown':
        gl.globalvar[0][0] = gl.globalvar[1][0]
        gl.globalvar[0][1] = gl.globalvar[1][1]
        gl.globalvar[0][2] = gl.globalvar[1][2]
        gl.globalvar[0][3] = gl.globalvar[1][3]
        gl.globalvar[1][0] = a
        gl.globalvar[1][1] = b
        gl.globalvar[1][2] = gl.angle
        gl.globalvar[1][3] = 1
        gl.globalvar[1][4] = gl.pencolor
    elif gl.status == 'penup':
        gl.globalvar[0][0] = gl.globalvar[1][0]
        gl.globalvar[0][1] = gl.globalvar[1][1]
        gl.globalvar[0][2] = gl.globalvar[1][2]
        gl.globalvar[0][3] = gl.globalvar[1][3]
        gl.globalvar[1][0] = a
        gl.globalvar[1][1] = b
        gl.globalvar[1][2] = gl.angle
        gl.globalvar[1][3] = 1
        gl.globalvar[1][4] = gl.pencolor
    if gl.visable == True:
        if gl.globalvar[0][3] == 1:
            screen.triangle(p, 6, 8, gl.globalvar[0][2], 0xffff)
            screen.triangle(p3, 6, 8, gl.angle, gl.pencolor)
            screen.line(p, p3, gl.globalvar[0][4])
        elif gl.status == "pendown":
            screen.triangle(p3, 6, 8, gl.angle, gl.pencolor)
    elif gl.visable == False:
        if gl.globalvar[0][3] == 1:
            screen.line(p, p3, gl.globalvar[0][4])

def pendown():
    iturtle.Isinit()
    gl.status = 'pendown'
    gl.globalvar[1][3] = 1
    x = gl.globalvar[1][0]
    y = gl.globalvar[1][1]
    p = screen.Point(x, y)
    if gl.visable == True:
        screen.triangle(p, 6, 8, gl.angle, gl.pencolor)

def penup():
    iturtle.Isinit()
    gl.status = 'penup'
    gl.globalvar[1][3] = 0
    x = gl.globalvar[1][0]
    y = gl.globalvar[1][1]
    p = screen.Point(x, y)
    if gl.visable == True:
        screen.triangle(p, 6, 8, gl.angle, 0xffff)

# def circle(radius, color):
#     x = gl.globalvar[gl.count][0]
#     y = gl.globalvar[gl.count][1]
#     p = screen.Point(x, y)
#     if gl.status == 'pendown':
#         screen.circle(p, radius, color)
