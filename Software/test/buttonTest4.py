import RPi.GPIO as GPIO

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Input pins:
U_pin = 22

GPIO.setmode(GPIO.BCM)

GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

disp = Adafruit_SSD1306.SSD1306_128_64(None)

disp.begin()

disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0,0,width,height), outline = 0, fill = 0)

font = ImageFont.load_default()

while 1:
	if GPIO.input(not U_pin):
		draw.text((0,-2), "Up button", font = font, fill = 255)