""" Natural Gas IOT Monitor
	Author: Dingjun Yue
	Date: Nov./2017
"""

import os
import time
from datetime import datetime
import RPi.GPIO as GPIO

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import Adafruit_MCP3008

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


#from subprocess import check_output


# Text area of the screen starts from (0, 0) to (width, 60)
# Battery status area of the screen starts from (0, 61) to (width, height)

# Input button pins on OLED board:
L_pin = 27 
R_pin = 23 
C_pin = 4  # Not used in the program
U_pin = 17 
D_pin = 22 
A_pin = 5 
B_pin = 6 
# Reset pin for OLED board:
RST = None

# Digital pins used for MCP3008 ADC
CLK  = 18
MISO = 16
MOSI = 24
CS   = 25

#--Global variables--------------------------------------------------------#
# Reference voltage for MCP3008 is 5 volts.
refVolt = 5.0

# Sensor reading frequency (Hz)
readFreq = 3.0

# Sensor channel number on MCP3008
sensorChannel = 0

# File path (Initialize to None)
filePath = None
# File to store all recorded data (Initialize to None)
fileName = None

#--Initializa OLED display and MCP3008 software SPI, PushButton etc.-------# 
# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize MCP3008 software SPI
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#--OLED Display Setup--------------------------------------------------#
# Initialize library
disp.begin()

# Clear display
disp.clear()
disp.display()

# Create blank image for drawing
# Make sure to create image with mode '1' for 1-bit color
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get the drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline = 0, fill = 0)

# Setup default font, other truetype fonts can be used as long as they are in the same folder of the python script
font = ImageFont.load_default()

#---------------------------------------OLED Functions-----------------------------------------#
def RefreshDisplay():
	# This function displays the stored image on the screen
	# Use this function whenever you want to display the text or shapes in the draw object
	disp.image(image)
	disp.display()

def ClearScreen():
	# This function clears the whole screen
	draw.rectangle((0, 0, width, height), outline = 0, fill = 0)

def ClearSelector():
	# This function clears only the selector area (0, 0) to (13, 60)
	draw.rectangle((0, 0, 13, 60), outline = 0, fill = 0)
	
def ClearSetter():
	# This function clears the time setter area (14, 10) to (width, 30)
	draw.rectangle((14, 10, width, 30), outline = 0, fill = 0)
	
def ClearTextArea():
	# This function clears only the text area (14, 0) to (width, 60)
	draw.rectangle((14, 0, width, 60), outline = 0, fill = 0)

def ClearBatArea():
	# This function clears only the battery status bar area (0, 61) to (width, height)
	draw.rectangle((0, 61, width, height), outline = 0, fill = 0)

def DrawText(posX, rowNumber, text):
	# This function draws a text in the draw object
	# The X position of text is 14
	# posX is the X position of the text
	# rowNumber is the on which row the text appears
	# text is the text you want to display
	if rowNumber == 0:
		posY = -2
	elif rowNumber == 1:
		posY = 8
	elif rowNumber == 2:
		posY = 18
	elif rowNumber == 3:
		posY = 28
	elif rowNumber == 4:
		posY = 38
	elif rowNumber == 5:
		posY = 48
	else: # This display can only handle 6 lines, if rowNumber is bigger than 5, it goes to the first row.
		posY = -2
	draw.text((posX, posY), text, font = font, fill = 255)
	
def DrawStatus(rowNumber, text):
	# Use this function to draw status in the status area
	if rowNumber == 0:
		posY = -2
	elif rowNumber == 1:
		posY = 8
	elif rowNumber == 2:
		posY = 18
	elif rowNumber == 3:
		posY = 28
	elif rowNumber == 4:
		posY = 38
	elif rowNumber == 5:
		posY = 48
	else: # This display can only handle 6 lines, if rowNumber is bigger than 5, it goes to the first row.
		posY = -2
	draw.text((101, posY), text, font = font, fill = 255)
	
def DrawBatteryStatus(batPercent):
	# This function draws the battery status bar on the bottom of the screen
	# It takes a battery percentage as the input
	batWidth = batPercent * width
	draw.rectangle((0, 61, batWidth, height), outline = 0, fill = 255)

def SelectorPosConditioner (rawPos):
	# This function always returns the selector's real position on the screen (0 - 5)
	# It takes the "raw" selector position as the input
	return rawPos % 6

