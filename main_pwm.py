from machine import Pin
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5006

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# 1 speed - duty 200 2 speed - duty 500 3 speed - duty 1000
speed_gear = {'1': 200, '2': 500, '3': 1000}
speed = 1

pwm_f = machine.PWM(Pin(0))
pwm_b = machine.PWM(Pin(4))
pwm_f.freq(60)
pwm_b.freq(60)
# f = Pin(0, Pin.OUT)
# b = Pin(4, Pin.OUT)
r = Pin(5, Pin.OUT)
l = Pin(3, Pin.OUT)

# f.off()
# b.off()
r.off()
l.off()

def forward():
    # b.off()
    # f.on()
    pwm_b.duty(0)
    pwm_f.duty(speed_gear[str(speed)])
    
def backword():
    # f.off()
    # b.on()
    pwm_f.duty(0)
    pwm_b.duty(speed_gear[str(speed)])

def right():
    l.off()
    r.on()

def left():
    r.off()
    l.on()

def stop_move():
    # f.off()
    # b.off()
    pwm_f.duty(0)
    pwm_b.duty(0)

def stop_steering():
    r.off()
    l.off()

while True:
    data, addr = sock.recvfrom(1024)
    key = data.decode()
    if key == "'w'":
        forward()
    if key == "'s'":
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
    if key == "Key.down":
        if key > 1:
            speed -= 1