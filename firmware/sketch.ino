#include <WiFi.h>
#include <PubSubClient.h>
#include "DHTesp.h"

// --- IDENTITY PROPERTY ---
const char* CLIENT_ID = "ESP32_Cooling_Unit_001";
const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";
const char* MQTT_BROKER = "broker.hivemq.com";

// Topics
const char* TOPIC_PUB_TEMP = "telemetry/temp/001";
const char* TOPIC_PUB_FAN  = "telemetry/fan_status/001";
const char* TOPIC_SUB_CMD  = "commands/fan/001";

const int DHT_PIN = 15;
const int FAN_PIN = 2;

DHTesp dhtSensor;
WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++) { message += (char)payload[i]; }
  
  Serial.print("Command from DT: ");
  Serial.println(message);

  if (message == "ON") {
    digitalWrite(FAN_PIN, HIGH);
  } else if (message == "OFF") {
    digitalWrite(FAN_PIN, LOW);
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(FAN_PIN, OUTPUT);
  dhtSensor.setup(DHT_PIN, DHTesp::DHT22);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }

  client.setServer(MQTT_BROKER, 1883);
  client.setCallback(callback);
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect(CLIENT_ID)) {
      client.subscribe(TOPIC_SUB_CMD);
    } else {
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  TempAndHumidity data = dhtSensor.getTempAndHumidity();
  float t = data.temperature;

  if (!isnan(t)) {
    // --- REFLECTION ---
    // Update the Digital Twin on both temperature and actual actuator state
    client.publish(TOPIC_PUB_TEMP, String(t).c_str());
    client.publish(TOPIC_PUB_FAN, digitalRead(FAN_PIN) == HIGH ? "ON" : "OFF");

    Serial.println("Temp: " + String(t) + "°C");
  }

  delay(2000); 
}