def PlaceSelector(rowNumber):
	# This function draws the selector on the screen, it takes the row number as input
	DrawText(0, SelectorPosConditioner(rowNumber), "->")

def SetterPosConditioner (rawPos):
	# This function always returns the selector's real position on the screen (0 - 5)
	# It takes the "raw" selector position as the input
	return rawPos % 5
	
def PlaceSetter(columnNumber):
	# This function draws the selector on the screen, it takes the row number as input
	columnNumber = SetterPosConditioner(columnNumber)
	if columnNumber == 0:
		posX = 24
	elif columnNumber == 1:
		posX = 47
	elif columnNumber == 2:
		posX = 65
	elif columnNumber == 3:
		posX = 83
	elif columnNumber == 4:
		posX = 102
	DrawText(posX, 1, "^")
#--------------------------------------END OLED Functions-----------------------------------------------#


#------------------------------	State Machine Code-----------------------------------------------------
class State(object):
	def __init__(self):
		pass
	
	def __repr__(self):
		return self.__str__()
	
	def __str__(self):
		return self.__class__.__name__

class InitialState(State):
    # This is the initial state, displaying the main screen whent the program starts
	def __init__(self):
		# This displays the major functions whenever we transition into this state
		ClearTextArea()
		DrawText(14, 0, "Sensor")
		DrawText(14, 1, "Wifi")
		DrawText(14, 2, "Time")
		# DrawText(14, 3, "SD Card")
        
	def on_button_pressed(self, selector_pos, button):
		# This function handles whenever there is a button press, either transition into another state,
		# or stay the same.
		if selector_pos == 0 and button == "A":
			return SensorState()
		else:
			pass
		if selector_pos == 1 and button == "A":
			return WifiState()
		else:
			pass
		if selector_pos == 2 and button == "A":
			return TimeState()
		else:
			pass		
		if button == "U":
			Arrow.move_up()
		else:
			pass
			
		if button == "D":
			Arrow.move_down()
		else:
			pass
		# if selector_pos == 3 and button == "A":
			# return SDCardState()
		# else:
			# pass
		
		return self # Don't forget to always return yourself :)

	def repeat_action(self):
	# The action that needs to be done in each class.
	# Make sure to call this method in the main loop
		pass

class SensorState(State):
    # This is the sensor state
	def __init__(self):
		ClearTextArea()
		DrawText(14, 0, "Start Record")
		DrawText(14, 1, "Live Reading")
        
	def on_button_pressed(self, selector_pos, button):
		if selector_pos == 0 and button == "A":
			return RecordingState()
		else:
			pass
        
		if selector_pos == 1 and button == "A":
			return LiveReadingState()
		else:
			pass
			
		if button == "B":
			return InitialState()
		else:
			pass

		if button == "U":
			Arrow.move_up()
		else:
			pass
			
		if button == "D":
			Arrow.move_down()
		else:
			pass

		return self
	
	def repeat_action(self):
		pass

class RecordingState(State):
	# This state handles all the data recording job.
	def __init__(self):
		ClearTextArea()
		DrawText(14, 0, "Recording...")

	def on_button_pressed(self, selector_pos, button):
		global filePath
		global fileName
		if button == "B":
			filePath = None
			fileName = None
			return SensorState()
		else:
			pass
		return self
	
	def repeat_action(self):
		global readFreq
		InitializeFile()
		KPa = ReadPressureKPa()
		dataString = str(datetime.now().time()) + "," + str(KPa) + '\n'
		WriteDataToFile(dataString)
		time.sleep(1/readFreq)

class WifiState(State):
	# You set wifi settings in this state.
	def __init__(self):
		ClearTextArea()
		DrawText(14, 0, "Turn on")
		DrawText(14, 1, "Turn off")
	
	def on_button_pressed(self, selector_pos, button):
		if button == "B":
			return InitialState()
		else:
			pass
			
		if selector_pos == 0 and button == "A":
			return WifiOnState()
		else:
			pass
		
		if selector_pos == 1 and button == "A":
			return WifiOffState()
		else:
			pass
		
		if button == "U":
			Arrow.move_up()
		else:
			pass
			
		if button == "D":
			Arrow.move_down()
		else:
			pass
		return self
		
	def repeat_action(self):
		pass
		
