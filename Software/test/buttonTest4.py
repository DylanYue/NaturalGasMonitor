# -*- coding: UTF-8 -*-

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PushButton import PushButton

# Text area of the screen starts from (0, 0) to (width, 60)
# Battery status area of the screen starts from (0, 61) to (width, height)

# Input pins:
L_pin = 27 
R_pin = 23 
C_pin = 4 
U_pin = 17 
D_pin = 22 
A_pin = 5 
B_pin = 6 

# Raspberry Pi pin configuration:
RST = None
 
# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

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
	disp.image(image)
	disp.display()

def ClearScreen():
	draw.rectangle((0, 0, width, height), outline = 0, fill = 0)

def ClearSelector():
	draw.rectangle((0, 0, 13, 60), outline = 0, fill = 0)
	
def ClearTextArea():
	draw.rectangle((14, 0, width, 60), outline = 0, fill = 0)

def ClearBatArea():
	draw.rectangle((0, 61, width, height), outline = 0, fill = 0)

	
def DrawText(posX, rowNumber, text):
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
	batWidth = batPercent * width
	draw.rectangle((0, 61, batWidth, height), outline = 0, fill = 255)

# Initialize the selector position	
selectorPos = 0

def SelectorPosConditioner (rawPos):
	# This function always returns the selector's real position on the screen (0 - 5)
	return rawPos % 6

def PlaceSelector(rowNumber):
	DrawText(0, SelectorPosConditioner(rowNumber), "->")
#--------------------------------------END OLED Functions-----------------------------------------------#

# Initialize Button Objects			
ButtonL = PushButton(L_pin)
ButtonR = PushButton(R_pin)
ButtonU = PushButton(U_pin)
ButtonD = PushButton(D_pin)
ButtonA = PushButton(A_pin)
ButtonB = PushButton(B_pin)

# List of menu ids and menu titles for each menu level
menuLevel1 = [[1, "Sensor"], [2, "Wifi"], [3, "Battery"], [4, "Time"], [5, "SD Card"]]
menuLevel12 = [[11, "Start Rec"], [12, "Stop Rec"], [13, "Calibrate"], [14, "Live Reading"]]
menuLevel22 = [[21, "Turn On"], [22, "Turn Off"]]
menuLevel32 = [[31, "Display Capacity"]]
menuLevel42 = [[41, "Set Time"], [42, "Display"]]
menuLevel52 = [[51, "Capacity"]]

class MenuItem(object):
    
    def __init__(self, menuID, menuTitle):
        self.menuID = menuID
        self.menuTitle = menuTitle

    def stringForDisplay(self):
        return self.menuTitle
    
    def getMenuID(self):
        return self.menuID
    
    # This method returns the menu's location on the screen (1, 2, 3...)
    def getMenuLocation(self):
        return (self.menuID % 10)
    
# Initialize menu items

def menuListGenerator(menuLevelList):
    menuItems = []
    for menu in menuLevelList:
        menuItem = MenuItem(menu[0], menu[1])
        menuItems.append(menuItem)
    return menuItems

menuItems1 = menuListGenerator(menuLevel1)
menuItems12 = menuListGenerator(menuLevel12)
menuItems22 = menuListGenerator(menuLevel22)
menuItems32 = menuListGenerator(menuLevel32)
menuItems42 = menuListGenerator(menuLevel42)
menuItems52 = menuListGenerator(menuLevel52)

#------------------------------	State Machine Code-----------------------------------------------------
class State(object):
	def __init__(self):
		pass


class InitialState(State):
    # The state which indicates that there are limited device capabilities
    def __init__(self):
		ClearTextArea()
		DrawText(14, 0, "Sensor")
		DrawText(14, 1, "Wifi")
		DrawText(14, 2, "Battery")
		DrawText(14, 3, "Time")
		DrawText(14, 4, "SD Card")
        
    def on_button_pressed(self, selector_pos, button):
		if selector_pos == 0 and button == "A":
			return SensorState()
		else:
			pass
		if selector_pos == 1 and button == "A":
			return WifiState()
		else:
			pass
		if selector_pos == 2 and button == "A":
			return BatteryState()
		else:
			pass
		if selector_pos == 3 and button == "A":
			return TimeState()
		else:
			pass
		if selector_pos == 4 and button == "A":
			return SDCardState()
		else:
			pass
		
		return self
        
    def display(self):
        print("Sensor")
        print("Wifi")
        print("Battery")
        print("Time")
        print("SD Card")
    
class SensorState(State):
    # The state which indicates that there are no limitations on device capabilities
    
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
			
		return self


class RecordingState(State):
    def __init__(self):
		ClearTextArea()
		DrawText(14, 0, "Recording...")

    def on_button_pressed(self, selector_pos, button):
        if button == "B":
            return SensorState()
		# return self

class Device(object):
	
	def __init__(self):
		self.state = InitialState()
	
	def on_button_pressed(self, selector_pos, button):
		self.state = self.state.on_button_pressed(selector_pos, button)

#--------------------------------------------------------------------------------#

#-----------------------------Selector Class-------------------------------------#

class Selector(object):
	# Selector class to store the information of the selector
	def __init__(self, selectorPos):
		ClearSelector()
		self.selectorPos = selectorPos
		PlaceSelector(self.selectorPos)
		
	def move_up(self):
		ClearSelector()
		self.selectorPos -= 1
		PlaceSelector(self.selectorPos)
		
	def move_down(self):
		ClearSelector()
		self.selectorPos += 1
		PlaceSelector(self.selectorPos)
		
	def selector_reset(self):
		ClearSelector()
		self.selectorPos = 0
		PlaceSelector(self.selectorPos)
		
	def current_pos(self):
		return self.selectorPos % 6



	
	
	
	
	
NGR = Device()
Arrow = Selector(0)

percentage = 0.1

while 1:

	DrawStatus(0,"Wifi")
	if ButtonU.ButtonPressed():
		Arrow.move_up()
	else:
		pass
		
	if ButtonD.ButtonPressed():
		Arrow.move_down()
	else:
		pass
		
	if ButtonA.ButtonPressed():
		NGR.state.on_button_pressed(Arrow.current_pos(), "A")
	else:
		pass
	
	if ButtonB.ButtonPressed():
		NGR.state.on_button_pressed(Arrow.current_pos(), "B")
	else:
		pass
	print NGR.state
	RefreshDisplay()