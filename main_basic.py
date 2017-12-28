from machine import Pin
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5006

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

f = Pin(0, Pin.OUT)
b = Pin(4, Pin.OUT)
r = Pin(5, Pin.OUT)
l = Pin(3, Pin.OUT)

f.off()
b.off()
r.off()
l.off()

def forward():
    b.off()
    f.on()
    
def backword():
    f.off()
    b.on()

def right():
    l.off()
    r.on()

def left():
    r.off()
    l.on()

def stop_move():
    f.off()
    b.off()

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