class TimeState(State):
	# You set times in this state.
	def __init__(self):
		ClearTextArea()
		DrawText(14, 0, "Set Time")
	
	def on_button_pressed(self, selector_pos, button):
		if button == "B":
			return InitialState()
		else:
			pass
			
		if selector_pos == 0 and button == "A":
			return SetTimeState()
		else:
			pass
		
		if button == "U":
			Arrow.move_up()
		else:
			pass
			
		if button == "D":
			Arrow.move_down()
		else:
			pass
		return self
		
	def repeat_action(self):
		pass

class SetTimeState(State):
	# You set times in this state.
	def __init__(self):
		ClearTextArea()
		self.setterPosition = 0
		self.now = datetime.now()
		self.year = self.now.year
		self.month = self.now.month
		self.day = self.now.day
		self.hour = self.now.hour
		self.minute = self.now.minute
		self.setter = Setter(self.setterPosition)
		
	def on_button_pressed(self, selector_pos, button):
		if button == "B":
			return TimeState()
		else:
			pass
		
		if button == "A":
			return SetTimeState()
		else:
			pass
			
		if button == "L":
			self.setter.move_left()
		else:
			pass
			
		if button == "R":
			self.setter.move_right()
		else:
			pass
		
		if button == "U":
			if self.setter.current_pos == 0:
				self.year += 1
			elif self.setter.current_pos == 1:
				self.month += 1
			elif self.setter.current_pos == 2:
				self.day += 1
			elif self.setter.current_pos == 3:
				self.hour += 1
			elif self.setter.current_pos == 4:
				self.minute += 1
		else:
			pass
			
		if button == "D":
			if self.setter.current_pos == 0:
				self.year -= 1
			elif self.setter.current_pos == 1:
				self.month -= 1
			elif self.setter.current_pos == 2:
				self.day -= 1
			elif self.setter.current_pos == 3:
				self.hour -= 1
			elif self.setter.current_pos == 4:
				self.minute -= 1
		else:
			pass
		return self
		
	def repeat_action(self):
		timeString = str(self.year)+'-'+str(self.month).rjust(2)+'-'+str(self.day).rjust(2)+' '+str(self.hour).rjust(2)+':'+str(self.minute).rjust(2)
		DrawText(14, 0, timeString)
		pass
# class SDCardState(State):
	
	# def __init__(self):
		# #self.total_capacity = check_output(["df -h", "|", "awk 'NR==2 {print $2; exit}'"])
		# ClearTextArea()
		# DrawText(14, 0, self.total_capacity)

class Device(object):
	# This class represents the whole device, you transition into different states in this class.
	def __init__(self):
		self.state = InitialState()
	
	def on_button_pressed(self, selector_pos, button):
		self.state = self.state.on_button_pressed(selector_pos, button)

#---------------------------End State Machine Functions--------------------------#

#-----------------------------Selector Class-------------------------------------#
class Selector(object):
	# Selector class to store the information of the selector
	def __init__(self, selectorPos):
		ClearSelector()
		self.selectorPos = selectorPos
		PlaceSelector(self.selectorPos)
		
	def move_up(self):
	# Move slector up once
		ClearSelector()
		self.selectorPos -= 1
		PlaceSelector(self.selectorPos)
		
	def move_down(self):
	# Move selector down once
		ClearSelector()
		self.selectorPos += 1
		PlaceSelector(self.selectorPos)
		
	def selector_reset(self):
	# Reset the selector to 0 position
		ClearSelector()
		self.selectorPos = 0
		PlaceSelector(self.selectorPos)
		
	def current_pos(self):
	# Return the current position of the selector on the screen (0 - 5)
		return self.selectorPos % 6
#----------------------------End Selector Class-------------------------------------#

#-----------------------------Setter Class-------------------------------------#
class Setter(object):
	# Selector class to store the information of the time setter
	def __init__(self, setterPos):
		ClearSetter()
		self.setterPos = setterPos
		PlaceSetter(self.setterPos)
		
	def move_left(self):
	# Move slector up once
		ClearSetter()
		self.setterPos -= 1
		PlaceSetter(self.setterPos)
		
	def move_right(self):
	# Move selector down once
		ClearSetter()
		self.setterPos += 1
		PlaceSetter(self.setterPos)
		
	def setter_reset(self):
	# Reset the selector to 0 position
		ClearSetter()
		self.setterPos = 0
		PlaceSetter(self.setterPos)
		
	def current_pos(self):
	# Return the current position of the selector on the screen (0 - 5)
		return self.setterPos % 5
