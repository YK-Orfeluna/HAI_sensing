#include <Wire.h>

const int HR = 1;        //Analog-pin(HR)
const int GSR = 3;       //Analog-pin(GSR)
const int LED = 13;

const int THREAD = 500 ;

int hr = 0;         //sensor-value(HR)
int gsr = 0;        //sensor-value(GSR)

const byte H = 'H';
const byte G = 'G';
byte hr1 = 0;
byte hr2 = 0;
byte gsr1 = 0;
byte gsr2 = 0;

void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  Wire.begin(8);
  Wire.onRequest(sendByte);
}

void loop() {
  hr = analogRead(HR);
  gsr = analogRead(GSR);
  if(hr > THREAD){
    digitalWrite(LED, HIGH);
  }
  else{
    digitalWrite(LED, LOW);
  }

  delay(10);
}

void sendByte(){
  hr1 = lowByte(hr);
  hr2 = highByte(hr);
  gsr1 = lowByte(gsr);
  gsr2 = highByte(gsr);

  byte arr[6] = {H, hr1, hr2, G, gsr1, gsr2};
  Wire.write(arr, 6);
}

