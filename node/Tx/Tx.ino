/*********
  Modified from the examples of the Arduino LoRa library
  More resources: https://randomnerdtutorials.com
*********/
#include <SPI.h>
#include <LoRa.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>

//define the pins used by the transceiver module
#define ss 5
#define rst 14
#define dio0 2

#define RX_PIN 17
#define TX_PIN 16
TinyGPSPlus gps;

int counter = 0;
bool gpsConnected = false; // Flag to track GPS connection status

void setup() {
  //initialize Serial Monitor
  Serial.begin(115200);
  while (!Serial);
  Serial.println("LoRa Sender");
  
  // GPS serial con
  Serial2.begin(9600);

  delay(3000);
  
  //setup LoRa transceiver module
  LoRa.setPins(ss, rst, dio0);
  
  //replace the LoRa.begin(---E-) argument with your location's frequency 
  //433E6 for Asia
  //866E6 for Europe
  //915E6 for North America
  while (!LoRa.begin(866E6)) {
    Serial.println(".");
    delay(500);
  }
   // Change sync word (0xF3) to match the receiver
  // The sync word assures you don't get LoRa messages from other LoRa transceivers
  // ranges from 0-0xFF
  LoRa.setSyncWord(0xF3);
  Serial.println("LoRa Initializing OK!");

  while (!gpsConnected) {
    if (Serial2.available() > 0) {
      if (gps.encode(Serial2.read())) {
        if (gps.location.isValid()) {
          gpsConnected = true; 
          Serial.println("GPS connected");
        }
      }
    }
  }
}

void loop() {
  while (Serial2.available() > 0) {
    gps.encode(Serial2.read());
  }

  if (gps.location.isValid()) {

    Serial.print("Latitude: ");
    Serial.println(gps.location.lat(), 6);
    Serial.print("Longitude: ");
    Serial.println(gps.location.lng(), 6);

    LoRa.beginPacket();
    LoRa.print("Lat: ");
    LoRa.print(gps.location.lat(), 6);
    LoRa.print(", Lng: ");
    LoRa.print(gps.location.lng(), 6);
    LoRa.print(", Counter: ");
    LoRa.print(counter);
    LoRa.endPacket();
  } else {
    Serial.println("Invalid GPS data");
    LoRa.beginPacket();
    LoRa.print("GPS unavailable ");
    LoRa.print(counter);
    LoRa.endPacket();
  }

  counter++;

  delay(1000);
}