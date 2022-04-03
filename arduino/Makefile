
# arduino-cli install instructions https://siytek.com/arduino-cli-raspberry-pi/

AC = arduino-cli
# USB = /dev/ttyACM0
USB = COM8
MAIN = arduino
# BOARD = arduino:avr:nano:cpu=atmega328old
BOARD = arduino:avr:micro
PROGRAMMER = avrispmkii

# LIST PROGRAMMERS
# arduino-cli board details -b arduino:avr:micro --list-programmers

# verbose cli flag is -v or --verbose

# arduino-cli documentation [here](https://arduino.github.io/arduino-cli/0.21/commands/arduino-cli/)

libraries:
# 	install the avr binaries for micro
	$(AC) core install arduino:avr
#	install the JSON library
	$(AC) lib install "ArduinoJson"
#   install the BFG libraries
	$(AC) lib install "Adafruit BusIO"
	$(AC) lib install "Adafruit LC709203F"
	$(AC) lib install "Grove - Coulomb Counter for 3.3V to 5V LTC2941"
	$(AC) lib install "SparkFun MAX1704x Fuel Gauge Arduino Library"
#   remaining hardware devices
	$(AC) lib install "TCA9548A"
	$(AC) lib install "Adafruit SHTC3 Library"
	$(AC) lib install "Adafruit MAX31855 library"
	$(AC) lib install "Adafruit INA260 Library"
	$(AC) lib install "Adafruit INA219"

# attach:
# 	$(AC) board attach -b $(BOARD) -p $(USB) $(MAIN)

build:
	$(AC) compile --fqbn $(BOARD) $(MAIN)

vbuild:
	$(AC) compile -v --fqbn $(BOARD) $(MAIN)

upload:
	$(AC) upload --port $(USB) --fqbn $(BOARD) --programmer $(PROGRAMMER) $(MAIN)

clean:
	$(AC) cache clean -v

find:
	$(AC) core update-index
	$(AC) board list
