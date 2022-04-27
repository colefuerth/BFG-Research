
// main file for arduino i2c interface

// #define WatchDog

#include <ArduinoJson.h>
#include "Devices.h"

DynamicJsonDocument doc(128); // json document for read/write, declared on the stack

Device *devices[] = {new LC709203F(), new SHTC3(), new INA219(), new MAX1704x_BFG()};

void setup()
{
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, LOW);
    while (!Serial)
        delay(1);
    delay(10);
    LOG("Starting...");

    if (TWCR == 0) // do this check so that Wire only gets initialized once
    {
        Wire.begin();
        LOG(F("Wire initialized"));
    }

    for (Device *d : devices)
    {
        d->begin();
    }
    
    LOG(F("Done setup"));
}

void loop()
{
    // check for data
    if (Serial.available() > 0)
    {
        digitalWrite(LED_BUILTIN, HIGH);
        // incoming data comes in as{DeviceStr:RequestsStr}
        // example: {"LC709203F":"VP"} will get Voltage and Percent from LC709203F device
        deserializeJson(doc, Serial);
        JsonObject root = doc.as<JsonObject>();
        for (JsonPair kv : root)
        {
            // iterate through devices
            String k = kv.key().c_str();
            Device *d = getDevice(k);
            String v = kv.value().as<const char *>();
            // build return packet
            DynamicJsonDocument ret(128);
            ret["D"] = d->D();
            for (char c : v)
            {
                ret[String(c)] = getValue(d, c);
            }
            serializeJson(ret, Serial); // send return package
            Serial.print('\n');         // delimiter between packets
        }
        digitalWrite(LED_BUILTIN, LOW);
    }
    delay(1); // slow the processor down a little
}

Device *getDevice(String _D)
{
    for (Device *d : devices)
    {
        if (d->D() == _D)
        {
            return d;
        }
    }
    ERROR(F("Requested device not found"));
    return NULL; // will return an empty device if not found
}

String getValue(Device *d, char V)
{
    switch (V)
    {
    case 'V':
        return String(d->V(), 3);
    case 'I':
        return String(d->I(), 3);
    case 'C':
        return String(d->C(), 3);
    case 'P':
        return String(d->P(), 3);
    case 'T':
        return String(d->T(), 3);
    case 'H':
        return String(d->H(), 3);
    case 'W':
        return String(d->W(), 3);
    default:
        return "";
    }
}
