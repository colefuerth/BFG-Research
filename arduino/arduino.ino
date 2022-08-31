
// main file for arduino i2c interface

#include <ArduinoJson.h>
#include "Devices.h"

DynamicJsonDocument doc(128); // json document for read/write, declared on the stack

// these two are ESSENTIAL for the use of the multiplexer `Device` backend
// Device::mux = 0x71;      // address of mux
// Device::channels = 0x00; // default mux state (changed by devices as needed)

// array of devices
// If passed a multiplexer channel, then the multiplexer will only allow the device to communicate on that channel when absolutely necessary
Device *devices[] = {new MAX31855(), new INA260(), new LC709203F()};
LC709203F *lc = (LC709203F *)devices[2]; // need direct access to the LC for voltage readings for the relay
#define RELAYCUTOFF 2.7

#define RELAY_PIN 7

void setup()
{
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, LOW);
    while (!Serial)
        delay(1);

    if (TWCR == 0) // do this check so that Wire only gets initialized once
    {
        Wire.begin();
        LOG("Wire initialized");
    }

    // initialize mux
    // Device::setmux(Device::channels); // set base state
    // LOG("Mux initialized");
    for (Device *d : devices)
    {
        d->begin();
    }

    // relay pin is 7, initialize to output
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, HIGH);

    LOG("Done setup");
}

void loop()
{
    // check for new data
    if (Serial.available() > 0)
    {
        digitalWrite(LED_BUILTIN, HIGH);
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
    // if d->D() is the LC709203F, update the relay state
    static unsigned long lastUpdate = 0;
    if (millis() - lastUpdate > 1000)
    {
        lastUpdate = millis();
        if (lc->V() < RELAYCUTOFF)
        {
            digitalWrite(RELAY_PIN, LOW);
        }
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
    ERROR("Requested device not found");
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
