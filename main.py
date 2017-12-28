from machine import Pin , PWM
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5006
FB=None


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# 1 speed - duty 200 2 speed - duty 500 3 speed - duty 1000
speed_gear = {'1': 200, '2': 500, '3': 1000}
speed = 1

pwm_f = PWM(Pin(0))
pwm_b = PWM(Pin(4))
pin_objs={0:pwm_f,4:pwm_b}
pwm_f.freq(60)
pwm_b.freq(60)



r = Pin(5, Pin.OUT)
l = Pin(3, Pin.OUT)


r.off()
l.off()

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

while True:
    data, addr = sock.recvfrom(1024)
    key = data.decode()
    if key == "'w'":

        FB = 0
        forward()
    if key == "'s'":

        FB = 4
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
        if speed < 3:

            speed += 1
            if FB:
                pin_objs[FB].duty(speed_gear[str(speed)])

    if key == "Key.down":
        if speed > 1:
            speed -= 1
            if FB:
                pin_objs[FB].duty(speed_gear[str(speed)])