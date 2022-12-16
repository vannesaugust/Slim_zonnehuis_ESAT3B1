import socket
import pickle
from cryptography import fernet

import RPi.GPIO as GPIO #dit gaat enkel op de raspberry zelf enkel kunnen geïnstalleerd worden
import time
GPIO.setwarnings(False)

#setup leds raspberry pi
LED_PIN_wasmachine = 2
LED_PIN_warmtepomp = 3
LED_PIN_droogkast = 4
LED_PIN_koelkast = 17
LED_PIN_vaatwas = 27
LED_PIN_batterij_ontladen = 22
LED_PIN_batterij_opladen = 5
LED_PIN_auto = 13
LED_PIN_robotmaaier = 6




GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_wasmachine, GPIO.OUT)
GPIO.setup(LED_PIN_warmtepomp, GPIO.OUT)
GPIO.setup(LED_PIN_droogkast, GPIO.OUT)
GPIO.setup(LED_PIN_koelkast, GPIO.OUT)
GPIO.setup(LED_PIN_vaatwas, GPIO.OUT)
GPIO.setup(LED_PIN_batterij_ontladen, GPIO.OUT)
GPIO.setup(LED_PIN_batterij_opladen, GPIO.OUT)
GPIO.setup(LED_PIN_auto, GPIO.OUT)
GPIO.setup(LED_PIN_robotmaaier, GPIO.OUT)


#variables connectie
HOST = "169.254.115.194"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
print(HOST)
print(PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    data = s.recv(1024)
    key = b't75ggizya6BwEUJ6M8PL8pKy2Cg-FEkInqHeV9GXwZo='
    data = fernet.Fernet(key).decrypt(data)
    werking_leds = pickle.loads(data)
    print(werking_leds)

    for i in range(len(werking_leds[0])):
        if werking_leds[0][i].lower() == 'wasmachine':
            if werking_leds[1][i] == 1:
                GPIO.output(LED_PIN_wasmachine, GPIO.HIGH)

            else:
                GPIO.output(LED_PIN_wasmachine, GPIO.LOW)


        if werking_leds[0][i].lower() == 'warmtepomp':
            if werking_leds[1][i] == 1:
                GPIO.output(LED_PIN_warmtepomp, GPIO.HIGH)

            else:
                GPIO.output(LED_PIN_warmtepomp, GPIO.LOW)



        if werking_leds[0][i].lower() == 'droogkast':
            if werking_leds[1][i] == 1:
                GPIO.output(LED_PIN_droogkast, GPIO.HIGH)

            else:
                GPIO.output(LED_PIN_droogkast, GPIO.LOW)


        if werking_leds[0][i].lower() == 'koelkast':
            if werking_leds[1][i] == 1:
                GPIO.output(LED_PIN_koelkast, GPIO.HIGH)

            else:
                GPIO.output(LED_PIN_koelkast, GPIO.LOW)


        if werking_leds[0][i].lower() == 'vaatwas':
            if werking_leds[1][i] == 1:
                GPIO.output(LED_PIN_vaatwas, GPIO.HIGH)

            else:
                GPIO.output(LED_PIN_vaatwas, GPIO.LOW)

        if werking_leds[0][i].lower() == 'batterij_ontladen': #met rode LED
            if werking_leds[1][i] == 1:
                GPIO.output(LED_PIN_batterij_ontladen, GPIO.HIGH)

            else:
                GPIO.output(LED_PIN_batterij_ontladen, GPIO.LOW)

        if werking_leds[0][i].lower() == 'batterij_opladen': #met groende LED
            if werking_leds[1][i] == 1:
                GPIO.output(LED_PIN_batterij_opladen, GPIO.HIGH)

            else:
                GPIO.output(LED_PIN_batterij_opladen, GPIO.LOW)


        if werking_leds[0][i].lower() == 'elektrische auto':
            if werking_leds[1][i] == 1:
                GPIO.output(LED_PIN_auto, GPIO.HIGH)

            else:
                GPIO.output(LED_PIN_auto, GPIO.LOW)
                
        if werking_leds[0][i].lower() == 'robotmaaier':
            if werking_leds[1][i] == 1:
                GPIO.output(LED_PIN_robotmaaier, GPIO.HIGH)

            else:
                GPIO.output(LED_PIN_robotmaaier, GPIO.LOW)
        
        



