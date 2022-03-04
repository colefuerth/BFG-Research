# Arduino Implementation

### Requirements

- Take in command line instructions over Serial UART, space-delimited.
- Recursively parse the instructions and execute them, allowing for requests containing individual or multiple instructions
- Manage the I2C bus, using a multiplexer, to get data from the correct devices
- Return parsed data to the host over Serial UART as an "ID:KEY:VALUE" string

### Table of Keys

| Key | Device(s) | Description | Return type |
| --- | --------- | ----------- | ------------ |
| V | LC709203F, MAX17043 | Battery Voltage (V) | float |
| I | LC709203F, LTC2941 | Battery Current (A) | float |
| C | ? | Battery Capacity (mAh) | int |
| S | ? | Battery State (0=discharging, 1=charging) | int |
| P | ? | Battery Percentage (0-1) | float |
| T | ? | Battery Temperature (C) | float |
| W | ? | Battery Wattage (W) | float |
