
// main file for arduino i2c interface

#include "ArduinoJson-v6.19.2.h"
#include "Devices.h"
#include <Wire.h>
// #include <map>

StaticJsonDocument<1024> doc; // json document for read/write, declared on the stack

// array of devices
// here to make sure that devices do indeed compile;
// if they are not called in main, they will not compile
Device devices[] = {LC709203F(), LTC2941_BFG(), MAX1704x_BFG()};

void setup()
{
    Serial.begin(115200);
    while (!Serial.available())
        ;
    Wire.begin();
}

void loop()
{
    // check for new data
    if (Serial.available())
    {
        // incoming data comes in as{DeviceStr:RequestsStr}
        // example: {LC709203F:VP} will get Voltage and Percent from LC709203F device
        deserializeJson(doc, Serial);
        JsonObject root = doc.as<JsonObject>();
        for (JsonPair kv : root)
        {
            // iterate through devices
            String k = kv.key().c_str();
            Device *d = getDevice(k);
            if (d->D() != k)
            {
                ERROR(F("Requested device not found"));
            }
            String v = String(kv.value().as<const char *>());
            // for each device, create a nested map of requests and values to be returned
            JsonVariant ret;
            for (char c : v)
            {
                ret[c] = getValue(d, c);
            }
            root[k] = ret;
        }
        serializeJson(doc, Serial); // send return package
    }
}

Device *getDevice(String _D)
{
    for (auto d : devices)
    {
        if (d.D() == _D)
        {
            return &d;
        }
    }
    return &Device(); // will return an empty device if not found
}

String getValue(Device *d, char V)
{
    switch(V)
    {
    case 'V':
        return String(d->V());
    case 'I':
        return String(d->I());
    case 'C':
        return String(d->C());
    case 'P':
        return String(d->P());
    case 'T':
        return String(d->T());
    default:
        return "";
    }
}