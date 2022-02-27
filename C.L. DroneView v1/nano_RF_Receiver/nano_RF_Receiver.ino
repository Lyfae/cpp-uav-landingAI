#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// Set up PPM Enoder PWM Pins
const int in1_roll = 3;
const int in2_pitch = 9;
const int in3_throttle = 5;
const int in4_yaw = 10;

// Set Up RF Pins and External Information
RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00501";
const uint8_t  channel = 122;

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

// Data Array
const int len = 8;
int sensorData[len];

// Max size 32 bytes because of buffer limit
struct CMD_Packet {
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

    // Halve frequency on pin 5 to 480Hz to account for PWM frequency difference
    TCCR0B = (1 << CS01) | (1 << CS00); // 0x03, x64
    TCCR0A = (1 << WGM00); // 0x01, phase correct

    // Describe Input Pins
    pinMode(in1_roll, OUTPUT);
    pinMode(in2_pitch, OUTPUT);
    pinMode(in3_throttle, OUTPUT);
    pinMode(in4_yaw, OUTPUT);

    // Set all PWM to zero initially (IMPORTANT)
    analogWrite(in1_roll, 0);
    analogWrite(in2_pitch, 0);
    analogWrite(in3_throttle, 0);
    analogWrite(in4_yaw, 0);

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

    // Map Joystick Values so that they are between 5-250
    packet.LStickX = map(packet.LStickX, 0, 255, 115, 250);
    packet.LTrim = map(packet.LTrim, 0, 255, 115, 250); // throttle (SPECIAL ONE) [Uses left pot for accuracy]
    packet.RStickX = map(packet.RStickX, 0, 255, 115, 250);
    packet.RStickY = map(packet.RStickY, 0, 255, 115, 250);

    // Place data from the transmitter module into array
    sensorData[0] = packet.LStickX;   // Left Stick X Axis
    sensorData[1] = packet.LStickY;   // Left Stick Y Axis
    sensorData[2] = packet.LButton;   // Left Button
    sensorData[3] = packet.RStickX;   // Right Stick X Axis
    sensorData[4] = packet.RStickY;   // Right Stick Y Axis
    sensorData[5] = packet.RButton;   // Right Button
    sensorData[6] = packet.LTrim;     // Left Pot
    sensorData[7] = packet.RTrim;     // Right Pot


    // Check for Toggle Buttons (Left = lock toggle for safety)
    if (!packet.LButton) // If button is pressed | button = LOW
    {
        if (prevLButton != packet.LButton) // Check to see if it was a held button (prevvalue)
        {
        lockThrottle = !lockThrottle; // If it was different value turn lock variable on
        prevLButton = packet.LButton; // Set the prev value to ON position to prevent hold
        lockThrottleValue = packet.LTrim;
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
    if (panicButton || piControl)
    {
        // Set all PWM to zero for out of control drone
        analogWrite(in1_roll, 115);
        analogWrite(in2_pitch, 115);
        analogWrite(in3_throttle, 115);
        analogWrite(in4_yaw, 115);
        sensorData[0] = 115; // FOR TESTING PURPOSES ONLY!!!
        sensorData[6] = 115; // FOR TESTING PURPOSES ONLY!!!
        sensorData[3] = 115; // FOR TESTING PURPOSES ONLY!!!
        sensorData[4] = 115; // FOR TESTING PURPOSES ONLY!!!
    }
    else if (lockThrottle) // Lock throttle to current value, lock the rest to 50% duty cycle
    {
        analogWrite(in1_roll, 182);
        analogWrite(in2_pitch, 182);
        analogWrite(in3_throttle, lockThrottleValue);
        analogWrite(in4_yaw, 182);
        sensorData[0] = 182; // FOR TESTING PURPOSES ONLY!!!
        sensorData[6] = lockThrottleValue; // FOR TESTING PURPOSES ONLY!!!
        sensorData[3] = 182; // FOR TESTING PURPOSES ONLY!!!
        sensorData[4] = 182; // FOR TESTING PURPOSES ONLY!!!
    }
    else
    {
        // Assign controller values to PPM Encoder 1:1 ratio
        analogWrite(in1_roll, packet.RStickY);
        analogWrite(in2_pitch, packet.RStickX);
        analogWrite(in3_throttle, packet.LTrim);
        analogWrite(in4_yaw, packet.LStickX);
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
    // Set all PWM to zero as last resort (INSERT GOOD LANDING PROCEDURE HERE LATER)
    analogWrite(in1_roll, 5);
    analogWrite(in2_pitch, 5);
    analogWrite(in3_throttle, 5);
    analogWrite(in4_yaw, 5);
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
    packet.LButton = 1;
    packet.RButton = 1;
    packet.LStickX = 182;
    packet.LStickY = 182;
    packet.RStickX = 182;
    packet.RStickY = 182;
    packet.LTrim = 182;
    packet.RTrim = 182;
}
