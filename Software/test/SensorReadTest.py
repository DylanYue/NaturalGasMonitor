""" This code runs the data acquisition and write to a file endlessly.
	Author: Dingjun Yue
	Date: Nov/2017
"""

import time
import Adafruit_MCP3008


# Software SPI configuration:
CLK  = 18
MISO = 16
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)
# Main program loop.
while True:
    # Read all the ADC channel values in a list.
	values = [0]*8
	for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
		values[i] = mcp.read_adc(i)
    # Print the ADC values.
	print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    # Print the ADC values.
    # Pause for half a second.
	time.sleep(0.5)