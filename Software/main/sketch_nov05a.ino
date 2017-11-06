#include<SPI.h>
#include<SD.h>
#include<Wire.h>
#include "RTClib.h"

const int sensorPin = 0;        // Sensor signal connected to A0
const int dataFrequency = 3;    // How many times the sensor is read within 1 second
const int sdChipSelect = 10;     // SD shield uses digital pin 10
const int baudRate = 9600;       // baud rate of serial communication

unsigned long lastSampleTime;

static String fileName;

RTC_DS1307 rtc;                 // Initialize the real time clock object

void setup() {
  // put your setup code here, to run once:
  //DateTime now = rtc.now();
  
  setupSerial();
  //fileName = String(now.year())+ "_" + String(now.month()) + "_" + String(now.day()) + "_" + String(now.hour()) + "_" + String(now.minute()) + "_" + String(now.second()) + ".txt";
  setupSD("Test1.txt");
  lastSampleTime = 0UL;
  
}

void loop() {
  // put your main code here, to run repeatedly:

  unsigned long nowMillis = millis();
  String dataString = "";
  float pressure;
  //DateTime now = rtc.now();
  //Serial.println(now.year(),DEC);
  if ((nowMillis - lastSampleTime) > 1000/dataFrequency)
  {
    pressure = readPressureKPa(sensorPin);
    lastSampleTime = nowMillis;
    dataString = String(pressure) + " KPa now: " + String(nowMillis);
    File dataFile = SD.open("Test1.txt", FILE_WRITE);
    if (dataFile)
    {
      dataFile.println(dataString);
      dataFile.close();
      Serial.println(dataString);
    }
    else
    {
      Serial.println("error opening file");
    }
  }
}

/*------------------Pressure Reading----------------------------------------*/
float readPressureMPa(int pinNumber)
{
  const float rawVoltageMin = 0.5;  // Sensor output voltage lower limit (volt)
  const float rawVoltageMax = 4.5;  // Sensor output voltage upper limit (volt)
  
  int rawValue = analogRead(pinNumber);   // Read raw value in the range of 0 - 1023
  float rawVoltage = rawValue * ((rawVoltageMax-rawVoltageMin)/1023.0) + rawVoltageMin; // Convert to voltage
  float pressure = (rawVoltage - rawVoltageMin) / (rawVoltageMax - rawVoltageMin); // Pressure unit MPa

  return pressure;  // MPa
}

float readPressureKPa(int pinNumber)
{
  return 1000 * readPressureMPa(pinNumber);
}
/*-------------------------------------------------------------------------*/

/*----------------------------------------SD Card--------------------------*/
void setupSD(String fileName)
{
  Serial.print("Initializing SD card...");
  if (!SD.begin(sdChipSelect))
  {
    Serial.println("Initialization failed!");
    return;
  }
  Serial.println("Initialization done.");

  if (SD.exists(fileName))
  {
    Serial.print(fileName);
    Serial.println(" exists.");
  }
  else
  {
    Serial.print(fileName);
    Serial.print(" does not exist. creating ");
    Serial.println(fileName);
    File dataFile;
    dataFile = SD.open(fileName, FILE_WRITE);
    dataFile.close();
    
    if (SD.exists(fileName))
    {
    Serial.println("File created succesfully");
    }
    else 
    {
    Serial.println("File creation failed.");
    }
  }
}

void setupSerial()
{
  Serial.begin(baudRate);
  while(!Serial)
  {
    ; // wait for serial port to connect.
  }
}
/*------------------------------------------------------------------------*/

