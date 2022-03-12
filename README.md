# BFG Research

## Summary

This repository is for development of data collection programs for a Raspberry Pi Zero, testing and comparing different Battery Fuel Gauges.

**To install dependencies, please run:** `pip install -r src/requirements.txt`

**To run the program, please run:** `python src/main.py`

## BFG Units Tested

| Device                                                    | Product Page                                                                                        | Datasheet                                                                    | Arduino Library                                                                                 | Manufacture    | Description                                                                                         |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------- |
| <img src="img/BFG1.jpg" width=600 alt='BFG_1'>            | [LC709203F](https://www.adafruit.com/product/4712)                                             | [Short Guide](datasheets/adafruit-lc709203f-lipo-lipoly-battery-monitor.pdf) | [Adafruit_LC709203F](https://github.com/adafruit/Adafruit_LC709203F)                            | AdaFruit       | This BFG reads a combination of voltage and current, to estimate the battery's charge and capacity. |
| <img src='img/BFG2.jpg' width=600 alt='BFG_2'>            | [LTC2941](https://www.analog.com/en/products/ltc2941.html#product-overview)                    | [Datasheet](datasheets/LTC2941.pdf)                                          | [Seeed_LTC2941](https://github.com/Seeed-Studio/Seeed_LTC2941)                                  | Analog Devices | BFG, Measures mAh drawn from a LiPo battery.                                                             |
| <img src='img/BFG3.jpg' width=600 alt='BFG_3'>            | [MAX17043](https://www.maximintegrated.com/en/products/power/battery-management/MAX17043.html) | [Datasheet](datasheets/MAX17043-MAX17044.pdf)                                | [SparkFun library](https://github.com/sparkfun/SparkFun_MAX1704x_Fuel_Gauge_Arduino_Library)    | Analog Devices | BFG, Measures mV across battery cell for estimate.                                                       |
| <img src='img/TCA9548A.jpg' width=600 alt='multiplexer'>  | [TCA9548A](https://learn.adafruit.com/adafruit-tca9548a-1-to-8-i2c-multiplexer-breakout/downloads)  | [Datasheet](datasheets/tca9548a.pdf)                                         | [GitHub library](https://github.com/WifWaf/TCA9548A)                                            | AdaFruit       | An I2C multiplexer, for connecting all devices to the arduino I2C bus.                              |
| <img src='img/SHTC3.jpg' width=600 alt='multiplexer'>     | [SHTC3](https://learn.adafruit.com/adafruit-sensirion-shtc3-temperature-humidity-sensor/arduino)    | [Datasheet](datasheets/SHTC3.pdf)                                            | [GitHub library](https://github.com/adafruit/Adafruit_SHTC3)                                    | AdaFruit       | Adafruit Sensirion SHTC3 Temperature & Humidity Sensor                                              |
| <img src='img/MAX31855.jpg' width=600 alt='thermocouple'> | [MAX31855](https://www.adafruit.com/product/269)                                                    | [Datasheet](datasheets/MAX31855.pdf)                                         | [Arduino Guide](https://learn.adafruit.com/thermocouple/arduino-code#arduino-library-2958404-6) | AdaFruit       | Thermocouple Amplifier MAX31855 breakout board                                                      |
| <img src='img/INA260.jpg' width=600 alt='power sensor'>   | [INA260](https://learn.adafruit.com/adafruit-ina260-current-voltage-power-sensor-breakout)          | [Datasheet](datasheets/ina260.pdf)                                           | [GitHub library](https://github.com/adafruit/Adafruit_INA260)                                   | AdaFruit       | Adafruit INA260 Current + Voltage + Power Sensor                                                    |

## Implementation

Since two of the units are designed for Arduino, the simplest way to implement this is to use an Arduino, and get all data from the arduino, onto the pi, over serial.

The pi sends JSON payloads to the arduino, which unpacks them, grabs the necessary data from the device requested, repacks it, and sends it back to the pi.

**The Python code for Pi is under `src`; the arduino code is under `arduino`**

## The Pi

The raspberry pi will be used for data collection, from the raspberry pi. The serial interface between the pi and the arduino will send requests back and forth. The easiest way to do this is with string requests.

## The Arduino

The arduino will interface with all hardware devices over I2C. Whenever a request comes in for an update on a device from the Pi, the Arduino will read data on the appropriate I2C interface, and return the data as JSON payload.

### Requirements

- Data will be communicated over serial, in JSON format. Arduino library is [ArduinoJSON](https://github.com/bblanchon/ArduinoJson).
- Manage the I2C bus, using a multiplexer, to get data from the correct devices
- All required key responses will be defined in a generic class, which will be a superclass to the BFG devices. This will allow for mosular queries.
- The BFGs will be kept in a map, where keys are the device string names, and the values are the BFG objects. Each data key will be associated with a BFG function call, so the JSON string queries can be directly mapped to the BFG functions.

### Table of Keys and Callable Data

| Key | Device(s) callable  | Description                       | Return type |
| --- | ------------------- | --------------------------------- | ----------- |
| D   | all devices         | specifies the device being queued | echo device |
| V   | LC709203F, MAX17043 | Battery Voltage (V)               | float       |
| I   | none                | Battery Current (A)               | float       |
| C   | LTC2941             | Battery Capacity (mAh)            | float       |
| P   | LTC2941, MAX17043   | Battery Percentage (0-100)        | float       |
| T   | LC709203F           | Battery Temperature (C)           | float       |

<!-- | S                   | ?                                 | Battery State (0=discharging, 1=charging) | int   | -->
<!-- | W                   | ?                                 | Battery Wattage (W)                       | float | -->

### Request JSON (Pi -> Arduino)

JSON requests will be one key/value pair. The key will be the device being queried, and the value will be an array of strings associated with values requested.

### Response JSON (Arduino -> Pi)

Output JSON will be will be a dict of dictionary of key/value pairs. Each root query key is the device, to identify the device being echoed. The value data being sent will be the key/value pairs for queried data, for each key/device.
