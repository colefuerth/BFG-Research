# Classes to connect to the individual BFG devices

class HID:
    # Generic Hardware Interface Device with RPi
    # provides basic functionality for all devices over I2C to inherit from
    def __init__(self, i2c_address):
        self.i2c_address = i2c_address
        self.name = "HID"
        self.manufacturer = "Unknown"

    def __str__(self):
        return f'{self.name} ({self.manufacturer})'

class BFG(HID):
    # Generic class to interface with BFG devices
    # this will provide a universal interface for data collecton between the three different BFG devices
    def __init__(self, i2c_address):
        super().__init__(i2c_address)
        self.name = 'BFG device'
        self.manufacturer = 'generic'

    def percent_capacity(self):
        pass

    def voltage(self):
        pass

    def current(self):
        pass

    def temperature(self):
        pass

    def power(self):
        return self.voltage() * self.current()

class BFG_1(BFG):
    # Specific class for BFG-1
    def __init__(self, i2c_address):
        super().__init__(i2c_address)
        # product page: https://www.adafruit.com/product/4712
        # library: https://github.com/adafruit/Adafruit_CircuitPython_LC709203F
        # notes: you will need to slow down the i2c port
        self.name = 'LC709203F'
        self.manufacturer = 'AdaFruit'

class BFG_2(BFG):
    # Specific class for BFG-2
    def __init__(self, i2c_address):
        super().__init__(i2c_address)
        self.name = 'LTC2941'
        self.manufacturer = 'Analog Device'

class BFG_3(BFG):
    # Specific class for BFG-3
    def __init__(self, i2c_address):
        super().__init__(i2c_address)
        self.name = 'MAX 17043'
        self.manufacturer = 'Maxim Integrated'