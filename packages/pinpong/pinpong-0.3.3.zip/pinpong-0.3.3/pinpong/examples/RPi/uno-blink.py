# -*- coding: utf-8 -*-

#RPi and PythonBoard 
#实验效果：控制板载LED灯一秒闪烁一次

import time
from pinpong.board import Board,Pin

rpi = Board("RPi").begin()
uno = Board("Uno").begin()
Board.set_default_board(uno)

uno_led = Pin(Pin.D13, Pin.OUT) #由于uno是默认板子，所以这里可以省略板子参数
rpi_led = Pin(rpi, Pin.D26, Pin.OUT) #由于uno是默认板子，所以这里需要指明使用rpi板子资源

while True:
  uno_led.value(1) #输出高电平
  rpi_led.value(1)
  time.sleep(1) #等待1秒 保持状态

  uno_led.value(0) #输出低电平
  rpi_led.value(0) #输出低电平
  time.sleep(1) #等待1秒 保持状态
