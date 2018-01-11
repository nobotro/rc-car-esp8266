# tetri-win wasvlaw
#lurji-backward
#narinjisferi-marjvena
#iasamnisferi-marcxena
#tetri scl
#melnisferi sda

from machine import Pin , PWM,I2C

import vl53l0x
import machine
import socket
import utime



UDP_IP = "0.0.0.0"
UDP_PORT = 5006
FB=None


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(0)

# 1 speed - duty 200 2 speed - duty 500 3 speed - duty 1000
speed_gear = {'1': 500,'2': 1000}
speed = 1

pwm_f = PWM(Pin(0))
pwm_b = PWM(Pin(15))

pwm_f.freq(30)
pwm_b.freq(30)
pin_objs={0:pwm_f,15:pwm_b}



r = Pin(1, Pin.OUT)
l = Pin(3, Pin.OUT)







r.off()
l.off()

i2c =None
sensor =None


def forward():


    pwm_b.duty(0)
    pwm_f.duty(speed_gear[str(speed)])

def backword():

    pwm_f.duty(0)
    pwm_b.duty(speed_gear[str(speed)])

def right():
    l.off()
    r.on()

def left():
    r.off()
    l.on()

def stop_move():
    global FB
    FB=None
    pwm_f.duty(0)
    pwm_b.duty(0)

def stop_steering():

    r.off()
    l.off()





def driver():

    global speed
    global FB
    global i2c
    global  sensor

    i2c = I2C(-1, Pin(5), Pin(4))
    sensor = vl53l0x.VL53L0X(i2c)
    sensor.start()

    while True:

        try:
             safety_manager()
        except:pass

        data=None
        try:
            data, addr = sock.recvfrom(1024)
        except:
            pass
        if not data:continue


        key = data.decode()
        if key == "'w'":

            FB = 0
            forward()
        if key == "'s'":

            FB = 15
            backword()
        if key == "'d'":
            right()
        if key == "'a'":
            left()
        if key == "!'w'":
            stop_move()
        if key == "!'s'":
            stop_move()
        if key == "!'d'":
            stop_steering()
        if key == "!'a'":
            stop_steering()
        if key == "Key.up":
            if speed < 2:

                speed += 1
                if FB==0 or FB==15:
                    pin_objs[FB].duty(speed_gear[str(speed)])

        if key == "Key.down":
            if speed > 1:
                speed -= 1
                if FB==0 or FB==15:
                    pin_objs[FB].duty(speed_gear[str(speed)])



def safety_manager():
    global FB
    global sensor
    global sock

    distance = sensor.read()



    if distance >50 and distance <400 :




        stop_move()
        FB = 15
        backword()
        utime.sleep(1)

        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        sock.setblocking(0)

driver()

