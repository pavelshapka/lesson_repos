import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
TroykaMoudle = 17
comparator = 4
val = []

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac + leds, GPIO.OUT, initial = GPIO.LOW)
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
    for i in range(7, -1, -1):
        bin2dac(value + 2 ** i)
        time.sleep(0.0008)
        comparatorValue = GPIO.input(comparator)
        if comparatorValue == 1:
            value += 2 ** i
    return value

try:
    chek = True
    GPIO.output(TroykaMoudle, 1) #Подаем питание на тройку-модуль
    start = time.time() #Засекаем начало эксперимента
    print('Началась зарядка конденсатора.')
    while True:
        value = adc() #Считываем аналоговый сигнал с конденсатора
        GPIO.output(leds, decimal2binary(value)) #Отображаем значение value на панели leds
        if value >= 245 and chek: #Если зарядились, то отключаем питание
            GPIO.output(17, 0)
            print('Началась разрядка конденастора')
            chek = False
        if chek == False and value <= 5: #Если зарядились, то заканчиваем эксперимент
            end = time.time() #засекаем конец эксперимента
            T = (end - start)/(len(val)-1) #Считаем период
            ny = 1/T #Считаем частоту
            break
        val.append(value) #Добавляем значение в список всех аналоговых значений 
        voltage = maxVoltage / levels * value
        print("digital value =  {:^3}, analog VOLTAGE = {:.2f}".format(value, voltage))
    
    plt.plot(val)
    with open('data.txt', 'w') as f1:
        for i in range(len(val)):
            f1.write(str(val[i]) + '\n')          
    with open('settings.txt', 'w') as f2:
        f2.write('T = ' + str(T) + '\n')
        f2.write('Ny = '+ str(ny))
        
    plt.show()
    
except KeyboardInterrupt:
    print("Прервано")
finally:
    GPIO.output(dac + leds, GPIO.LOW)
    GPIO.cleanup(dac)