#include<Servo.h>

int photoresistorpin = A0;
int photoresistorvalue = 0;

Servo m2;
Servo m3;
Servo m4;
Servo m5;
Servo m6;
Servo m7;

char c;
String values = "";


void setup() {
  
  Serial.begin(9600);

  while (analogRead(photoresistorpin) < 323) {
    
  }

  m2.attach(2);
  m3.attach(3);
  m4.attach(4);
  m5.attach(5);
  m6.attach(6);
  m7.attach(7);

  stopAll();

  delay(7500);

  sendReady();

}


void loop() {

  if(Serial.available() > 0) {
    
    c = Serial.read();
    values += c;

    if(values.length() == 18) {

      updateMotors(values);
      values = "";
      
    }
    
  }
  
}


void sendReady() {
  
  Serial.write("ready");
  
}

void stopAll() {

  m2.writeMicroseconds(1500);
  m3.writeMicroseconds(1500);
  m4.writeMicroseconds(1500);
  m5.writeMicroseconds(1500);
  m6.writeMicroseconds(1500);
  m7.writeMicroseconds(1500);

}


void updateMotors(String values) { //length must be 18

  m2.writeMicroseconds(map(values.substring(0,3).toInt(), 0, 100, 1100, 1900));
  m3.writeMicroseconds(map(values.substring(3,6).toInt(), 0, 100, 1100, 1900));
  m4.writeMicroseconds(map(values.substring(6,9).toInt(), 0, 100, 1100, 1900));
  m5.writeMicroseconds(map(values.substring(9,12).toInt(), 0, 100, 1100, 1900));
  m6.writeMicroseconds(map(values.substring(12,15).toInt(), 0, 100, 1100, 1900));
  m7.writeMicroseconds(map(values.substring(15).toInt(), 0, 100, 1100, 1900));
  
}
