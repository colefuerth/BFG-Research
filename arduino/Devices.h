// Header file for BFG implementations

#include <Arduino.h>

// generic class for BFG implementations
class Device {
public:
    Device() {this->_D = "none"; this->_addr = 0;}
    void begin();                   // start I2C interface
    String D() {return this->_D;}    // Device ID
    float V() {return 0;}           // Voltage (V)
    float I() {return 0;}           // current (A)
    float C() {return 0;}           // capacity (mAh)
    int   S() {return 0;}           // state, 0=discharging, 1=charging
    float P() {return 0;}           // Battery percentage
    float T() {return 0;}           // Temperature (C)
    float W() {return 0;}           // Wattage (W)
private:
    String _D;                      // Device ID
    int _addr;                      // I2C address
};