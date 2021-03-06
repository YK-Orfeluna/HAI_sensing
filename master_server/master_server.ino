#include <Wire.h>
const byte H = 'H';
const byte G = 'G';

//IP: 192, 168, 11, 10

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char* ssid = "0024A5B57EBC";
const char* password = "mxte5ttdejm8s";

ESP8266WebServer server(80);

const int LED = 13;
const char CNM = ',';

int hr = 0;
int gsr = 0;
const int THREAD = 500;

String hr_s, gsr_s;

void handleRoot() {
  server.send(200, "text/plain", "sensorvalue=" + hr_s + CNM + gsr_s);

}

void handleNotFound() {
  digitalWrite(LED, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  digitalWrite(LED_BUILTIN, 0);
}

void setup(void) {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  WiFi.config(IPAddress(192, 168, 11, 10), WiFi.gatewayIP(), WiFi.subnetMask());
  //http://ashiyu.cocolog-nifty.com/blog/2015/08/indexhtml-8dfa.html

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);

  server.on("/inline", []() {
    server.send(200, "text/plain", "this works as well");
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  // 受信バッファに３バイト（ヘッダ＋int）以上のデータが着ているか確認
  Wire.requestFrom(8, 6);
  if (Wire.available() > 0) {
    if (Wire.read() == H) {
      int low1 = Wire.read();
      int high1 = Wire.read();
      hr = makeWord(high1, low1);
      hr_s = String(hr, DEC);
      Serial.print("HR = ");
      Serial.println(hr);

      if (hr > THREAD) {
        digitalWrite(LED_BUILTIN, HIGH);
      }
      else {
        digitalWrite(LED_BUILTIN, LOW);
      }
    }
    if (Wire.read() == G) {
      int low2 = Wire.read();
      int high2 = Wire.read();
      gsr = makeWord(high2, low2);
      gsr_s = String(gsr, DEC);
      Serial.print("GSR = ");
      Serial.println(gsr);
    }
  }
  server.handleClient();
}
