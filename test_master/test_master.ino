#include <Wire.h>
int hr = 0;
int gsr = 0;

byte H = 'H';
byte G = 'G';

void setup() {
  Serial.begin(9600);
  Wire.begin();
}

void loop() {
  Wire.requestFrom(8, 6);
  if (Wire.available() > 0) {
    if (Wire.read() == H) {
      int low1 = Wire.read();
      int high1 = Wire.read();
      hr = makeWord(high1, low1);
      Serial.print("HR = ");
      Serial.println(hr);
    }
    if (Wire.read() == G) {
      byte low2 = Wire.read();
      byte high2 = Wire.read();
      gsr = makeWord(high2, low2);
      Serial.print("GSR = ");
      Serial.println(gsr);
    }


  }
}
