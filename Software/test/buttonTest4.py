# -*- coding: UTF-8 -*-
import RPi.GPIO as GPIO

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Input pins:

# Input pins:
L_pin = 27 
R_pin = 23 
C_pin = 4 
U_pin = 17 
D_pin = 22 
 
A_pin = 5 
B_pin = 6 
 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up

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

	
def DrawText(posX, rowNumber, text):
	# posX is the x position of the text
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

# Initialize the selector position	
selectorPos = 0

def SelectorPosConditioner (rawPos):
	# This function always returns the selector's real position on the screen (0 - 5)
	return rawPos % 6

def PlaceSelector(rowNumber):
	DrawText(0, SelectorPosConditioner(rowNumber), "->")


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
        pressed = GPIO.wait_for_edge(self.pin_number, GPIO.FALLING)
        time.sleep(0.15)  # Wait 0.15s for the bouncing effect of physical switches
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

# Initialize Button Objects			
ButtonL = PushButton(L_pin)
ButtonR = PushButton(R_pin)
ButtonU = PushButton(U_pin)
ButtonD = PushButton(D_pin)
ButtonA = PushButton(A_pin)
ButtonB = PushButton(B_pin)

while 1:
			
	if not ButtonD.ButtonPressed():
		ClearScreen()
		selectorPos += 1
		PlaceSelector(selectorPos)
		DrawText(14, 2, "Down button");
		
	if not ButtonU.BottonPressed():
		ClearScreen()
		selectorPos -= 1
		PlaceSelector(selectorPos)
		DrawText(14, 3, "Up button");
	RefreshDisplay()