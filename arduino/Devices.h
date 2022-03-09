// Header file for BFG implementations

#include <Arduino.h>    // String implemented here
// #include <Wire.h> // for I2C
#include <Adafruit_LC709203F.h>

/**
 * generic class for BFG implementations
 * 
 * All hardware devices will inherit from this superclass. 
 * This way, all payloads can be handled in a generic way, with one universal serial interface. The pi at the other end can worry about valid calls and such.
 */
class Device {
public:
    Device() {this->_D = "none";}
    void begin();                   // start I2C interface
    String D() {return this->_D;}    // Device ID
    float V() {return 0;}           // Voltage (V)
    float I() {return 0;}           // current (A)
    float C() {return 0;}           // capacity (mAh)
    int   S() {return 0;}           // state, 0=discharging, 1=charging
    float P() {return 0;}           // Battery percentage
    float T() {return 0;}           // Temperature (C)
    float W() {return 0;}           // Wattage (W)
protected:
    String _D;                      // Device ID
};


// class LC709203F : public Device {
// public:
//     LC709203F(Adafruit_LC709203F *lc) : Device() {this->_D = "LC709203F"; this->_lc = lc; this->lc.begin()}
// };
