# A utility for determining the COM port of the Arduino, using arduino-cli

import subprocess as sp
import platform

if platform.system() == 'Windows':
    arduino_cli = 'arduino-cli/win64/arduino-cli.exe'
elif platform.system() == 'Linux':
    arduino_cli = 'arduino-cli/linux64/arduino-cli'
else:
    raise Exception('Unsupported OS')

# get the list of boards from `arduino-cli board list`


def get_arduino_comport():
    # return sp.check_output([arduino_cli, 'board', 'list']).decode('utf-8').split('\n')
    for i, line in enumerate(sp.check_output([arduino_cli, 'board', 'list']).decode('utf-8').strip().split('\n')[1:]):
        # if line contains 'Arduino', return the COM port
        if 'Arduino' in line:
            for token in line.split(' '):
                if platform.system() == 'Windows' and token.startswith('COM') or \
                   platform.system() == 'Linux' and token.startswith('/dev/ttyACM'):
                    return token.strip()
    raise Exception('No Arduino found')


if __name__ == '__main__':
    print(get_arduino_boards())
