# coding: utf-8
import screen
from Turtle import globalvar as gl
from Turtle import waffle_turtle as turtle

#初始化屏幕
screen.on()
screen.fill(0xffff)

def Isinit():
    if gl.init == False:
        raise NameError("You need to init turtle first!")

#可选参数保证海龟位置处于默认或者自定义
def init(a='', b=''):
    # screen.fill(0xffff)
    if gl.init == False:
        gl.init = True
    else:
        raise NameError("turtle has been initialized,you don't need to init it again.")
    gl.globalvar = [[64, 80, 0, 1, 0xf800],[64, 80, 0, 1, 0xf800]]
    gl.angle = 0
    gl.status = 'pendown'
    gl.pencolor = 0xf800
    if a!='' and b!='':
        turtle.errorthrow(a, b)
        p = screen.Point(a, b)
        gl.globalvar[0]=[a,b,0,1,0xf800]
        gl.globalvar[1]=[a,b,0,1,0xf800]
    elif a!='':
        turtle.errorthrow(a, 80)
        p = screen.Point(a, 80)
        gl.globalvar[0]=[a,80,0,1,0xf800]
        gl.globalvar[1]=[a,80,0,1,0xf800]
    elif b!='':
        turtle.errorthrow(64, b)
        p = screen.Point(64, b)
        gl.globalvar[0]=[64,b,0,1,0xf800]
        gl.globalvar[1]=[64,b,0,1,0xf800]
    else:
        turtle.errorthrow(64, 80)
        p = screen.Point(64, 80)
        gl.globalvar[0]=[64,80,0,1,0xf800]
        gl.globalvar[1]=[64,80,0,1,0xf800]
    if gl.visable == True:
        screen.triangle(p, 6, 8, gl.angle, 0xf800)

def reset():
    gl.init = False
    gl.globalvar = [[64,80,0,1,0xf800],[64,80,0,1,0xf800]]
    gl.angle = 0
    gl.status = 'pendown'
    gl.pencolor = '0xf800'
    screen.fill(0xffff)

def clear():
    Isinit()
    screen.fill(0xffff)
    x = gl.globalvar[1][0]
    y = gl.globalvar[1][1]
    angle = gl.globalvar[1][2]
    sts = gl.globalvar[1][3]
    col = gl.globalvar[1][4]
    gl.globalvar = [[x, y, angle, sts, col],[x, y, angle, sts, col]]
    p = screen.Point(x, y)
    if gl.visable == True:
        if gl.status == 'pendown':
            screen.triangle(p, 6, 8, gl.angle, gl.pencolor)

def color(color):
    Isinit()
    crgb_565 = gl.globalcolor.get(color,None)
    if crgb_565 == None:
        print("此颜色不存在")
    else:
        gl.pencolor = crgb_565
        gl.globalvar[1][4] = crgb_565
        if gl.visable == True and gl.status == 'pendown':
            p = screen.Point(gl.globalvar[1][0], gl.globalvar[1][1])
            screen.triangle(p, 6, 8, gl.angle, 0xffff)
            screen.triangle(p, 6, 8, gl.angle, gl.pencolor)

def hideturtle():
    Isinit()
    gl.visable = False
    p = screen.Point(gl.globalvar[1][0], gl.globalvar[1][1])
    screen.triangle(p, 6, 8, gl.angle, 0xffff)

def showturtle():
    Isinit()
    gl.visable = True
    p = screen.Point(gl.globalvar[1][0], gl.globalvar[1][1])
    screen.triangle(p, 6, 8, gl.angle, gl.pencolor)
