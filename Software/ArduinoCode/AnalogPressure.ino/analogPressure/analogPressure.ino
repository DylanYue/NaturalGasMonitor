/* 
 * This code reads pressure value from an analog pressure transducer
 * Author: Dingjun Yue
 * Email: dingjun.yue@gmail.com
 */

// Analog pressure sensor is connected to A0
int analogPressureSensor = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println(readPressure(analogPressureSensor));
}

float readPressure(int analogPin) {
  // Read raw value in the range of 0 - 1023
  int rawValue = analogRead(analogPin);
  // Convert to voltage, range: 0.5v - 4.5v
  float voltage = rawValue * (4.0/1023.0) + 0.5;
  // Convert to MPa, range: 0 - 1 MPa
  float pressure = (voltage - 0.5) / 4.0;
  
  return pressure;
}

