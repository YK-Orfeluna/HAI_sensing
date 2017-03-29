char HEAD = 'H';
int hr = 0;           //sensor-value(HR)
int gsr = 0;          //sensor-value(GSR)

const int LED = 13;      //LED

void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
}

void loop() {

  // 受信バッファに３バイト（ヘッダ＋int）以上のデータが着ているか確認
  if (Serial.available() >= sizeof(HEAD) + sizeof(int)) {
    // ヘッダの確認
    if(Serial.read() == HEAD){
      int low1 = Serial.read(); // 下位バイトの読み取り
      int high1 = Serial.read(); // 上位バイトの読み取り
      hr = makeWord(high1, low1); // 上位バイトと下位バイトを合体させてint型データを復元

      int low2 = Serial.read(); // 下位バイトの読み取り
      int high2 = Serial.read(); // 上位バイトの読み取り
      gsr = makeWord(high2, low2);
    }
  }

  delay(100);

}

