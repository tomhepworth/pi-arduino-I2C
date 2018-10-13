#include <Wire.h> 

#define SLAVE_ADDRESS 0x20
int value = 0;
int aOrD = 0;

void setup() {
  pinMode(13, OUTPUT);

  pinMode(A4, INPUT_PULLUP);
  pinMode(A5, INPUT_PULLUP);

  Serial.begin(57600); // start serial for output
  
  // initialize I2C as slave
  Wire.begin(SLAVE_ADDRESS);
  // define callbacks for I2C communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  Serial.println("Ready!");
}

void loop() {
  delay(100);
}

// callback for received data
void receiveData(int byteCount){
  int io;
  // value is a global so analog values that are read can be transmitted
  if(byteCount == 2){
    Serial.println("BC = 2");
    io = Wire.read();
    value = Wire.read();

    pinMode(io, OUTPUT);
    if(io > 128){
      analogWrite((io - 128),value);
    }else{
      digitalWrite(io,value);
    }
    
  } else if (byteCount == 1) {  // DIGITAL/ANALOG READ
    Serial.println("BC = 1");
    io = Wire.read();

    pinMode(io, INPUT);
    if(io > 128){
      analogRead(io - 128);
    }else{
      digitalRead(io);
    }
    
  } else { //READ WIRE
  io = Wire.read();
  // As I2C only does 7 bit data, we have to reassemble the two parts in to one value that the other end chopped up when it sent it
    value  = Wire.read() << 8; 
    value |= Wire.read(); 
  }  

  /*if ((io >= 2) && (io <= 13)) {
    pinMode(io, OUTPUT);

    // Servos on 3, 5, 6, 9, 10, and 11. Note, 3 is also INT1
    digitalWrite(io, value);
    Serial.print(", writing: ");
    Serial.println(value);
  }

  if ((io >= 14) && (io <= 17)) {
    pinMode(io, INPUT);
    value = analogRead(io); 
    Serial.print(", reading: ");
    Serial.println(value); 
  }
  if ((io >= 20) && (io <= 21)) {
    pinMode(io, INPUT);
    value = analogRead(io);
    Serial.print(", reading: ");
    Serial.println(value); 
  }*/


}

// callback for sending data
void sendData(){
  // As I2C only does 7 bit data, we have to chop up a value, return two parts and reassemble at the other end
  Wire.write(value >> 8);
  Wire.write(value & 255);
}


