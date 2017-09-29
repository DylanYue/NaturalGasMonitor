/******************************************
	This is a sample code for receiving data from bluetooth.
*******************************************/

int counter = 0;
int incomingByte;

void setup(){
	Serial.begin(12500);
}

void loop(){
	// see if there is incoming serial data:
	if (Serial.available() > 0) {
		// read the oldest byte in the serial buffer:
		incomingByte = Serial.read();
		// if it's a capital R, reset the counter
		if (incomingByte == 'R') {
			Serial.println("RESET");
			counter = 0;
		}
	}
	
	Serial.println(counter);
	counter++;
	
	delay(250);
}