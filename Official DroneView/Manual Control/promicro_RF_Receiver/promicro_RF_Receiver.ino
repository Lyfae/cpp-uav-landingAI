#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// Set up PPM Enoder PWM Pins
const int in1_roll = 5;
const int in2_pitch = 6;
const int in3_throttle = 9;
const int in4_yaw = 10;
const int in5_flightmodes = 3;

// Set Up RF Pins and External Information
RF24 radio(2, 4); // CE, CSN
const byte address[6] = "00501";
const uint8_t  channel = 122;

// Set Up Camera Gimbal Pins
const int servo_pan = 7;
const int servo_tilt = 8;

// Tranciever Timeout Control Variables
unsigned long lastReceiveTime = 0;
unsigned long currentTime = 0;

// Toggle Button Variables
bool lockThrottle = false;
bool panicButton = false;
int prevLButton = 1;
int prevRButton = 1;
int lockThrottleValue = 0;
bool piControl = false;

// Tested Control Values
// Low End 461 || High End 1003
const int LOW_END = 461;
const int HIGH_END = 1003;
const int MID_VAL = (HIGH_END + LOW_END) / 2;
//Guess Values For Baby Mode
const int LOW_END_BBY = 602;
const int HIGH_END_BBY = 862;

// Data Array
const int len = 9;
int sensorData[len];

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

CMD_Packet packet;

