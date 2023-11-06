#include <TinyGPS++.h> // library for GPS module
#include <SoftwareSerial.h>

TinyGPSPlus gps;
SoftwareSerial SerialGPS(1, 3); 

float Latitude , Longitude;
int year , month , date, hour , minute , second;
String DateString , TimeString , LatitudeString , LongitudeString;

bool gpsConnected = false; // Flag to track GPS connection status

void setup()
{
  Serial.begin(9600);
  SerialGPS.begin(9600);
  Serial.println();
  Serial.print("Connecting to GPS");
  
  // Wait until GPS module is connected
  while (!gpsConnected) {
    if (SerialGPS.available() > 0) {
      if (gps.encode(SerialGPS.read())) {
        if (gps.location.isValid()) {
          gpsConnected = true; // Set the flag to true when GPS is connected
        }
      }
    }
  }
  
  Serial.println("GPS connected");
}

void loop()
{
  while (SerialGPS.available() > 0)
    if (gps.encode(SerialGPS.read()))
    {
      if (gps.location.isValid())
      {
        Latitude = gps.location.lat();
        Longitude = gps.location.lng();
      }

      if (gps.date.isValid())
      {
        date = gps.date.day();
        month = gps.date.month();
        year = gps.date.year();
      }

      if (gps.time.isValid())
      {
        hour = gps.time.hour()+ 2; //adjust UTC
        minute = gps.time.minute();
        second = gps.time.second();
      }

      // Print GPS data to Serial Monitor
      Serial.print("Latitude: ");
      Serial.println(Latitude, 6);
      Serial.print("Longitude: ");
      Serial.println(Longitude, 6);
      Serial.print("Date: ");
      Serial.print(date);
      Serial.print("/");
      Serial.print(month);
      Serial.print("/");
      Serial.println(year);
      Serial.print("Time: ");
      Serial.print(hour);
      Serial.print(":");
      Serial.print(minute);
      Serial.print(":");
      Serial.println(second);

      delay(1000); // Wait for a second before printing the next set of data
    }
}
