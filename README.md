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

### The Pi

The raspberry pi will be used for data collection, from the raspberry pi. The serial interface between the pi and the arduino will send requests back and forth. The easiest way to do this is with string requests.

### The Arduino

The arduino will interface with all hardware devices over I2C. Whenever a request comes in for an update on a device from the Pi, the Arduino will read data on the appropriate I2C interface, and return the data as a csv string.

Documentation on Arduino serial interface is found [in the readme](src/arduino/README.md).
