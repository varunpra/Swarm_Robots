#include<SPI.h>
#include"nRF24L01.h"
#include"RF24.h"

float angle;
float master[16]={1,2,3,4,60,6,7,8,9,10,11,12,13,14,15,60};
float slave1[1];
float slave2[2];
float slave3[2];
float slave4[2];
int temp;

RF24 radio(9,10);
const uint64_t pipes[5]={0x00,0x01,0x02,0x03,0x04};

void setup(void) 
{
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(pipes[0]);
  radio.openReadingPipe(1,pipes[1]);
  radio.openReadingPipe(2,pipes[2]);
  radio.openReadingPipe(3,pipes[3]);
  radio.openReadingPipe(4,pipes[4]);
  radio.startListening();
  radio.stopListening();

  

  
}

void loop()
{
 
  radio.stopListening();
  radio.write(master,sizeof(master));
  
  radio.startListening();
  while(radio.available())
  {
    radio.startListening();
    radio.read(slave1,sizeof(slave1));
    radio.read(slave2,sizeof(slave2));
    radio.read(slave3,sizeof(slave3));
    radio.read(slave4,sizeof(slave4));
    
 Serial.println("  Slave Readings  "); 
 Serial.println(slave1[0]);
 Serial.println(slave2[0]);
 Serial.println(slave3[0]);
 Serial.println(slave4[0]);
 }
 if(slave1[0]==2 && slave2[0]==3 && slave3[0]==4 && slave4[0]==5)
 {
  Serial.println("YES");
 }
 else
 {
  Serial.println("NO");
 }
 
 delay(200);
}



