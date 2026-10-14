#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

#define DHT_PIN 4
#define DHT_TYPE DHT22
#define SOIL_MOISTURE_PIN 34

const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";
const char* BACKEND_URL = "http://YOUR_PC_IP:8000/api/soil/read";
const char* DEVICE_ID = "ESP32-KRUSHIAI-01";
const int FARMER_ID = 1;

// Configure RS485 pins and Modbus registers only after confirming the exact NPK sensor datasheet.
#define RS485_RX 16
#define RS485_TX 17
#define RS485_DE_RE 4

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.reconnect();
    delay(3000);
    return;
  }

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  int rawMoisture = analogRead(SOIL_MOISTURE_PIN);
  float moisture = map(rawMoisture, 4095, 0, 0, 100);

  // Replace these placeholders only after the exact NPK Modbus register map is confirmed.
  float nitrogen = 0;
  float phosphorus = 0;
  float potassium = 0;

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("DHT reading unavailable");
    delay(5000);
    return;
  }

  StaticJsonDocument<512> doc;
  doc["device_id"] = DEVICE_ID;
  doc["farmer_id"] = FARMER_ID;
  doc["nitrogen"] = nitrogen;
  doc["phosphorus"] = phosphorus;
  doc["potassium"] = potassium;
  doc["soil_moisture"] = moisture;
  doc["air_temperature"] = temperature;
  doc["humidity"] = humidity;

  String payload;
  serializeJson(doc, payload);

  HTTPClient http;
  http.begin(BACKEND_URL);
  http.addHeader("Content-Type", "application/json");
  int response = http.POST(payload);
  Serial.printf("HTTP response: %d\n", response);
  http.end();

  delay(10000);
}
