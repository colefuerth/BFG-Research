# BFG Research

## Summary

This repository is for development of data collection programs for a Raspberry Pi Zero, testing and comparing different Battery Fuel Gauges.

**To install dependencies, please run:** `pip install -r src/requirements.txt`

**To run the program, please run:** `python src/main.py`

## BFG Units Tested

| BFG                                            | Product                                                                                        | Datasheet                                                                    | `pip` Library                                                                                    | Manufacture    | Description                                                                                         |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------- | --------------------------------------------------------------------------------------------------- |
| <img src="img/BFG1.jpg" width=300 alt='BFG_1'> | [LC709203F](https://www.adafruit.com/product/4712)                                             | [Short Guide](datasheets/adafruit-lc709203f-lipo-lipoly-battery-monitor.pdf) | [adafruit-circuitpython-lc709203f](https://github.com/adafruit/Adafruit_CircuitPython_LC709203F) | AdaFruit       | This BFG reads a combination of voltage and current, to estimate the battery's charge and capacity. |
| <img src='img/BFG2.jpg' width=300 alt='BFG_2'> | [LTC2941](https://www.analog.com/en/products/ltc2941.html#product-overview)                    | [Datasheet](datasheets/LTC2941.pdf)                                          | **no pip library.** gonna have to make one                                                       | Analog Devices | Measures mAh drawn from a LiPo battery.                                                             |
| <img src='img/BFG3.jpg' width=300 alt='BFG_3'> | [MAX17043](https://www.maximintegrated.com/en/products/power/battery-management/MAX17043.html) | [Datasheet](datasheets/MAX17043-MAX17044.pdf)                                | **no pip library.** gonna have to make one                                                       | Analog Devices | Measures mV across battery cell for estimate.                                                       |

## Implementation

Since two of the units are designed for Arduino, the simplest way to implement this is probably to use an Arduino, and get all data from the arduino, onto the pi, over serial.

**The Python code for Pi is under `src`; the arduino code is under `arduino`**

## The Pi

The raspberry pi will be used for data collection, from the raspberry pi. The serial interface between the pi and the arduino will send requests back and forth. The easiest way to do this is with string requests.

## The Arduino

The arduino will interface with all hardware devices over I2C. Whenever a request comes in for an update on a device from the Pi, the Arduino will read data on the appropriate I2C interface, and return the data as a csv string.

### Requirements

- Data will be communicated over serial, in JSON format. Arduino library is [ArduinoJSON](https://arduinojson.org/).
- Manage the I2C bus, using a multiplexer, to get data from the correct devices
- All required key responses will be defined in a generic class, which will be a superclass to the BFG devices. This will allow for mosular queries.
- The BFGs will be kept in a map, where keys are the device string names, and the values are the BFG objects. Each data key will be associated with a BFG function call, so the JSON string queries can be directly mapped to the BFG functions.

### Table of Keys

| Key | Device(s) | Description | Return type |
| --- | --------- | ----------- | ------------ |
| D | all devices | specifies the BFG device being queued | echo device |
| V | LC709203F, MAX17043 | Battery Voltage (V) | float |
| I | LC709203F, LTC2941 | Battery Current (A) | float |
| C | ? | Battery Capacity (mAh) | float |
| S | ? | Battery State (0=discharging, 1=charging) | int |
| P | ? | Battery Percentage (0-100) | float |
| T | ? | Battery Temperature (C) | float |
| W | ? | Battery Wattage (W) | float |

### Input JSON

JSON requests will be one key/value pair. The key will be the device being queried, and the value will be an array of strings associated with values requested.

### Output JSON

Output JSON will be will be a dictionary of key/value pairs. Every query will include a "D":device pair, to identify the device being echoed. The remaining data being sent will be the key/value pairs for queried data.
