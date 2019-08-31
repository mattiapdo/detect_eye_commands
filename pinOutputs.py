import RPi.GPIO as GPIO
from time import sleep

def init_GPIO_pin(pin_number):

    #GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin_number, GPIO.OUT, initial = GPIO.LOW)

def send_signal(pin_number, repeat = 5):

    for i in range(3):
        GPIO.output(pin_number, GPIO.HIGH)
        sleep(0.2)
        GPIO.output(pin_number, GPIO.LOW)
        sleep(0.2)

    for i in range(repeat):
        GPIO.output(pin_number, GPIO.HIGH)
        sleep(1)
        GPIO.output(pin_number, GPIO.LOW)
        sleep(1)

    GPIO.output(pin_number, GPIO.HIGH)
    sleep(3)
    GPIO.output(pin_number, GPIO.LOW)
    
