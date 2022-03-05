
// main file for arduino i2c interface

#include <ArduinoJson-v6.19.2.h>

DynamicJsonDocument doc(1024); // json document for read/write

void setup()
{
    Serial.begin(115200);
    // Wire.begin();
}

void loop()
{
    // check for new data
    if (Serial.available())
    {
        deserializeJson(doc, Serial);
        Serial.println(doc);
    }
}
