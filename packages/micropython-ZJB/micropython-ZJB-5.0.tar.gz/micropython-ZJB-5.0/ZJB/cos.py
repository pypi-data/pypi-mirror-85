import screen
import math
import time
from  screen import Point
screen.on()
screen.fill(0xffff)#设置为白色
# 屏幕像素128*160,x:128,y:160
# 坐标原点：（64，80）
p1 = screen.Point(64,0) #绘制成x轴正方向
p2 = screen.Point(64,160)#绘制成x轴负方向

p3 = screen.Point(0,80)#绘制成y轴正方向
p4 = screen.Point(128,80)#绘制成y轴负方向

p5 = screen.Point(59,5)#绘制成x轴正方向箭头:上
p6 = screen.Point(69,5)#绘制成x轴正方向箭头:下

p7 = screen.Point(5,85)#绘制成y轴正方向箭头:左
p8 = screen.Point(5,75)#绘制成y轴正方向箭头:右

screen.line(p1,p2,0xf800)#绘制成x轴
screen.line(p3,p4,0xf800)#绘制成y轴

screen.line(p1,p5,0xf800)#绘制成x轴正方向箭头
screen.line(p1,p6,0xf800)

screen.line(p3,p7,0xf800)#绘制成y轴正方向箭头
screen.line(p3,p8,0xf800)

#x1=64-y2
#y1=80-x2

for x2 in range(-80,80):
    y2=40*(math.cos(x2*3.14/64))
    print("x2：",x2)
    print("y2：",y2)
    x1=64-y2
    y1=80-x2
    p9 = screen.Point(int(x1),y1)
    screen.pixel(p9,0xf800)
    time.sleep(0.2)
  
