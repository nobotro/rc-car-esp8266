from machine import Pin , PWM
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
pwm_b = PWM(Pin(4))

pwm_f.freq(30)
pwm_b.freq(30)
pin_objs={0:pwm_f,4:pwm_b}



r = Pin(5, Pin.OUT)
l = Pin(3, Pin.OUT)
trig = Pin(1, Pin.OUT)
echo = Pin(15, Pin.IN)






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





def driver():
    global speed
    while True:

        safety_manager()
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
            if speed < 2:

                speed += 1
                if FB==0 or FB==4:
                    pin_objs[FB].duty(speed_gear[str(speed)])

        if key == "Key.down":
            if speed > 1:
                speed -= 1
                if FB==0 or FB==4:
                    pin_objs[FB].duty(speed_gear[str(speed)])



def safety_manager():

        global FB



        trig.value(0)  # Stabilize the sensor
        utime.sleep_us(5)
        trig.value(1)
        # Send a 10us pulse.
        utime.sleep_us(10)
        trig.value(0)
        echo = Pin(15, Pin.IN)
        try:

            pulse_time = machine.time_pulse_us(echo, 1,500*2*30)
            cm = pulse_time / 58.2
            print(cm)
            if cm >5 and cm <15 :
                print('warning')

                FB = 4
                backword()
                utime.sleep(2)
                stop_move()

        except :
             pass



driver()


