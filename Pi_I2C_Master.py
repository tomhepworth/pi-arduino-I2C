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
	return (msb * (2**7)) + lsb			## reassemble the value & return

def digitalWrite(io, v):				##just a wrapper funciton as only one byte needs to be sent, this can be handled by the smbus library just fine
	bus.write_byte_data(address,io,v)

def analogWrite(io, v):
	##analogWrite is only ever used for PWM outout which is a value between 0 and 255. This means we can send the value in only one byte.
	if(v > 255): ##small error handling
		print("PWM output only goes up to 255")
	else:
		bus.write_byte_data(address,(io+128),v)	## set bit 8 to signal an analogWrite



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
		AorD = input("Analog, Digital? a/d:")
		v = int(input("Enter a value: "))

		if(AorD == "a"):
			analogWrite(io,v)

		elif(AorD == "d"):
			digitalWrite(io,v)	## plain old digitalWrite

		else:
			print("ERROR: invalid write type")

	else:
		print("ERROR: invalid mode selected")
