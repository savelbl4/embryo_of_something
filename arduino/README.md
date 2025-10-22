
## установка

raspberrypi:~ $ curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh


arduino-cli board list


arduino-cli config init


lsusb


sudo apt install dkms


savelbl4@raspberrypi:~ $ sudo modprobe -r ch341
savelbl4@raspberrypi:~ $ sudo modprobe ch341
savelbl4@raspberrypi:~ $ sudo modprobe

arduino-cli core update-index

arduino-cli core install arduino:avr

arduino-cli sketch new NanoBlink

## комиляция и прошивка

~/NanoBlink $ arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega328old .

~/NanoBlink $ arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:nano:cpu=atmega328old .

## какие-то дополнительные штуки

sudo apt install avrdude

avrdude -p atmega328p -c arduino -P /dev/ttyUSB0 -b 57600 -U eeprom:r:eeprom_dump.hex:i

avrdude -p atmega328p -c arduino -P /dev/ttyUSB0 -b 57600 -U flash:r:firmware.hex:i

sudo apt install hexedit

hexedit eeprom_dump.hex