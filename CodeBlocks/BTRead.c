/* Algorithm for sending a file from a master arduino to a slave arduino:
   
   Master side: open the SD card, read test.txt file and send the data stream to slave
   device via HC-05. Repeat the same for mypicture.jpg file. Report any error during
   opening and reading SD card.
   
   Slave side: Keep listening to any incoming messages from master via HC-06. As soon as
   data stream is received, open the SD card, write first file and close. Repeat the same for second file.
   Report any error during opening and writing SD card.
*/

#include<SoftwareSerial.h>
SoftwareSerial sigmaSS(8,9); // RX, TX

#include<SPI.h>
#include<SD.h>
char EOF_MARKER = '$';  //End of file marker. File must contain this character at the end

File myFile;
char ch;
boolean foundEOF = false;

void setup(){
	Serial.begin(9600);
	sigmaSS.begin(9600);
	Serial.print("Initializing SD card...");
	if(!SD.begin(4)){
		Serial.println("Initialization Failed!");
		return;
	}
	Serial.println("initialization done.");
	myFile = SD.open("PC_FILE.txt", O_CREAT | O_TRUNC | O_WRITE);
}

void createStr(){
	foundEOF = false;
	int idx = 0;
	
	while(1){
		if(Serial.available()){
			ch = (char)Serial.read();
			if(ch = '$'){
				Serial.flush();
				if(myFile) myFile.close();
				foundEOF = true;
				break;
			}
			if(myFile) myFile.print((char)ch);
		}
	}
	if(foundEOF){
		Serial.println("Found EOF and Written to SD card");
	}
	else{
		Serial.println("Could not find EOF character in file!!");
	}
	Serial.flush();
}

void loop(){
	if(Serial.available()){
		createStr();
	}
}