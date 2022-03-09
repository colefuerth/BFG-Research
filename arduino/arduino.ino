
// main file for arduino i2c interface

#include "ArduinoJson-v6.19.2.h"
#include "Devices.h"
#include <Wire.h>

DynamicJsonDocument doc(1024); // json document for read/write

// array of devices
Device d[] = {LC709203F(), LTC2941_BFG(), MAX1704x_BFG()};

void setup()
{
    Serial.begin(115200);
    while (!Serial.available());
    Wire.begin();
}

void loop()
{
    // check for new data
    if (Serial.available())
    {
        deserializeJson(doc, Serial);
    }
}
