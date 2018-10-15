# pi-arduino-I2C
Simple pin control over I2C using the python smbus2 library for Raspberry Pi and the Wire library for Arduino. 

Contains the following wrapper functions to be used on the Pi master as they would on an Arduino:
digitalRead(pin) 
analogRead(pin)

Notes:

1: Make sure you're using a decent bi-directional level controller that explicitly supports I2C, like this one: https://www.adafruit.com/product/757 Other level converters refer to "bi-directional" for serial communication, but for I2C the signal must be bi-directional on the same line.

2: Be careful where serial prints are used in the arduino code. They corrupt the data being sent over i2c due to the interrupt service routine.
