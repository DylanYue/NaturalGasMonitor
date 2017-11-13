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


def RefreshDisplay():
	disp.image(image)
	disp.display()

def ClearScreen():
	draw.rectangle((0, 0, width, height), outline = 0, fill = 0)

def ClearTextArea():
	draw.rectangle((0, 0, width, 60), outline = 0, fill = 0)

def ClearBatArea():
	draw.rectangle((0, 61, width, height), outline = 0, fill = 0)

	
def DrawText(rowNumber, text):
	# The X position of text is 14
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
	
	draw.text((14, posY), text, font = font, fill = 255)
	
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
	
	draw.text((100, posY), text, font = font, fill = 255)
	
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


# Initialize Button Objects			
ButtonL = PushButton(L_pin)
ButtonR = PushButton(R_pin)
ButtonU = PushButton(U_pin)
ButtonD = PushButton(D_pin)
ButtonA = PushButton(A_pin)
ButtonB = PushButton(B_pin)

percentage = 0.1
while 1:
	DrawBatteryStatus(percentage)
	draw.rectangle((100, 0, width, 60), outline = 1, fill = 0)
	if ButtonL.ButtonPressed():
		ClearTextArea()
		selectorPos += 1
		PlaceSelector(selectorPos)
		DrawText(14, 2, "Left button");
	else:
		pass
		
	if ButtonA.ButtonPressed():
		ClearTextArea()
		percentage += 0.05
		DrawText(14, 5, "A button");
	else:
		pass
	RefreshDisplay()