import screen
from screen import Point
import utime

import Turtle.init_turtle as init_turtle
import Turtle.waffle_turtle as turtle
import Turtle.globalvar as gl

gameover = 0

def rules():
    global gameover
    if gl.globalvar[1][0] in range(5,15) and gl.globalvar[1][1] in range(30,110):
        return True
    elif gl.globalvar[1][0] in range(15,45) and gl.globalvar[1][1] in range(80,90):
        return True
    elif gl.globalvar[1][0] in range(45,55) and gl.globalvar[1][1] in range(60,130):
        return True
    elif gl.globalvar[1][0] in range(55,75) and (gl.globalvar[1][1] in range(60,70) or gl.globalvar[1][1] in range(120,130)):
        return True
    elif gl.globalvar[1][0] in range(75,85) and (gl.globalvar[1][1] in range(30,70) or gl.globalvar[1][1] in range(120,130)):
        return True
    elif gl.globalvar[1][0] in range(85,95) and (gl.globalvar[1][1] in range(30,40) or gl.globalvar[1][1] in range(60,70) or gl.globalvar[1][1] in range(90,130)):
        return True
    elif gl.globalvar[1][0] in range(95,115) and (gl.globalvar[1][1] in range(30,40) or gl.globalvar[1][1] in range(60,70) or gl.globalvar[1][1] in range(90,100) or gl.globalvar[1][1] in range(120,130)):
        return True
    elif gl.globalvar[1][0] in range(115,125) and gl.globalvar[1][1] in range(30,40):
        gameover = 1
        return False
    elif gl.globalvar[1][0] in range(115,125) and (gl.globalvar[1][1] in range(30,40) or gl.globalvar[1][1] in range(60,70) or gl.globalvar[1][1] in range(90,130)):
        return True
    else:
        gameover = 2
        return False


def game_end():
    if gameover == 1:
        init_turtle.reset()
        p = screen.Point(50,155)
        screen.print(p,"You Win",clr = 0xf800, bg = 0xffff, size = 4, direction = screen.ROTATE_90)
    elif gameover == 2:
        init_turtle.reset()
        p = screen.Point(50,155)
        screen.print(p,"You Lose",clr = 0x001f, bg = 0xffff, size = 4, direction = screen.ROTATE_90)

def map():
    init_turtle.reset()
    init_turtle.init(10,40)
    init_turtle.showturtle()
    init_turtle.color('blue')
    #建立坐标轴表明方向
    p = screen.Point(7,3)
    p_x = screen.Point(17,3)
    p_y = screen.Point(7,13)
    screen.line(p,p_x,0x0000)
    screen.line(p,p_y,0x0000)
    screen.triangle(p_x,3,4,90,0x0000)
    screen.print(p_x, 'x')
    screen.triangle(p_y,3,4,0,0x0000)
    screen.print(p_y, 'y', direction = screen.ROTATE_90)
    #终点
    p_end = screen.Point(120,35)
    screen.fill_circle(p_end, 4, 0xf800)
    #迷宫设置
    p_11 = screen.Point(5,30)
    p_12 = screen.Point(5,110)
    p_21 = screen.Point(15,30)
    p_22 = screen.Point(15,80)
    p_23 = screen.Point(15,90)
    p_24 = screen.Point(15,110)
    p_31 = screen.Point(45,60)
    p_32 = screen.Point(45,80)
    p_33 = screen.Point(45,90)
    p_34 = screen.Point(45,130)
    p_41 = screen.Point(55,70)
    p_42 = screen.Point(55,120)
    p_51 = screen.Point(75,30)
    p_52 = screen.Point(75,60)
    p_61 = screen.Point(85,40)
    p_62 = screen.Point(85,60)
    p_63 = screen.Point(85,90)
    p_64 = screen.Point(85,120)
    p_71 = screen.Point(95,100)
    p_72 = screen.Point(95,120)
    p_81 = screen.Point(115,100)
    p_82 = screen.Point(115,120)
    p_91 = screen.Point(125,30)
    p_92 = screen.Point(125,40)
    p_93 = screen.Point(125,60)
    p_94 = screen.Point(125,70)
    p_95 = screen.Point(125,90)
    p_96 = screen.Point(125,130)

    screen.line(p_11, p_21, 0x03ef)
    screen.line(p_12, p_24, 0x03ef)
    screen.line(p_12, p_11, 0x03ef)
    screen.line(p_21, p_22, 0x03ef)
    screen.line(p_23, p_24, 0x03ef)
    screen.line(p_22, p_32, 0x03ef)
    screen.line(p_23, p_33, 0x03ef)
    screen.line(p_32, p_31, 0x03ef)
    screen.line(p_33, p_34, 0x03ef)
    screen.line(p_41, p_42, 0x03ef)
    screen.line(p_31, p_52, 0x03ef)
    screen.line(p_52, p_51, 0x03ef)
    screen.line(p_61, p_62, 0x03ef)
    screen.line(p_42, p_64, 0x03ef)
    screen.line(p_64, p_63, 0x03ef)
    screen.line(p_71, p_72, 0x03ef)
    screen.line(p_71, p_81, 0x03ef)
    screen.line(p_72, p_82, 0x03ef)
    screen.line(p_81, p_82, 0x03ef)
    screen.line(p_51, p_91, 0x03ef)
    screen.line(p_61, p_92, 0x03ef)
    screen.line(p_62, p_93, 0x03ef)
    screen.line(p_41, p_94, 0x03ef)
    screen.line(p_63, p_95, 0x03ef)
    screen.line(p_34, p_96, 0x03ef)
    screen.line(p_91, p_92, 0x03ef)
    screen.line(p_93, p_94, 0x03ef)
    screen.line(p_95, p_96, 0x03ef)

def gameplay():
    map()

    # 终端命令玩
    # while True:
    #     if not rules():
    #         break
    #     else:
    #         game_continue = input("Please input the command:")
    #         exec('turtle.' + game_continue)

            # 通关攻略
            # turtle.forward(45)
            # turtle.left(90)
            # turtle.forward(40)
            # turtle.left(90)
            # turtle.forward(20)
            # turtle.right(90)
            # turtle.forward(30)
            # turtle.left(90)
            # turtle.forward(30)
            # turtle.right(90)
            # turtle.forward(40)
    # game_end()

def game_restart():
    gameplay()

