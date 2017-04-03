const int HR = 1;        //Analog-pin(HR)
const int GSR = 4;       //Analog-pin(GSR)
const int LED = 13;

const int THREAD = 500 ;

int hr = 0;         //sensor-value(HR)
int gsr = 0;        //sensor-value(GSR)

const char HEAD = 'H';
const char FOOT = 'F';

void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
}

void loop() {
  hr = analogRead(HR);
  if(hr > THREAD){
    digitalWrite(LED, HIGH);
  }
  else{
    digitalWrite(LED, LOW);
  }
  gsr = analogRead(GSR);

  sendIntData(hr, gsr); // int型データの送信
  //Serial.print(hr);
  //Serial.print(" ,");
  //Serial.println(gsr);

  delay(10);

}

// int型のデータを送信する関数
void sendIntData(int value1, int value2) {
  Serial.write(HEAD); // ヘッダの送信
  Serial.write(lowByte(value1)); // 下位バイトの送信
  Serial.write(highByte(value1)); // 上位バイトの送信
  Serial.write(FOOT);
  Serial.write(lowByte(value2)); // 下位バイトの送信
  Serial.write(highByte(value2)); // 上位バイトの送信
}

