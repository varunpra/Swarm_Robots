/* Master Node of the Swarm */

// Including all the libraries

#include<Wire.h>
#include<SPI.h>
#include"nRF24L01.h"
#include"RF24.h"
#include <HMC5883L.h>

// Defining the Motor Pins on the Arduino

#define R1 4
#define R2 5
#define L1 2
#define L2 3

// Creating the NRF and HMC5883L Object

HMC5883L compass;
RF24 radio(7,8);

// Defining the Pipes for Communication on NRF
const uint64_t pipes[3]={0x00,0x01,0x02};

// Defining Variables

float Master_Heading[2];
int Slave1_Flag[2];
int Slave2_Flag[2];
int Slave1_Flag_To_Be[2];
int Slave2_Flag_To_Be[2];
float headingDegrees;

void setup(void) 
{
  Serial.begin(9600);
  
  // Defining the Motor Pins as OUTPUT
  
  pinMode(L1,OUTPUT);
  pinMode(L2,OUTPUT);
  pinMode(R1,OUTPUT);
  pinMode(R2,OUTPUT);
  radio.begin();
  radio.openWritingPipe(pipes[0]);
  radio.openReadingPipe(1,pipes[1]);
  radio.openReadingPipe(2,pipes[2]);
  radio.startListening();
  radio.stopListening();
  while (!compass.begin())
  {
    Serial.println("Could not find a valid HMC5883L sensor, check wiring!");
    delay(500);
  }
// Calibrating the Sensor Readings

// Set measurement range
  compass.setRange(HMC5883L_RANGE_1_3GA);
// Set measurement mode
  compass.setMeasurementMode(HMC5883L_CONTINOUS);
 // Set data rate
  compass.setDataRate(HMC5883L_DATARATE_30HZ);
// Set number of samples averaged
  compass.setSamples(HMC5883L_SAMPLES_8);
// Set calibration offset. See HMC5883L_calibration.ino
  compass.setOffset(88,62);
}

void loop()
{
  Vector norm = compass.readNormalize();
  // Calculate heading
  float heading = atan2(norm.YAxis, norm.XAxis);
  // Set declination angle on your location and fix heading
  // You can find your declination on: http://magnetic-declination.com/
  // (+) Positive or (-) for negative
  // For Bytom / Poland declination angle is 4'26E (positive)
  // Formula: (deg + (min / 60.0)) / (180 / M_PI);
  float declinationAngle = (-1 + (16.0 / 60.0)) / (180 / M_PI);
  heading += declinationAngle;
  // Correct for heading < 0deg and heading > 360deg
  if (heading < 0)
  {
    heading += 2 * PI;
  }
  if (heading > 2 * PI)
  {
    heading -= 2 * PI;
  }
  // Convert to degrees
  headingDegrees = heading * 180/M_PI; 
  // Output
  Serial.print(" Heading = ");
  Serial.print(heading);
  Serial.print(" Degress = ");
  Serial.print(headingDegrees);
  Serial.println();
  delay(100);
  Master_Heading[0]=headingDegrees;

  // Sending the Masters Heading To the Slaves through pipe 0x00
  radio.stopListening();
  radio.write(Master_Heading,sizeof(Master_Heading));

  // Now Waiting For a Flag From The Slaves
  radio.startListening();
  while(radio.available())
  {
    Serial.println("Lode");
  radio.startListening();
  radio.read(Slave1_Flag,sizeof(Slave1_Flag));
  radio.read(Slave2_Flag,sizeof(Slave2_Flag));
  Serial.println(Slave1_Flag[0]);
  Serial.println(Slave2_Flag[0]);
  }
 if(Slave1_Flag==Slave1_Flag_To_Be && Slave2_Flag == Slave2_Flag_To_Be)
 {
  Serial.println("YES");
 }
 else
 {
  Serial.println("NO");
 }
 delay(200);
}

void Right()
{
  digitalWrite(L2,LOW);
  digitalWrite(L1,HIGH);
  digitalWrite(R2,LOW);
  digitalWrite(R1,LOW);
  }
void Stop()
{
  digitalWrite(L2,LOW);
  digitalWrite(L1,LOW);
  digitalWrite(R1,LOW);
  digitalWrite(R2,LOW);
  }
void Left()
{
  digitalWrite(L2,LOW);
  digitalWrite(L1,LOW);
  digitalWrite(R2,HIGH);
  digitalWrite(R1,LOW);
  }
void Straight()
{
  digitalWrite(L2,LOW);
  digitalWrite(L1,HIGH);
  digitalWrite(R2,HIGH);
  digitalWrite(R1,LOW);
  }




