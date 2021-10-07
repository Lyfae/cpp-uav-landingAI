#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10); // CE, CSN         
const byte address[6] = "00001";     //Byte of array representing the address. This is the address where we will send the data. This should be same on the receiving side.

unsigned long lastReceiveTime = 0;
unsigned long currentTime = 0;

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

CMD_Packet packet;

void resetData() {
  // Reset the values when there is no radio connection - Set initial default values
  packet.testElement = 0;
  packet.LButton = 1;
  packet.RButton = 1;
  packet.LStickX = 127;
  packet.LStickY = 127;
  packet.RStickX = 127;
  packet.RStickY = 127;
  packet.LTrim = 127;
  packet.RTrim = 127;
}

void setup() {
  Serial.begin(115200);
  radio.begin();                  //Starting the Wireless communication
  radio.openReadingPipe(0, address); //Setting the address where we will send the data
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
  resetData();
}

void loop() {
  if (radio.available()) {
    radio.read(&packet, sizeof(CMD_Packet));

    Serial.println("------------Controller Values------------");
    Serial.print("LStickX: ");
    Serial.print(packet.LStickX);
    Serial.print("; LStickY: ");
    Serial.print(packet.LStickY);
    Serial.print("; LButton: ");
    Serial.println(packet.LButton);
    Serial.print("RStickX: ");
    Serial.print(packet.RStickX); 
    Serial.print("; RStickY: ");
    Serial.print(packet.RStickY);
    Serial.print("; RButton: ");
    Serial.println(packet.RButton);
    Serial.print("LTrim: ");
    Serial.print(packet.LTrim); 
    Serial.print("; RTrim: ");
    Serial.println(packet.RTrim);
    Serial.println();

    /* DUMB WAY BUT IT WORKS (for time management purposes only)
    int packetlength = 9;
    String sendPacket[packetlength];

    sendPacket[0] = "Data Values:";
    sendPacket[1] = String(packet.LStickX);
    sendPacket[2] = String(packet.LStickY);
    sendPacket[3] = String(packet.LButton);
    sendPacket[4] = String(packet.RStickX);
    sendPacket[5] = String(packet.RStickY);
    sendPacket[6] = String(packet.RButton);
    sendPacket[7] = String(packet.LTrim);
    sendPacket[8] = String(packet.RTrim);

    String output;
    for (int i = 0; i < packetlength; i++)
    {
      output += sendPacket[i] + " ";
    }
    Serial.println(output);
    */
    
    delay(500);
  }

  currentTime = millis();
  if ( currentTime - lastReceiveTime > 1000 ) { // If current time is more then 1 second since we have recived the last data, that means we have lost connection
    resetData(); // If connection is lost, reset the data. It prevents unwanted behavior, for example if a drone has a throttle up and we lose connection, it can keep flying unless we reset the values
  }
}
