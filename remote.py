from pynput.keyboard import Key, Listener
import socket
import time

#UDP_IP = "127.0.0.1"
UDP_IP = "192.168.72.169"
UDP_PORT = 5006

def on_press(key):
    key = str(key)
    if key == "'w'":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(str(key).encode(), (UDP_IP, UDP_PORT))
        return
    if key == "'s'":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(key.encode(), (UDP_IP, UDP_PORT))
        return
    if key == "'d'":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(key.encode(), (UDP_IP, UDP_PORT))
        return
    if key == "'a'":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(key.encode(), (UDP_IP, UDP_PORT))
        return
    if key == "Key.up":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(key.encode(), (UDP_IP, UDP_PORT))
        return
    if key == "Key.down":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(key.encode(), (UDP_IP, UDP_PORT))
        return

def on_release(key):
    key = '!' + str(key)
    if key == "!'w'":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(key.encode(), (UDP_IP, UDP_PORT))
        return
    if key == "!'s'":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(key.encode(), (UDP_IP, UDP_PORT))
        return
    if key == "!'d'":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(key.encode(), (UDP_IP, UDP_PORT))
        return
    if key == "!'a'":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(key.encode(), (UDP_IP, UDP_PORT))
        return
    if key == "!Key.esc":
        print('Exiting...')
        return

with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
