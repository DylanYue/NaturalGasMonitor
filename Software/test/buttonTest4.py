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

font = ImageFont.load_default()

while 1:
	draw.rectangle((0,0,width,height), outline = 0, fill = 0)
	
	if not GPIO.input(U_pin):
		draw.text((0,-2), "你好", font = font, fill = 255)
		draw.text((2,10), "Test", font = font, fill = 255)
	else:
		draw.text((0,-2), "Hehe", font = font, fill = 255)
		
	disp.image(image)
	disp.display()