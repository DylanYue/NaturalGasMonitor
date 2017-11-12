import RPi.GPIO as GPIO
import time

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
        time.sleep(0.45)  # Wait 0.25s for the bouncing effect of physical switches
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