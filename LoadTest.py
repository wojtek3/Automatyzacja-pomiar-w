import serial
import time as tim
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, time, datetime

ser = serial.Serial("COM7", 9600) 
readCommand = b'\xAA\x04\x91\x00\x00\x40\x00\x40\x05\x00\x00\x30\x75\xB8\x0B\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x2E'
commandPC = b'\xAA\x04\x92\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x42'
commandON = b'\xAA\x04\x92\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x43'
commandOFF = b'\xAA\x04\x92\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x42'

def readData():
    ser.flushInput()
    ser.flushOutput()
    ser.write(readCommand)
    data = ser.read(26)
    datahex = data.hex()
    bytelist = [datahex[i:i+2] for i in range(0,len(datahex),2)]
    current = bytelist[4] + bytelist[3]
    current = int(current,16)/1000

    voltage = bytelist[8] + bytelist[7] + bytelist[6] + bytelist[5]
    voltage = int(voltage,16)/1000

    power = bytelist[10] + bytelist[9]
    power = int(power,16)/10
    return (current, voltage, power)

def writeCurrent(current):
    ser.flushInput()
    ser.flushOutput()
    setCommand = bytearray(b'\xAA\x04\x90\x30\x75\xB8\x0B\x04\x01')
    hexSet = current.to_bytes(2,'little')
    setCommand.extend(hexSet)
    endCommand = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    setCommand.extend(endCommand)
    checksum = int(hex(sum(setCommand))[-2:],16)
    setCommand.append(checksum)
    ser.write(setCommand)

def writeVoltage(voltage):
    ser.flushInput()
    ser.flushOutput()
    setCommand = bytearray(b'\xAA\x04\x90\x30\x75\xB8\x0B\x04\x01')
    hexSet = current.to_bytes(2,'little')
    setCommand.extend(hexSet)
    endCommand = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    setCommand.extend(endCommand)
    checksum = int(hex(sum(setCommand))[-2:],16)
    setCommand.append(checksum)
    ser.write(setCommand)

def plotCharacteristics(data):
    df = pd.DataFrame(data, columns = ['prad', 'napiecie', 'power','setcurrent'])
    plt.plot(df['napiecie'], df['prad'])
    plt.plot(df['napiecie'], df['power'])
    plt.title("Charakterystyka I-U, P-U")
    plt.xlabel("Napięcie [V]")
    plt.ylabel("Prąd [A]")
    plt.show()

def measure(startCurrent, endCurrent, stepSize, delay):
    data = []
    startTime = int(tim.time() * 1000)
    for i in range(startCurrent,endCurrent,stepSize):
        writeCurrent(i)
        tim.sleep(delay)
        curr = readData()
        curr = curr + (i,)
        data.append(curr)
        print(curr)
        
    writeCurrent(0)
    stopTime = int(tim.time() * 1000)
    print("Czas pomiaru: " + str(stopTime-startTime) + "ms")
    df = pd.DataFrame(data, columns = ['prad', 'napiecie', 'power', 'setcurrent'])
    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y %H-%M-%S")
    df.to_csv("results" + date_time + ".csv", index=False)
    return data

def main():
    ser.write(commandPC)
    tim.sleep(0.1)
    ser.write(commandON)
    data = measure(100,4000,30,0.01)
    plotCharacteristics(data)

main()


