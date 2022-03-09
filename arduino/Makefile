
# arduino-cli install instructions https://siytek.com/arduino-cli-raspberry-pi/

AC = arduino-cli
USB = /dev/ttyUSB0
MAIN = arduino
BOARD = arduino:avr:micro
# "programmer": "arduino:avrispmkii"

# verbose cli flag is -v or --verbose

# documentation here https://arduino.github.io/arduino-cli/0.21/commands/arduino-cli/

libraries:
	$(AC) core install arduino:avr
	$(AC) lib install "Adafruit BusIO"
	$(AC) lib install "Adafruit LC709203F"
	$(AC) lib install "Grove - Coulomb Counter for 3.3V to 5V LTC2941"
	$(AC) lib install "SparkFun MAX1704x Fuel Gauge Arduino Library"

build:
	$(AC) compile --fqbn $(BOARD) $(MAIN).ino

upload:
	$(AC) upload -p /dev/ttyUSB0 --fqbn $(BOARD) $(MAIN)

clean:
	$(AC) cache clean -v