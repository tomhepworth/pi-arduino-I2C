from smbus2 import SMBus
import time
# for RPI version 1, use bus = smbus.SMBus(0)
bus = SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x20

##bus.write_byte_data(address,io,value)
def digitalRead(io):
	bus.write_byte(address,io) 		## tells arduino code that we're reading
	time.sleep(0.05) 				## wait to give time for the arduino to read
	return bus.read_byte(address) 	## now get the value & return

def analogRead(io):
	bus.write_byte(address,io + 128) 	## set bit 8 high on io to do an analog read
	time.sleep(0.1) 					## wait for time for the ADC to run
	msb = bus.read_byte(address)		## get first half of value
	lsb = bus.read_byte(address)		## get bottom half of value
	return (msb * (2**8)) + lsb			## reassemble the value & return


while True:
	io = int(input("Enter io (2 - 21): "))
	if not io:
		continue

	mode = input("Read or Write? r/w: ")

	if(mode == "r"):
		AorD = input("Analog or Digital? a/d: ")
		if(AorD == "a"):
			print(analogRead(io))

		elif(AorD == "d"):
			print(digitalRead(io))

		else:
			print("ERROR: invalid read type")

	elif(mode == "w"):
		ADorS = input("Analog, Digital? a/d:")
		v = int(input("Enter a value: "))
		if not v:
			continue

		if(AorD == "a"):
			bus.write_byte_data(address,(io+128),v)	## set bit 8 to signal an analogWrite

		elif(ADorS == "d"):
			bus.write_byte_data(address,io,v)		## plain old digitalWrite

		else:
			print("ERROR: invalid write type")

	else:
		print("ERROR: invalid mode selected")
