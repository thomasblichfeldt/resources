import os
import socket
import machine
import time
import urequests as requests
from machine import SPI
from machine import Pin
from machine import ADC
from network import WLAN

wlan = WLAN(mode=WLAN.STA)
csPin = Pin('G16', mode=Pin.OUT)
relayPin = Pin('G23', mode=Pin.OUT)
spi = SPI(0, mode=SPI.MASTER, baudrate=100000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB)
adc = ADC(0)
adc_c = adc.channel(pin='G5')

def connectWifi():
    nets = wlan.scan()
    for net in nets:
        if net.ssid == 'pitlab-local':
            print('Network found!')
            wlan.connect(net.ssid, auth=(net.sec, ''), timeout=5000)
            while not wlan.isconnected():
                machine.idle() # save power while waiting
            print('WLAN connection succeeded!')
            break

def http_get(url):
    try:
        r = requests.get(url)
        string = str((r.json()))
        info = string.split(',')
        return info
    except OSError as e:
        print(str(e))

def readDB(fbInfo):
    currentLikes = fbInfo[0]
    currentLikes = currentLikes[14:]
    f = open('miniDB.txt')
    miniDB = str(f.read()).split('\n')
    miniDB[3] = currentLikes
    f.close()
    return miniDB

def calculateWaterTokes(miniDB):
    totalLikes = int(miniDB[0])
    pendingLikes = int(miniDB[1])
    waterTokens = int(miniDB[2])
    newTotalLikes = int(miniDB[3])
    newLikes = newTotalLikes - totalLikes

    pendingLikes = pendingLikes + newLikes
    miniDB[0] = str(totalLikes + newLikes)
    miniDB[2] = str(waterTokens + (pendingLikes // 5))
    miniDB[1] = str(pendingLikes % 5)
    del miniDB[3]
    return miniDB

def writeToMiniDB(miniDB):
    f = open('miniDB.txt', 'w')
    f.write(str(miniDB[0]) + '\n' + str(miniDB[1]) + '\n' + str(miniDB[2]) + '\n')
    f.close()

def humidityAvarage():
    avr = 0
    count = 0
    while(count < 100):
        adc_c()
        avr += adc_c.value()
        count = count + 1
    avr = avr / 100
    print (avr)
    if avr < 10:
        getWater()
    else:
        happy()


def happy():

    print("Happy!")

    csPin.value(0)
    time.sleep_us(500)
    spi.write(0x00); spi.write(0x02); spi.write(0x02); spi.write(0x00); spi.write(0x00); spi.write(0x02); spi.write(0x02); spi.write(0x00)
    spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00)
    spi.write(0x00); spi.write(0x00); spi.write(0x01); spi.write(0x00); spi.write(0x00); spi.write(0x01); spi.write(0x00); spi.write(0x00)
    spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00)
    spi.write(0x00); spi.write(0x01); spi.write(0x00); spi.write(0x02); spi.write(0x00); spi.write(0x00); spi.write(0x01); spi.write(0x00)
    spi.write(0x00); spi.write(0x01); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x01); spi.write(0x00)
    spi.write(0x00); spi.write(0x00); spi.write(0x01); spi.write(0x01); spi.write(0x01); spi.write(0x01); spi.write(0x00); spi.write(0x00)
    spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00)

    time.sleep_us(500)
    csPin.value(1)

def sad():

    print("Sad!")

    csPin.value(0)
    time.sleep_us(500)

    spi.write(0x00); spi.write(0x00); spi.write(0x02); spi.write(0x00); spi.write(0x00); spi.write(0x02); spi.write(0x00); spi.write(0x00)
    spi.write(0x00); spi.write(0x02); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x02); spi.write(0x00)
    spi.write(0x00); spi.write(0x00); spi.write(0x01); spi.write(0x00); spi.write(0x00); spi.write(0x01); spi.write(0x00); spi.write(0x00)
    spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00)
    spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x02); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00)
    spi.write(0x00); spi.write(0x00); spi.write(0x01); spi.write(0x01); spi.write(0x01); spi.write(0x01); spi.write(0x00); spi.write(0x00)
    spi.write(0x00); spi.write(0x01); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x01); spi.write(0x00)
    spi.write(0x00); spi.write(0x01); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x00); spi.write(0x01); spi.write(0x00)

    time.sleep_us(500)
    csPin.value(1)

def off():
    csPin.value(0)
    time.sleep_us(500)
    for x in range(0, 63):
        spi.write(0x00)
    time.sleep_us(500)
    csPin.value(1)

def getWater():
    global waterTokens
    global relayPin
    global miniDB
    if waterTokens > 0:
        print("getting water")
        relayPin.value(1)
        time.sleep_ms(5000)
        relayPin.value(0)
        waterTokens = waterTokens - 1
        miniDB[2] = waterTokens
        writeToMiniDB(miniDB)
        happy()
    else:
        sad()

connectWifi()
while(True):
    facebookInformation = http_get('https://graph.facebook.com/v2.9/1193479840761405?fields=name,fan_count&access_token=EAADZCpkVMmEYBABI4ZCvBoZCUyHnroau1OrQadlfqzaqXz9nygUrBn95pGCJkZBSdqiU3LbGwDT64TZCdgplJZBMz11si1JMDdtH8qxwtqRwidLOO0pZCvJ39rnmHDVjZBcN5H9RFInpZBRo7VaRhgennsQ2PUFy5I48ZD')
    if facebookInformation != None:
        miniDB = readDB(facebookInformation)
        miniDB = calculateWaterTokes(miniDB)
        writeToMiniDB(miniDB)
        totalLikes = int(miniDB[0])
        pendingLikes = int(miniDB[1])
        waterTokens = int(miniDB[2])
    else:
        machine.reset()
    humidityAvarage()
    time.sleep(30)
