# pi-arduino-I2C
Simple pin control over I2C using the python smbus2 library for Raspberry Pi and the Wire library for Arduino.
Make sure you're using a decent bi-directional level controller that explicitly supports I2C, like this one: https://www.adafruit.com/product/757 Other level converters refer to "bi-directional" for serial communication, but for I2C the signal must be bi-directional on the same line.
