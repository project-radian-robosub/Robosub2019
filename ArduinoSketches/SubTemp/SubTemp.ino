/* Ryan Hays 072519
 * Project Radian Robosub 
 * Temp check for Jetson Nano/ Main Tray
 * LM 35 Sensor
 */
int tempPin = A1;

void setup() {
  Serial.begin(9600);
  delay(1000);
  Serial.println("Wonder Twin Powers...Activate!");
  Serial.println("Initializing...");
  delay(2000);
}

void loop() {
  int value;
  float tempC;
  float tempF;

  value = analogRead(tempPin);
  
  tempC = float(value) /1023;
  tempC = tempC * 500;

  tempF = tempC * 1.8 + 32;

  Serial.print("  Main Temp:  ");
  Serial.print(tempC);
  Serial.print(" C   ");
  Serial.print(tempF);
  Serial.println(" F");

  delay(1000);

}
