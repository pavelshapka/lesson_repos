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
    for i in range(256):
        dec2dac(i)
        time.sleep(0.05)
        volt = MaxV / lvl * i
        print(i, '-', round(volt, 2))
    for i in range(256):
        dec2dac(256-1-i)
        time.sleep(0.05)
        volt = MaxV / lvl * i
        print(i, '-', round(volt, 2))
except KeyboardInterrupt:
    print("Прервано")
finally:
    GPIO.output(dac, [0, 0, 0, 0, 0, 0, 0, 0])
    GPIO.cleanup()
