import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
GPIO.setup(2, GPIO.OUT)
p = GPIO.PWM(2, 1000)

def dec2bin(x):
    res = [0, 0, 0, 0, 0, 0, 0, 0]
    tmp = list(map(int, list(bin(x)[2:])))
    for i in range(len(tmp)):
        res[-1-i] = tmp[-1-i]
    return res

def dec2dac(n):    
    GPIO.setup(dac, GPIO.OUT)
    values = dec2bin(n)
    GPIO.output(dac, values)
    return 0

p.start(0)
try:
    while True:
        n = input("Введите число от 1 до 100: ")
        if n == 'q':
            break
        elif n.isdigit() and int(n) <= 100:
            p.ChangeDutyCycle(int(n))
        else:
            print("Введите корректное число")
            continue
finally:
    p.stop()
    GPIO.cleanup()
