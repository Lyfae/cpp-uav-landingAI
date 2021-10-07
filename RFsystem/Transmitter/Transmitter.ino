#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10); // CE, CSN         
const byte address[6] = "00001";     //Byte of array representing the address. This is the address where we will send the data. This should be same on the receiving side.

// Define the digital inputs
#define lBTN 2  // Joystick button 1
#define rBTN 3  // Joystick button 2

// Max size 32 bytes because of buffer limit
struct CMD_Packet {
  byte testElement;
  byte LButton;
  byte RButton;
  byte LStickX;
  byte LStickY;
  byte RStickX;
  byte RStickY;
  byte LTrim;
  byte RTrim;
};

//Make command packet
CMD_Packet packet;

void setup() {
  Serial.begin(115200);
  radio.begin();                  //Starting the Wireless communication
  radio.openWritingPipe(address); //Setting the address where we will send the data
  radio.setPALevel(RF24_PA_MIN);  //You can set it as minimum or maximum depending on the distance between the transmitter and receiver.
  radio.stopListening();          //This sets the module as transmitter

  //Set Up Controls
  pinMode(lBTN, INPUT_PULLUP);
  pinMode(rBTN, INPUT_PULLUP);
}

void loop()
{
  // Define Test Byte as Arbritrary Number
  packet.testElement = 420;
  
  // Read all analog inputs and map them to one Byte value
  packet.LStickX = map(analogRead(A4), 0, 1023, 255, 0);
  packet.LStickY = map(analogRead(A5), 0, 1023, 255, 0);
  packet.RStickX = map(analogRead(A2), 0, 1023, 255, 0);
  packet.RStickY = map(analogRead(A3), 0, 1023, 255, 0);
  packet.LTrim = map(analogRead(A7), 0, 1023, 0, 255);
  packet.RTrim = map(analogRead(A6), 0, 1023, 0, 255);

  // Read all digital inputs
  packet.LButton = digitalRead(lBTN);
  packet.RButton = digitalRead(rBTN);

  // Send the whole data from the structure to the receiver
  radio.write(&packet, sizeof(CMD_Packet));
}
