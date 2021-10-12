import RPi.GPIO as GPIO
import import time
dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
TroykaMoudle = 17
comparator = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(TroykaMoudle, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comparator, GPIO.IN)

def decimal2binary(i):
    return [int(elem) for elem in bin(i)[2:].zfill(bits)]

def bin2dac(i): 
     signal = decimal2binary(i)
     GPIO.output(dac, signal)
     return signal   
def adc():
    value = 0
    for i in range(8):
        bin2dac(value + 2 ** i)
        time.sleep(0.0005)
        comparatorValue = GPIO.input(comparator)
        if i == 8:
            if comparatorValue == 1:
                value -= 1
        else:
            if comparatorValue == 0:
                value += 2 ** i
            else:
                value -= 2 ** (i - 1) + 2 ** i
    return value
try:
    while True:
       value = adc()
       voltage = maxVoltage / levels * value 
       print("digital value =  {:^3}, analog VOLTAGE = {:.2f}".format(value, voltage))
except KeyboardInterrupt:
    print("Прервано")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)