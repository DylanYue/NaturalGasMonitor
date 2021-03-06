""" This code runs the data acquisition and write to a file endlessly.
	data is stored under data folder
	Author: Dingjun Yue
	Date: Nov/2017
"""

import time
import Adafruit_MCP3008
import os
from datetime import datetime

# Software SPI configuration: Initialize ADC MCP3008
CLK  = 18
MISO = 16
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Reference voltage is 5 volts.
refVolt = 5.0

# Initialize file and get ready to record.
filename = str(datetime.now())
here = os.path.dirname(os.path.realpath(__file__))
subdir = "data"
filepath = os.path.join(here, subdir, filename)

with open(filepath, "w") as f:
        f.write("Time" + "," + "Pressure(KPa)" + '\n')
		

# Main program loop
while True:

	rawValue = mcp.read_adc(0)
	floatRaw = float(rawValue)
	rawVolt = floatRaw * refVolt / 1024.0
	pressureMPa = (rawVolt) / 4.0
	pressureKPa = pressureMPa * 1000.0
	
	valueString = str(datetime.now().time()) + "," + str(pressureKPa) + '\n'

	with open(filepath, "a") as f:
		f.write(valueString)

	time.sleep(0.33)
