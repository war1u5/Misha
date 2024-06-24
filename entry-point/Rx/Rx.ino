#include <SPI.h>
#include <LoRa.h>

// Define the pins used by the transceiver module
#define ss D8
#define rst D0
#define dio0 D2

#define VALID_PACKET_IDENTIFIER 0x01

int packetCounter = 0;

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);
  while (!Serial);

  delay(3000);

  // Setup LoRa transceiver module
  LoRa.setPins(ss, rst, dio0);

  // Replace the LoRa.begin(---E-) argument with your location's frequency
  // 433E6 for Asia
  // 866E6 for Europe
  // 915E6 for North America
  while (!LoRa.begin(866E6)) {
    delay(500);
  }

  // Change sync word (0xF3) to match the transmitter
  LoRa.setSyncWord(0xF3);

  // Configure LoRa settings to match the transmitter
  LoRa.setSpreadingFactor(12);  // Spreading factor 7
  LoRa.setSignalBandwidth(125E3);  // Bandwidth 500 kHz
  LoRa.setCodingRate4(5);  // Coding rate 4/5

  Serial.println("LoRa Initializing OK!");
}

void loop() {
  // Try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // Read and print the entire packet
    while (LoRa.available()) {
      String LoRaData = LoRa.readString();
      Serial.print(LoRaData); 
    }
  }
}