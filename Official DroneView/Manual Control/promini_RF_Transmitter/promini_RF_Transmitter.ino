/*
* Cheap Controller
*     Revision 0.3
*                
* by Christopher J. Watson
* 
* Library: TMRh20/RF24, https://github.com/tmrh20/RF24/
*/
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
RF24 radio(2, 10); // CE, CSN
const byte address[6] = "00501";
const uint8_t  channel = 122;
//Low End 461
//High End 1003
const int LOW_END = 461;
const int HIGH_END = 1003;
//Guess Values For Baby Mode
const int LOW_END_BBY = 602;
const int HIGH_END_BBY = 862;



// Define the digital inputs
#define lBTN 3  // Joystick button 1
#define rBTN 8  // Joystick button 2
#define BBYMode 9 // Switch 1

// Max size 32 bytes because of buffer limit
struct CMD_Packet {
  byte LButton;
  byte RButton;
  byte LStickXL;
  byte LStickXH;
  byte LStickYL;
  byte LStickYH;
  byte RStickXL;
  byte RStickXH;
  byte RStickYL;
  byte RStickYH;
  byte LTrimL;
  byte LTrimH;
  byte RTrimL;
  byte RTrimH;
  byte BbyMode;
};

//Make command packet
CMD_Packet packet;

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_LOW,0);
  radio.setChannel(channel);
  radio.stopListening();
  Serial.println("Sending");
  
  //Set Up Controls
  pinMode(lBTN, INPUT_PULLUP);
  pinMode(rBTN, INPUT_PULLUP);
  pinMode(BBYMode, INPUT_PULLUP);
}



void loop() {
  //map vals
  int highmap = 0;
  int lowmap = 0;
  //temp vals
  int tempx = 0;
  int tempy = 0;
  
  //If baby mode, go easy
  if(digitalRead(BBYMode)==0){
    highmap = HIGH_END_BBY;
    lowmap = LOW_END_BBY;
  }else{
    highmap = HIGH_END;
    lowmap = LOW_END;
  }
  
  // Read all analog inputs and map them to one Byte value
  //Gather Left Stick Values
  tempx = map(analogRead(A3),0,1023,lowmap,highmap);
  tempy = (map(analogRead(A2),0,1023,highmap,lowmap));
  packet.LStickXL = (byte)tempx;
  packet.LStickXH = (byte)(tempx>>8);
  packet.LStickYL = (byte)tempy;
  packet.LStickYH = (byte)(tempy>>8);
  //Gather Right Stick Values
  tempx = map(analogRead(A0),0,1023,lowmap,highmap);
  tempy = (map(analogRead(A1),0,1023,highmap,lowmap));
  packet.RStickXL = (byte)tempx;
  packet.RStickXH = (byte)(tempx>>8);
  packet.RStickYL = (byte)tempy;
  packet.RStickYH = (byte)(tempy>>8); 
  //Gather Trim Values
  tempx = map(analogRead(A7),0,1023,LOW_END,HIGH_END);
  tempy = map(analogRead(A6),0,1023,LOW_END,HIGH_END);
  packet.LTrimL = (byte)tempx;
  packet.LTrimH = (byte)(tempx>>8);
  packet.RTrimL = (byte)tempy;
  packet.RTrimH = (byte)(tempy>>8);
  // Read all digital inputs
  packet.LButton = digitalRead(lBTN);
  packet.RButton = digitalRead(rBTN);

  //If baby mode, go easy
  packet.BbyMode = digitalRead(BBYMode);

  // Send the whole data from the structure to the receiver
  radio.write(&packet, sizeof(CMD_Packet));
  
  delay(5);
}
