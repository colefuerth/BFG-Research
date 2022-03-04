# Classes to connect to the individual BFG devices

class BFG:
    # Generic class to interface with BFG devices
    def __init__(self):
        self.name = "generic BFG device"
        self.serial = "unknown"
        
    def __str__(self):
        return self.name + " (" + self.serial + ")"

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