#include <Arduino.h> // Standard framework for embedded C++

// Protocol Definition
#define AWAKE_BYTE  0x00   // Received when EAR is above threshold
#define DROWSY_BYTE 0xFF   // Received when EAR is below threshold (Alarm)

// Hardware Mapping
const int BUZZER_PIN = 8; 
const int LED_PIN = 13;

// State Variables
bool isAlarmActive = false;
unsigned long alarmTriggerTime = 0;
const unsigned long MIN_ALARM_TIME = 2000; // Keep alarm on for 2 seconds min

void setup() {
    // Initialize Serial at 9600 baud to match Python script
    Serial.begin(9600);
    
    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(LED_PIN, OUTPUT);
    
    // System Check
    digitalWrite(LED_PIN, HIGH);
    delay(500);
    digitalWrite(LED_PIN, LOW);
}

void loop() {
    // 1. Check for incoming signal from the Python "Sensor"
    if (Serial.available() > 0) {
        uint8_t incomingByte = Serial.read();

        // 2. Logic: Process the Signal
        if (incomingByte == DROWSY_BYTE) {
            isAlarmActive = true;
            alarmTriggerTime = millis(); 
            
            // Trigger physical actuators
            digitalWrite(BUZZER_PIN, HIGH);
            digitalWrite(LED_PIN, HIGH);
        } 
        else if (incomingByte == AWAKE_BYTE) {
            // Only turn off if the 2-second safety window has passed
            if (isAlarmActive && (millis() - alarmTriggerTime >= MIN_ALARM_TIME)) {
                isAlarmActive = false;
                digitalWrite(BUZZER_PIN, LOW);
                digitalWrite(LED_PIN, LOW);
            }
        }
    }
}