import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
lvl = 2**(len(dac))
MaxV = 3.3

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
try:
    while True:
        n = input("Введите число от 1 до 255: ")
        if n == 'q':
            break
        elif n < '0' and n > '9':
            print("Введите корректное число")
            continue
        else:
            n = int(n)
            dec2dac(n)
            volt = MaxV / lvl * n
            print(n, '-', volt)
finally:
    GPIO.output(dac, [0, 0, 0, 0, 0, 0, 0, 0])
    GPIO.cleanup()
