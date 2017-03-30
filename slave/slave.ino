const int HR = 1;        //Analog-pin(HR)
const int GSR = 3;       //Analog-pin(GSR)
const int LED = 13;

int hr = 0;         //sensor-value(HR)
int gsr = 0;        //sensor-value(GSR)

const char* HEAD = "H";

void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
}

void loop() {
  hr = analogRead(HR);
  gsr = analogRead(GSR);

  sendIntData(hr, gsr); // int型データの送信

  delay(100);

}

// int型のデータを送信する関数
void sendIntData(int value1, int value2) {
  Serial.write(HEAD); // ヘッダの送信
  Serial.write(lowByte(value1)); // 下位バイトの送信
  Serial.write(highByte(value1)); // 上位バイトの送信
  Serial.write(lowByte(value2)); // 下位バイトの送信
  Serial.write(highByte(value2)); // 上位バイトの送信
}

