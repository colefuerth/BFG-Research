// Header file for BFG implementations

// avr libraries
#include <Arduino.h> // String implemented here
#include <Wire.h>

// bfg libraries
#include <Adafruit_LC709203F.h>
#include <LTC2941.h>
#include <SparkFun_MAX1704x_Fuel_Gauge_Arduino_Library.h>

// remaining libraries
#include <TCA9548A.h>
#include <Adafruit_SHTC3.h>
// #include <Adafruit_MAX31855.h>

// --------------- UTILITY FUNCTIONS ---------------

// If there is a major fault, display msg on serial and flash LED
// all messages should be PROGMEM strings, to save stack space
void ERROR(const __FlashStringHelper *msg)
{
    Serial.println(msg);
    pinMode(LED_BUILTIN, OUTPUT);
    while (1)
    {
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
    }
}

// ------------------ DEVICE BASE CLASS ------------------

class Device
{
public:
    Device() { this->_D = "none"; }
    void begin();                   // start I2C interface
    String D() { return this->_D; } // Device ID
    float V() { return 0; }         // Voltage (V)
    float I() { return 0; }         // current (mA)
    float C() { return 0; }         // draw so far (mAh)
    float P() { return 0; }         // Battery percentage
    float T() { return 0; }         // Temperature (C)
    float H() { return 0; }         // Humidity (%), relative
    float W() { return 0; }         // Wattage (mW)
    // int S() { return 0; }           // state, 0=discharging, 1=charging
protected:
    String _D; // Device ID
};

// ------------------ BFG DEVICES ------------------

class LC709203F : public Device
{
public:
    LC709203F() : Device()
    {
        this->_D = "LC709203F";
        if (!this->lc.begin())
            ERROR(F("Couldnt find Adafruit LC709203F?\nMake sure a battery is plugged in!"));
        // lc.setThermistorB(3950);
        lc.setPackSize(LC709203F_APA_1000MAH);
        lc.setAlarmVoltage(3.4);
    }

    float V() { return lc.cellVoltage(); }
    float P() { return lc.cellPercent(); }
    float T() { return lc.getCellTemperature(); }

protected:
    Adafruit_LC709203F lc;
};

class LTC2941_BFG : public Device
{
public:
    LTC2941_BFG() : Device()
    {
        this->_D = "LTC2941";
        this->ltc.initialize();
        ltc2941.setBatteryFullMAh(1000);
    }

    float C() { return this->ltc.getmAh(); }
    float P() { return this->ltc.getPercent(); }

protected:
    LTC2941 ltc = ltc2941;
};

// this sucks but it was the only way to get the library to compile
SFE_MAX1704X lipo(MAX1704X_MAX17043);
class MAX1704x_BFG : public Device
{
public:
    MAX1704x_BFG() : Device()
    {
        this->_D = "MAX1704x";
        if (!lipo.begin())
            ERROR(F("MAX17044 not detected. Please check wiring. Freezing."));
        // Quick start restarts the MAX17044 in hopes of getting a more accurate guess for the SOC.
        lipo.quickStart();

        // We can set an interrupt to alert when the battery SoC gets too low. We can alert at anywhere between 1% - 32%:
        lipo.setThreshold(20); // Set alert threshold to 20%.
    }

    float V() { return lipo.getVoltage(); }
    float P() { return lipo.getSOC(); }

    // protected:
    // SFE_MAX1704X lipo(MAX1704X_MAX17043); // Create a MAX17043 object
};

// ------------------ REMAINING I2C DEVICES ------------------

// TODO: add more info to this class
class TCA9548AMUX : public Device
{
public:
    TCA9548AMUX() : Device()
    {
        this->_D = "TCA9548A";
        this->tca.begin(Wire);
        tca.openAll(); // by default, open all channels. Only mess with this if there are address conflicts
    }

    void openChannel(uint8_t channel)
    {
        this->tca.openChannel(channel);
    }

    void closeChannel(uint8_t channel)
    {
        this->tca.closeChannel(channel);
    }

private:
    TCA9548A tca;
};

class SHTC3 : public Device
{
public:
    SHTC3() : Device()
    {
        this->_D = "SHTC3";
        if (!shtc3.begin())
            ERROR(F("Couldn't find SHTC3"));
        // Serial.println("Found SHTC3 sensor");
    }

    float T()
    {
        this->_update();
        return this->temp.temperature;
    }
    float H()
    {
        this->_update();
        return this->humidity.relative_humidity;
    }

private:
    Adafruit_SHTC3 shtc3 = Adafruit_SHTC3();
    sensors_event_t humidity, temp;

    void _update()
    {
        this->shtc3.getEvent(&humidity, &temp);
    }
};
