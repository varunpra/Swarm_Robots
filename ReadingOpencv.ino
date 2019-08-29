
#include<SPI.h>
#include"nRF24L01.h"
#include"RF24.h"
int coordinate[6];
RF24 radio(9,10);const uint64_t pipes=0x00;
void setup(){
    Serial.begin(9600);
    radio.begin();
  radio.openWritingPipe(pipes);
   radio.startListening();
  radio.stopListening();
    
}
void loop(){
    /*String first  = Serial.readStringUntil(',');
    Serial.read(); //next character is comma, so skip it using this
    String second = Serial.readStringUntil(',');
    Serial.read();
    String third  = Serial.readStringUntil('\0');
    Serial.println(first);
    Serial.println(second);
    Serial.println(third);
    //parse your data here. example:
    //double x = Double.parseDouble(first);*/
    while(Serial.available())
    {
    String first  = Serial.readStringUntil(',');
    coordinate[0]=first.toInt();
    Serial.read(); //next character is comma, so skip it using this
    String second = Serial.readStringUntil(',');
    coordinate[1]=second.toInt();
    Serial.read();
    String third  = Serial.readStringUntil(',');
    coordinate[2]=third.toInt();
    Serial.read();
    String fourth = Serial.readStringUntil(',');
    coordinate[3]=fourth.toInt();
    Serial.read();
    String fifth = Serial.readStringUntil(',');
    coordinate[4]=fifth.toInt();
    Serial.read();
    String sixth = Serial.readStringUntil('%');
    coordinate[5]=(sixth.toInt());
    for(int i=0;i<6;i++){
    Serial.print(coordinate[i]);
    Serial.print(",");
    
      }
      Serial.println("");
      radio.stopListening();
  radio.write(coordinate,sizeof(coordinate));
    }
    
    }
    
