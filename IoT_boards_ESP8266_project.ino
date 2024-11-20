#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

const char *ssid = "hash test";
const char *password = "idontknow";

const char *apiToken = "akmyaxupfz613o3zecoq2o1r2fc5tn";
const char *userToken = "uhx86xxfyz8hav3x8eqbjpxbpdb1cm";

// Pushover API endpoint
const char *pushoverApiEndpoint = "https://api.pushover.net/1/messages.json";

const int MQ135pin = D7;
const int alert = D8;
const int stpBtn = D6;
int wait = 3;

struct tm *timeinfo;

void setup()
{
  Serial.begin(9600);
  pinMode(MQ135pin, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(alert, OUTPUT);
  pinMode(stpBtn, INPUT_PULLUP);

  digitalWrite(LED_BUILTIN, 0);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("\nConnecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print('.');
    delay(1000);
  }
  Serial.println("\nConnected.");
  WiFi.setAutoReconnect(true);
  WiFi.persistent(true);

  // Set time via NTP, as required for x.509 validation
  configTime(5 * 3600, 1800, "pool.ntp.org", "time.nist.gov");
  Serial.print("Waiting for NTP time sync...");
  time_t now = time(nullptr);
  while (now < 1510592825)
  {
    delay(500);
    Serial.print('.');
    now = time(nullptr);
  }
  timeinfo = localtime(&now);
  Serial.print("\nCurrent time: ");
  Serial.print(asctime(timeinfo));
  digitalWrite(LED_BUILTIN, 1);
  tone(alert,500);
  delay(200);
  tone(alert,1000);
  delay(500);
  noTone(alert);
}

void loop()
{
  if (WiFi.status() != WL_CONNECTED)
    ESP.restart();
  if (digitalRead(MQ135pin))
    return;

  digitalWrite(LED_BUILTIN, 0);y
  while (digitalRead(stpBtn))
  {
    for (int freq = 500; freq < 1000; freq += 10)
    {
      tone(alert, freq);
      delay(10);
    }
    for (int freq = 1000; freq > 500; freq -= 10)
    {
      tone(alert, freq);
      delay(10);
    }
  }
  noTone(alert);
  digitalWrite(LED_BUILTIN, 1);
}
