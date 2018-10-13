import smbus
import time
# for RPI version 1, use bus = smbus.SMBus(0)
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x20

##bus.write_byte_data(address,io,value)
def digitalRead(io):
    bus.write_byte(address,io) ##tells arduino code that we're reading from io
    time.sleep(0.1) ##wait to give time for the arduino to analogread io
    return bus.read_byte(address) ## now listen for the value to be sent

def analogRead(io)
    bus.write_byte(address,io + 128) ##tells arduino code that we're reading from io
    time.sleep(0.1) ##wait to give time for the arduino to analogread io
    return bus.read_byte(address) ## now listen for the value to be sent

while True:
    io = int(input("Enter io (2 - 21): "))
    mode = input("read or write? r/w ")
    aOrD = int(input("analog (1) or digital (0)?"));
    if(mode == "r"):
        if not io:
            continue
        if(aOrD == 1):
            print(analogRead(io))
        else:
            print(digitalRead(io))
    elif(mode == "w"):
        v = int(input("Enter a value: "))
        if not io:
            continue
        if(aOrD == 1):
            bus.write_byte_data(address,(io+128),v)
        else:
            bus.write_byte_data(address,io,v)

    else:
        print("error: no mode selected")
