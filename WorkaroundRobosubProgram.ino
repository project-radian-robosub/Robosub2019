#include <MS5837.h>
#include <PID_v1.h>
#include<Servo.h>
#include <Wire.h>

MS5837 sensor;

int photoresistorpin = A0;
int photoresistorvalue = 0;

int m_pow[6] = {0, 0, 0, 0, 0, 0};
int p_pow[6] = {0, 0, 0, 0, 0, 0};
int motor_vals[6] = {0, 0, 0, 0, 0, 0};

Servo m2;
Servo m3;
Servo m4;
Servo m5;
Servo m6;
Servo m7;

char c;
String values = "";

int resetPin = 22;

double Setpoint, Input, Output;

double Kp = 2.5;
double Ki = 0;
double Kd = 1.5;

PID depthPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

void setup() {
  digitalWrite(resetPin, HIGH);
  delay(200);
  pinMode(resetPin, OUTPUT);
  
  Serial.begin(9600);
  Wire.begin();
  
  while (analogRead(photoresistorpin) < 290) {
    
  }

  sensor.read();

  Setpoint = 1085;
  Input = sensor.pressure();

  depthPID.SetMode(AUTOMATIC);

  m2.attach(2);
  m3.attach(3);
  m4.attach(4);
  m5.attach(5);
  m6.attach(6);
  m7.attach(7);

  stopAll();

  delay(7500);

  while (!sensor.init()) {
    Serial.println("Pressure init failed!");
    delay(2000);
  }

  sensor.setModel(MS5837::MS5837_30BA);
  sensor.setFluidDensity(997); // kg/m^3 (freshwater, 1029 for seawater)

  sendReady();

}


void loop() {
  
  if(Serial.available() > 0) {
    
    c = Serial.read();
    values += c;

    if(values.length() == 18) {

      updateMove(values);
      values = "";
      
    }
    
  }
  
  sensor.read();

  Input = sensor.pressure();
  depthPID.Compute();
  updatePressure(-Output);
  setMotors();

  if(analogRead(photoresistorpin) < 290) {
    Serial.write("1");
    delay(100);
    digitalWrite(resetPin, LOW);
    delay(100);
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


void updateMove(String values) { //length must be 18

  m_pow[0] = values.substring(0,3).toInt();
  m_pow[1] = values.substring(3,6).toInt();
  m_pow[2] = values.substring(6,9).toInt();
  m_pow[3] = values.substring(9,12).toInt();
  m_pow[4] = values.substring(12,15).toInt();
  m_pow[5] = values.substring(15).toInt();
  
}

void updatePressure(double p_power) { 

  if(p_power > 60) {
    p_power = 60;
  }
  if(p_power < -60) {
    p_power = -60;
  }
  p_pow[2] = map(p_power, -100, 100, 0, 100);
  p_pow[3] = map(p_power, -100, 100, 0, 100);
  
}

void setMotors() { 

  for(int i; i < sizeof(motor_vals); i++) {
    motor_vals[i] = 50;
  }
  for(int i; i < sizeof(motor_vals); i++) {
    motor_vals[i] += p_pow[i] - 50;
    motor_vals[i] += m_pow[i] - 50;
  }

  int max_val = 50;

  for(int i; i < sizeof(motor_vals); i++) {
    if(abs(motor_vals[i] - 50) > abs(max_val - 50)) {
      max_val = motor_vals[i];
    }
  }

  if(abs(max_val - 50) > 50) {
    for(int i; i < sizeof(motor_vals); i++) {
      motor_vals[i] = map(motor_vals[i] - 50, -abs(max_val - 50), abs(max_val - 50), -50, 50);
      motor_vals[i] += 50;
    }
  }

  motor_vals[3] = motor_vals[3] - (2 * (motor_vals[3] - 50));

  m2.writeMicroseconds(map(motor_vals[0], 0, 100, 1100, 1900));
  m3.writeMicroseconds(map(motor_vals[0], 0, 100, 1100, 1900));
  m4.writeMicroseconds(map(motor_vals[0], 0, 100, 1100, 1900));
  m5.writeMicroseconds(map(motor_vals[0], 0, 100, 1100, 1900));
  m6.writeMicroseconds(map(motor_vals[0], 0, 100, 1100, 1900));
  m7.writeMicroseconds(map(motor_vals[0], 0, 100, 1100, 1900));
}
