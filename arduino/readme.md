# Arduino Code

## Libraries

This project has a list of dependencies. If you have arduino-cli and make installed, you can run `make libraries` in the src folder, and it will auto-install all dependencies.

Else, the list of libraries required is:

    ArduinoJson
    Adafruit BusIO
    Adafruit LC709203F
    Grove - Coulomb Counter for 3.3V to 5V LTC2941
    SparkFun MAX1704x Fuel Gauge Arduino Library
    TCA9548A
    Adafruit SHTC3 Library
    Adafruit MAX31855 library
    Adafruit INA260 Library
    Adafruit INA219

*NOTE:* Most likely, I will make forks of this repository depending on specific tests being run, with trimmed-down versions of this library. This library is very big, and uses a lot of PROGMEM. Dependencies will change in these forks.

## Choosing Devices

All connected devices will be specified in the `Device *devices[]` array in arduino.ino, near the top of the code. Each device, with the exception of the MAX31855 (uses serial), will need its I2C multiplexer channel specified, but ONLY if using the multiplexer.

## Multiplexer

- The multiplexer is controlled with Wire commands, and is used to select the I2C channel of the device.
- Lines 11 and 12 of arduino.ino specify the multiplexer's I2C address and the default state.
- If the default state is 0, then all channels will be closed by default, and only opened if a device has a channel specified.
- If the default state is 0xFF, then all channels will be opened by default, and only closed if a device has a channel specified. Thus, if there are any device conflicts, both devices need channels specified.
- **The multiplexer can be removed** simply by not setting any channels in the `Device *devices[]` array, and commenting out the `Device::setmux(Device::channels);` call on line 35 of ardunio.ino.
- **IMPORTANT:** If the multiplexer is either not connected or set to the wrong channel, and something tries to write to it, **the processor will crash**. This is left up to the user to ensure it does not happen, as I ran out of PROGMEM to make safeties against this

## MAX31855

Since the MAX31855 is a serial device, it is not possible to use the multiplexer to control its I2C channel. Its SPI pins are specified in its class in `Devices.h`. By default, the pins are:

    - CLK = 4
    - CS = 5
    - DO = 6

## Getting Started

### JSON Communication

Getting data from the arduino is done with JSON packets. The JSON packet is a string of the form:

```json
{"devicename":"devicevalue","devicename":"devicevalue"}
```

    devicename is the name of the device, ex: "INA260"
    devicevalue is the string of attributes to get from the device
    ex: "VIW" will get the voltage, current and power readings.

*Note:* requests can contain multiple device requests, separated by commas. You can request updates on all devices in a single packet, but responses will come back in individual packets.

So, a request for the voltage, current and power of the INA260 would be:

```json
{"INA260":"VIW"}
```

These packets are sent over the serial port, and the arduino will respond with a JSON packet of the form:

```json
{"D":"devicename","key1":value,"key2":value}
```

    D is the device name this packet is referring to
    key1 and key2 are the keys of the values requested
    value is the value of the key

So, a response from the INA260 request above might be:

```json
{"D":"INA260","V":4.015,"I":85.000,"P":350.000}
```

### Logging and Errors

The arduino might have logging or error messages. These are also sent over serial JSON, in addition to the normal JSON packets.

A message might look like:

```json
{"D":"LOG","M":"message"}
```

ERRORS are the same, except the device value is "ERROR" instead of "LOG". ERRORS should stop the program, and are usually caused by a hardware failure. ERRORS will also indicate the processor has stopped.
