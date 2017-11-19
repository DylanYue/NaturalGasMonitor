class Sensor(object):
	
	def __init__(self, pinNumber):
		self.pinNumber = pinNumber
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pinNumber, GPIO.IN)