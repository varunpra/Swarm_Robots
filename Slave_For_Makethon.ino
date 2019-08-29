/*
  HMC5883L Triple Axis Digital Compass. Compass Example.
  Read more: http://www.jarzebski.pl/arduino/czujniki-i-sensory/3-osiowy-magnetometr-hmc5883l.html
  GIT: https://github.com/jarzebski/Arduino-HMC5883L
  Web: http://www.jarzebski.pl
  (c) 2014 by Korneliusz Jarzebski
*/

#include <Wire.h>
//#include <HMC5883L.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>
//HMC5883L compass;
#include<SPI.h>
#include"nRF24L01.h"
#include"RF24.h"
#define R1 4
#define R2 5
#define L1 2
#define L2 3
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);
float Kp=10;
float Ki=0;
float Kd=0.1;

int diff;
int th=35;
float master_mod;
float slave_mod;
RF24 radio(9,10);
const uint64_t pipes[2]={0x00,0x02};
float upper_limit;
float lower_limit;
float master_angle;
float dia;
float R[2];
float A[2];



void setup()
{
  Serial.begin(9600);
pinMode(L1,OUTPUT);
pinMode(L2,OUTPUT);
pinMode(R1,OUTPUT);
pinMode(R2,OUTPUT);
    radio.begin();
  radio.openWritingPipe(pipes[1]);
  radio.openReadingPipe(1,pipes[0]);
  radio.startListening();

}

void loop()
{


  sensors_event_t event; 
  mag.getEvent(&event);

  // Calculate heading
  float heading = atan2(event.magnetic.y, event.magnetic.x);

   float declinationAngle = 0.017;
  heading += declinationAngle;
  
  // Correct for when signs are reversed.
  if(heading < 0)
    heading += 2*PI;
    
  // Check for wrap due to addition of declination.
  if(heading > 2*PI)
    heading -= 2*PI;
   
  // Convert radians to degrees for readability.
  float hd = heading * 180/M_PI; 
  Serial.println("angl_slave");
  Serial.println(hd);
  if(hd>180)
  {
    slave_mod=hd-360;
       Serial.println("Slave mod");
   Serial.println(slave_mod);
  } 
  else
  {
    slave_mod=hd;
  Serial.println("Slave mod");
   Serial.println(slave_mod);
    }
  
  while(radio.available())
 {
   radio.startListening();
   radio.read(A,sizeof(A));
   Serial.println(A[0]);
  master_angle=A[0];
  if(A[0]>180)
  {
    master_mod=A[0]-360;
   }
   else
   {
    master_mod=A[0];
    }
   Serial.println("  A ultra  ");
   Serial.println("master_mod:");
   Serial.println(master_mod);
   }
 if(master_angle<360&&master_angle>360-th)
  {
    upper_limit=master_angle-360+th;
    lower_limit=master_angle-th;
    }
    else if(master_angle>0&&master_angle<th)
    {
      upper_limit=master_angle+th;
      lower_limit=master_angle+360-th;
      }
      else
      {
  upper_limit=master_angle+th;
  lower_limit=master_angle-th;}
  Serial.println("Upper_limit");
  Serial.println(upper_limit);
  Serial.println("Lower Limit");
  Serial.println(lower_limit);
 
 if(master_angle<360&&master_angle>180)
 {Serial.println("Entered condition 1 of loop 1");
 float master=master_angle;
 float dia=master-180;
 if(hd<master&&hd>dia)
 {
     diff=mod(master_mod-slave_mod);
     diff=map(diff,0,180,500,1023);
        Serial.println("Diff");
        Serial.println(Kp*diff);
  left();
  Serial.println("Left");
  Serial.println(mod(master_mod-slave_mod));
 }
  else if(hd<upper_limit&&hd>lower_limit)
  {
    s();
    Serial.println("Stop");
  R[0]=1;
  radio.stopListening();
  radio.write(R,sizeof(R));
  radio.startListening();
  }
    else
    {
         diff=mod(master_mod-slave_mod);
             diff=map(diff,0,180,500,1023);
        Serial.println("Diff");
        Serial.println(Kp*diff);
      right();
      Serial.println("Right");
      Serial.println(mod(master_mod-slave_mod));}
      
    }
    else if(master_angle>0&&master_angle<180)
    {
      //Serial.println("Entered loop 1 of condition 2");
      float master=master_angle;
      float dia=master_angle+180;
      if(hd>master&&hd<dia)
      {
         diff=mod(master_mod-slave_mod);
             diff=map(diff,0,180,500,1023);
        Serial.println("Diff");
        Serial.println(Kp*diff);
        right();
        Serial.println("Right");
        Serial.println(mod(master_mod-slave_mod));
        }
        else if(hd<upper_limit&&hd>lower_limit)
        {
             s();
             Serial.println("Stop");
  R[0]=1;
  radio.stopListening();
  radio.write(R,sizeof(R));
  radio.startListening();
          }
          else
          {
              diff=mod(master_mod-slave_mod);
                  diff=map(diff,0,180,500,1023);
        Serial.println("Diff");
        Serial.println(Kp*diff);
            left();
            Serial.println("Left");
            Serial.println(mod(master_mod-slave_mod));
          
      }}
    
 
  
  // Output
  Serial.print(" Heading = ");
  Serial.print(heading);
  Serial.print(" Degress = ");
  Serial.print(hd);
  Serial.println();

  delay(100);
}
void right()
{
Serial.println("Entered the function right");
  digitalWrite(L2,LOW);
  digitalWrite(L1,HIGH);
  digitalWrite(R2,LOW);
  digitalWrite(R1,LOW);
  }
void s()
{
  digitalWrite(L2,LOW);
  digitalWrite(L1,LOW);
  digitalWrite(R1,LOW);
  digitalWrite(R2,LOW);
  }
void left()
{
    Serial.println("Entered the function left");

  digitalWrite(L2,HIGH);
  digitalWrite(L1,LOW);
  digitalWrite(R2,LOW);
  digitalWrite(R1,LOW);
 }
  float mod(float a)
  {
    if(a<0)
    {
      return(-1*a);
      }
      else
      {
        return(a);
        }
    }
