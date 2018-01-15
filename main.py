from machine import Pin , PWM,I2C
import vl53l0x
import machine
import socket
import utime

# TODO brzanebis ertxel gagzavnis gaketeba

UDP_IP = "0.0.0.0"
UDP_PORT = 5006

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(0)

# 1 speed - duty 500 2 speed - duty 1000
speed_gear = {'1': 500,'2': 1000}
speed = 1

pwm_f = PWM(Pin(0)) # tetri-forward
pwm_b = PWM(Pin(15)) # lurji-backward
pwm_f.freq(30)
pwm_b.freq(30)
pin_objs = {0:pwm_f,15:pwm_b}

r = Pin(1, Pin.OUT) # narinjisferi-right
l = Pin(3, Pin.OUT) # iasamnisferi-left

FB = None
i2c = None
sensor = None

def forward():
    global FB
    FB = 0
    pwm_b.duty(0)
    pwm_f.duty(speed_gear[str(speed)])

def backword():
    global FB
    FB = 15
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
    FB = None
    pwm_f.duty(0)
    pwm_b.duty(0)

def stop_steering():
    r.off()
    l.off()

stop_steering()

def parking(sensor):
    global proximity_enable
    proximity_enable = False
    while True:
        if 500 > sensor.read() > 80:
            print(sensor.read())
            utime.sleep(0.2)
            forward()
            utime.sleep(0.1)
        else:
            return
        stop_move()

def driver():
    global speed
    global FB
    global i2c
    global sensor
    global sock
    proximity_enable = True
    i2c = I2C(-1, Pin(5), Pin(4)) # tetri-scl, melnisferi-sda
    sensor = vl53l0x.VL53L0X(i2c)
    sensor.start()
    while True:
        if proximity_enable:
            try:
                if 50  < sensor.read() < 400:
                    backword()
                    utime.sleep(1)
                    stop_move()
                    sock.close()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.bind((UDP_IP, UDP_PORT))
                    sock.setblocking(0)
            except:
                pass
        data = None
        try:
            data, addr = sock.recvfrom(1024)
        except:
            pass
        if not data:
            continue
        key = data.decode()
        if key == "'w'":
            forward()
        if key == "'s'":
            backword()
        if key == "'d'":
            right()
        if key == "'a'":
            left()
        if key == "'t'":
            if proximity_enable:
                proximity_enable = False
            else:
                proximity_enable = True
        if key == "'p'":
            parking(sensor)
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
                if FB == 0 or FB == 15:
                    pin_objs[FB].duty(speed_gear[str(speed)])

driver()