#----------------------------End Setter Class-------------------------------------#

#----------------------------Push Button Class--------------------------------------#
class PushButton(object):

    def __init__(self, pin_number):
        self.pin_number = pin_number
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_number, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def ButtonDown(self):
        """ This method detects if the button is down
            True  ==> button down
            False ==> button up
        """
        return True if not GPIO.input(self.pin_number) else False

    def ButtonPressed(self):
        """ This method detects if the button is pressed once
            True   ==> button pressed once
            False  ==> button not pressed
        """
        pressed = not GPIO.input(self.pin_number)
        time.sleep(0.02)  # Wait 0.02s for the bouncing effect of physical switches
        return True if pressed else False

    def HoldTime(self):
        """ This method returns the time the button is held down
        """
        # Return 0 is button is not down.
        if not self.ButtonDown():
            return 0
        # Return the time the button is held down.
        else:
            start = time.time()
            while self.ButtonDown():
                time.sleep(0.01)
                # If the button has been holding down for more than 5 seconds
                # break the loop and return the hold time.
                if (time.time() - start) > 5:
                    break
            length = time.time() - start
            return length
#---------------------------End Push Button Class-------------------------------------#			

#----------------------------File IO Functions--------------------------------------#
def InitializeFile():
	# This function creates a file if one does not exist
	# Name of the file is the current time and it's stored in the data folder.
	global filePath, fileName
	if filePath:
		pass
	else:
		fileName = str(datetime.now())
		here = os.path.dirname(os.path.realpath(__file__))
		subdir = "data"
		filePath = os.path.join(here, subdir, fileName)
		# Write the column titles to the file
		with open(filePath, "w") as f:
			f.write("Time" + "," + "Pressure(KPa)" + '\n')

def WriteDataToFile(dataString):
	global filePath
	if filePath:
		with open(filePath, "a") as f:
			f.write(dataString)
	else:
		InitializeFile()
#--------------------------End File IO Functions-----------------------------------#

#--------------------------Sensor Functions----------------------------------------#
def ReadChannel(channelNumber):
	# This one returns the raw readings from a MCP3008 channelNumber
	# Channel numbers are 0 - 7
	return mcp.read_adc(channelNumber)
	
def ReadPressureKPa():
	# This functions reads pressure sensor and returns KPa readings.
	global sensorChannel
	rawReading = ReadChannel(sensorChannel)
	floatRaw = float(rawReading)
	rawVolt = floatRaw * (refVolt) / 1024.0
	pressureMPa = (rawVolt) / 4.0
	return (pressureMPa * 1000.0)
	

	
NGR = Device()
Arrow = Selector(0)

# Initialize Button Objects			
ButtonL = PushButton(L_pin)
ButtonR = PushButton(R_pin)
ButtonU = PushButton(U_pin)
ButtonD = PushButton(D_pin)
ButtonA = PushButton(A_pin)
ButtonB = PushButton(B_pin)

percentage = 0.1

while 1:

	#DrawStatus(0,"Wifi")
	NGR.state.repeat_action() # Do the repeat action for each class first.
	if ButtonU.ButtonPressed():
		NGR.on_button_pressed(Arrow.current_pos(), "U")
	else:
		pass
		
	if ButtonD.ButtonPressed():
		NGR.on_button_pressed(Arrow.current_pos(), "D")
	else:
		pass
		
	if ButtonL.ButtonPressed():
		NGR.on_button_pressed(Arrow.current_pos(), "L")
	else:
		pass
		
	if ButtonR.ButtonPressed():
		NGR.on_button_pressed(Arrow.current_pos(), "R")
	else:
		pass
		
	if ButtonA.ButtonPressed():
		NGR.on_button_pressed(Arrow.current_pos(), "A")
	else:
		pass
	
	if ButtonB.ButtonPressed():
		NGR.on_button_pressed(Arrow.current_pos(), "B")
	else:
		pass
	# print(NGR.state)
	RefreshDisplay()