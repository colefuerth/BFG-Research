// Header file for BFG implementations

// avr libraries
#include <Arduino.h> // String implemented here
#include <Wire.h>

// bfg libraries
#include <Adafruit_LC709203F.h>

// remaining libraries
#include <SPI.h> // for thermocouple softserial
#include <Adafruit_MAX31855.h>
#include <Adafruit_INA260.h>

// --------------- UTILITY FUNCTIONS ---------------

void LOG(String msg)
{
    Serial.println("{\"D\":\"LOG\",\"M\":\"" + msg + "\"}");
}

// If there is a major fault, display msg on serial and flash LED
// all messages should be PROGMEM strings, to save stack space
void ERROR(String msg)
{
    Serial.println("{\"D\":\"ERROR\",\"M\":\"" + msg + "\"}");
    // LOG(msg);
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
    static uint8_t mux;
    static uint8_t channels;
    Device(int channel = -1)
    {
        this->_D = "none";
        this->_channel = channel;
        channels &= 0xFF ^ (1 << this->_channel);
    }

    /**
     * @brief change multiplexer register
     */
    static void setmux(uint8_t reg)
    {
        Wire.beginTransmission(mux);
        Wire.write(reg);
        Wire.endTransmission();
    }

    virtual bool begin() { return true; }
    // void begin();                   // start I2C interface
    virtual String D() { return this->_D; } // Device ID
    virtual float V() { return -1; }        // Voltage (V)
    virtual float I() { return -1; }        // current (mA)
    virtual float C() { return -1; }        // draw so far (mAh)
    virtual float P() { return -1; }        // Battery percentage
    virtual float T() { return -1; }        // Temperature (C)
    virtual float H() { return -1; }        // Humidity (%), relative
    virtual float W() { return -1; }        // Wattage (mW)
    // int S() { return 0; }           // state, 0=discharging, 1=charging
protected:
    String _D; // Device ID
    uint8_t _channel;

    void open()
    {
        if (this->_channel >= 0)
        {
            if (this->_channel > 7)
            {
                ERROR("Invalid channel");
            }
            channels |= 1 << this->_channel;
            Device::setmux(channels);
        }
    }

    void close()
    {
        if (this->_channel >= 0)
        {
            if (this->_channel > 7)
            {
                ERROR("Invalid channel");
            }
            channels &= 0xFF ^ (1 << this->_channel);
            Device::setmux(channels);
        }
    }

    /**
     * @brief template function to get a value from an I2C device. opens multiplexer channel (if specified) and closes it when done
     * @tparam T type of value to return
     * @param f function to call to get value
     */
    template <typename T, typename Func>
    T withmux(Func f)
    {
        this->open();
        T ret = f();
        this->close();
        return ret;
    }
};

uint8_t Device::mux = 0x70;      // default address of mux
uint8_t Device::channels = 0xFF; // default mux state (changed by devices as needed)

// ------------------ BFG DEVICES ------------------

class LC709203F : public Device
{
public:
    LC709203F(int channel = -1) : Device(channel)
    {
        this->_D = "LC709203F";
    }

    bool begin()
    {
        return this->withmux<bool>([&]()
                                   {
        if (!this->lc.begin())
            ERROR("Couldnt find Adafruit LC709203F? Make sure a battery is plugged in!");
        lc.setThermistorB(3950);
        lc.setPackSize(LC709203F_APA_500MAH);
        lc.setAlarmVoltage(3.4);
        LOG("LC709203F initialized");
        return true; });
    }

    float V()
    {
        return this->withmux<float>([&]()
                                    { return lc.cellVoltage(); });
    }
    float P()
    {
        return this->withmux<float>([&]()
                                    { return lc.cellPercent(); });
    }
    float T()
    {
        return this->withmux<float>([&]()
                                    { return lc.getCellTemperature(); });
    }

protected:
    Adafruit_LC709203F lc;
};

/**
 * @brief This class is a wrapper for the MAX31855. This device uses SPI, unlike other devices.
 */
class MAX31855 : public Device
{
public:
    MAX31855() : Device()
    {
        this->_D = "MAX31855";
    }

    bool begin()
    {
        delay(100); // max chip needs a second to stabilize
        if (!this->tc.begin())
            ERROR("Couldn't find MAX31855");
        LOG("MAX31855 initialized");
        return true;
    }

    float T()
    {
        double c = this->tc.readCelsius();
        if (isnan(c))
            ERROR("Something wrong with thermocouple!");
        return c;
    }

    float C()
    {
        double c = this->tc.readInternal();
        if (isnan(c))
            ERROR("Something wrong with internal MAX31855 temp!");
        return c;
    }

private:
    uint8_t MAXCLK = 4, MAXCS = 5, MAXDO = 6;
    Adafruit_MAX31855 tc = Adafruit_MAX31855(MAXCLK, MAXCS, MAXDO);
};

class INA260 : public Device
{
public:
    INA260(int channel = -1) : Device(channel)
    {
        this->_D = "INA260";
    }

    bool begin()
    {
        return this->withmux<bool>([&]()
                                   {
        if (!this->ina.begin())
            ERROR("Couldn't find INA260");
        LOG("INA260 initialized");
        return true; });
    }

    float V()
    {
        return this->withmux<float>([&]()
                                    { return this->ina.readBusVoltage() / 1000.0; });
    }
    float I()
    {
        return this->withmux<float>([&]()
                                    { return this->ina.readCurrent(); });
    }
    float W()
    {
        return this->withmux<float>([&]()
                                    { return this->ina.readPower(); });
    }

protected:
    Adafruit_INA260 ina;
};