void setup() {
    // Set Up Serial Comms - Debug
    Serial.begin(9600);

    Serial.println("PIO Worked!");

    // Set up Radio
    radio.begin();
    radio.openReadingPipe(1, address);
    radio.setPALevel(RF24_PA_MIN,0);
    radio.setChannel(channel);
    Serial.println("Starting Radio");
    resetData(); 
    radio.startListening();

    // Halve frequency on pin 3 to 480Hz to account for PWM frequency difference
    TCCR0B = (1 << CS01) | (1 << CS00); // 0x03, x64
    TCCR0A = (1 << WGM00); // 0x01, phase correct

    // Describe Input Pins
    pinMode(in1_roll, OUTPUT);
    pinMode(in2_pitch, OUTPUT);
    pinMode(in3_throttle, OUTPUT);
    pinMode(in4_yaw, OUTPUT);
    pinMode(in5_flightmodes, OUTPUT);

    pinMode(servo_pan, OUTPUT);
    pinMode(servo_tilt, OUTPUT);

    // Set all PWM to lowest initially (IMPORTANT)
    analogWrite(in1_roll, 0);
    analogWrite(in2_pitch, 0);
    analogWrite(in3_throttle, 0);
    analogWrite(in4_yaw, 0);
    analogWrite(in5_flightmodes, 0);

    // Fill Data Array With Dummy Data
    for (int i = 0; i < len; i++)
    {
    sensorData[i] = 0;
    }
}
void loop() {
    // Check Serial for RPi Inputs
    RPiSerial();

    if (radio.available()) {
    radio.read(&packet, sizeof(CMD_Packet));

    // Place data from the transmitter module into array
    sensorData[0] = packet.LStickXL | ((packet.LStickXH&0x03)<<8);   // Left Stick X Axis
    sensorData[1] = packet.LStickYL | ((packet.LStickYH&0x03)<<8);   // Left Stick Y Axis
    sensorData[2] = packet.LButton;   // Left Button
    sensorData[3] = packet.RStickXL | ((packet.RStickXH&0x03)<<8);   // Right Stick X Axis
    sensorData[4] = packet.RStickYL | ((packet.RStickYH&0x03)<<8);   // Right Stick Y Axis
    sensorData[5] = packet.RButton;   // Right Button
    sensorData[6] = packet.LTrimL | ((packet.LTrimH&0x03)<<8);     // Left Pot
    sensorData[7] = packet.RTrimL | ((packet.RTrimH&0x03)<<8);     // Right Pot
    sensorData[8] = packet.BbyMode;


    // Check for Toggle Buttons (Left = lock toggle for safety)
    if (!packet.LButton) // If button is pressed | button = LOW
    {
        if (prevLButton != packet.LButton) // Check to see if it was a held button (prevvalue)
        {
        lockThrottle = !lockThrottle; // If it was different value turn lock variable on
        prevLButton = packet.LButton; // Set the prev value to ON position to prevent hold
        lockThrottleValue = sensorData[6]; // packet.Ltrim
        }
    }
    else
    {
        prevLButton = packet.LButton; // If button released, then set prev value back to 1
    }

    // Check Toggle Buttons (Right = PANIC BUTTON)
    if (!packet.RButton)
    {
        if (prevRButton != packet.RButton)
        {
        panicButton = !panicButton;
        prevRButton = packet.RButton;
        }
    }
    else
    {
        prevRButton = packet.RButton;
    }

    // Initiate lockthrottle and panicbutton modes
    if (panicButton)
    {
        // Set all PWM to zero for out of control drone
        analogWrite(in1_roll, LOW_END);
        analogWrite(in2_pitch, LOW_END);
        analogWrite(in3_throttle, LOW_END);
        analogWrite(in4_yaw, LOW_END);
        sensorData[0] = LOW_END; // FOR TESTING PURPOSES ONLY!!!
        sensorData[6] = LOW_END; // FOR TESTING PURPOSES ONLY!!!
        sensorData[3] = LOW_END; // FOR TESTING PURPOSES ONLY!!!
        sensorData[4] = LOW_END; // FOR TESTING PURPOSES ONLY!!!
    }
    else if (lockThrottle || piControl) // Lock throttle to current value, lock the rest to 50% duty cycle
    {
        analogWrite(in1_roll, MID_VAL);
        analogWrite(in2_pitch, MID_VAL);
        analogWrite(in3_throttle, lockThrottleValue);
        analogWrite(in4_yaw, MID_VAL);
        sensorData[0] = MID_VAL; // FOR TESTING PURPOSES ONLY!!!
        sensorData[6] = lockThrottleValue; // FOR TESTING PURPOSES ONLY!!!
        sensorData[3] = MID_VAL; // FOR TESTING PURPOSES ONLY!!!
        sensorData[4] = MID_VAL; // FOR TESTING PURPOSES ONLY!!!
    }
    else
    {
        // Assign controller values to PPM Encoder 1:1 ratio
        analogWrite(in1_roll, sensorData[4]);
        analogWrite(in2_pitch, sensorData[3]);
        analogWrite(in3_throttle, sensorData[6]); // LTrim
        analogWrite(in4_yaw, sensorData[0]);
        analogWrite(in5_flightmodes, map(sensorData[7],0,1023,115,250)); // RTrim
    }

    // Print array of information into Serial Monitor
    String printString = "";
    for (int i = 0; i < len; i++)
    {
        printString += String(sensorData[i]) + " ";
    }
    Serial.println(printString);
    delay(50);
    }
    else
    {
    // Throttle lock as last resort (INSERT GOOD LANDING PROCEDURE HERE LATER)
    analogWrite(in1_roll, MID_VAL);
    analogWrite(in2_pitch, MID_VAL);
    analogWrite(in3_throttle, MID_VAL - 100);
    analogWrite(in4_yaw, MID_VAL);
    }

    currentTime = millis();
    if ( currentTime - lastReceiveTime > 1000 ) { // If current time is more then 1 second since we have recived the last data, that means we have lost connection
    resetData(); // If connection is lost, reset the data. It prevents unwanted behavior, for example if a drone has a throttle up and we lose connection, it can keep flying unless we reset the values
    }
}

// [Function] Checks to see if serial data has been recieved from the Raspberry Pi
void RPiSerial()
{
    if (Serial.available() > 0)
    {
        char command = Serial.read();
        if (command == 'y')
        {
            Serial.println("Detected! Auto-Panic Mode Toggled!");
            piControl = !piControl;
        }
    }
}

// [Function] Reset data when there is no radio connection - Set initial default values
void resetData() {
  // Reset the values when there is no radio connection - Set initial default values
  packet.LButton = 1;
  packet.RButton = 1;
  packet.LStickXL = 0xFF;
  packet.LStickYL = 0xFF;
  packet.RStickXL = 0xFF;
  packet.RStickYL = 0xFF;
  packet.LTrimL = 0xFF;
  packet.RTrimL = 0xFF;
  packet.LStickXH = 0x01;
  packet.LStickYH = 0x01;
  packet.RStickXH = 0x01;
  packet.RStickYH = 0x01;
  packet.LTrimH = 0x01;
  packet.RTrimH = 0x01;
}
