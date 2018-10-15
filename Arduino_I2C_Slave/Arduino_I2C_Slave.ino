#include <Wire.h>


// I2C support
#define SLAVE_ADDRESS 0x20
int value = 0;
byte readCount = 0;

void setup() {
  Serial.begin(57600);
  Serial.print("Setup");


  // Setup pins & initialise I2C as slave
  pinMode(A4, INPUT_PULLUP);
  pinMode(A5, INPUT_PULLUP);
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for I2C communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  Serial.println("Ready");
}

void loop() {
  //Serial.print("v: "); //use serial prints here to prevent conflicts with i2c and the interrupt service routine (see sendData())
  //Serial.println(value); //note that value will only update when an i2c request is made
  delay(100);
}


// callback for received data
void receiveData(int byteCount){
  int io;
  // no "int value" as it is a global so analog values that are read can be transmitted

  if (byteCount == 2) { // Write to a pin
    io = Wire.read();
    value = Wire.read();
    pinMode(io, OUTPUT);

    if (io > 128) { // If the io pin value has the bit 8 set, then it's an analogWrite request
      analogWrite((io - 128),value);

    } else {
      digitalWrite(io,value);

    }

  } else if (byteCount == 1) {  // Read from a pin
    io = Wire.read();
    pinMode(io, INPUT);

    if (io > 128) { // If the io pin value has the bit 8 set, then it's an analogRead request - you can digitalRead an analog pin except for A6 & A7 (20 & 21) which are analog only
      value = analogRead(io - 128);
      readCount = 0; // Override any current read count as the value has now changed - if the master hasn't read the two values, tough.

    } else {
      value = digitalRead(io);
      readCount = 1; // This will jump straight to returning the LSB as we are only going to be returning a 0 or a 1 - rather up to the other end to ask for just one byte.
    }
  }
}


// callback for sending data
void sendData(){
  //IMPORTANT:  Avoid using serial prints in this area as they interfere with the interrupt service routine, slow down the arduino, and can corrupt the value being sent. Use them in the loop() function if required. 
  
  // As I2C only does 7 bit data, we have to chop up a value, return two parts and reassemble at the other end. The 'other end' has to perform two reads as the 'other end' is a Pi running Python and SMBus library has no simple way of receiving a word from a slave without using a register, which isn't supported in the Arduino Wire library.
  int t = 0;
  if (readCount == 0) {
    t = value >> 8; // MSB
    readCount = 1; // Set flag to send second half on next call
  } else {
    t = value & 255; // LSB
    readCount = 0;
  }
  Wire.write(t);
}
