#include <Wire.h>

/* Software for Refill Dispensary */
#define PRESSED 1 
#define RELEASED 0 // probs don't need this at all 
#define SCREEN_ADDR 0x78

/* UI components */
const int pot_1 = 32; // for user selection 1
const int pot_2 = 34; // for user selection 2

const int button_1 = 12; // for user selection 1
const int button_2 = 14; // for user selection 2
const int reset_button = 15; // resets the entire machine

const int green_led = 16; // machine status LEDs
const int yellow_led = 17;
const int red_led = 19;

/* Screen */
const int screen_data = 4; // data line for communicating between screen & microcontroller
const int screen_clock = 5;

/* Dispensing part */
const int load_cell = 31; // will send values to microcontroller
const int valve_1 = 1;
const int valve_2 = 2;

/* States can be categorized by the following:
Wait  - no buttons have been pressed
      - nothing is being dispensed
      -  green status LED is on
Dispense  - Conditions to check before entering the state: 
            1. button is pressed and the corresponding potentiometer has a non-zero value
            2. previous state was wait
            3. load cell reads a value > X grams -> we originally said 19 grams
          - machine status turns yellow
          - "zeros" out the scale
          - corresponding valve opens
          - constantly checks if the load cell detects a weight within tolerance of requested quantity -> when it does, it stops & closes the valve
Debug - 
*/
enum State {Wait, Dispense, Debug};
State curState;

int button_1_state, button_2_state, reset_state, pot_1_state, pot_2_state = 0; 


/* The goal of this function is to let us know if we're properly understanding how the buttons work */
void getButtons(int * buf){
  int button_1_state = digitalRead(button_1);
  int button_2_state = digitalRead(button_2);
  int reset_state =  digitalRead(reset_button);
  
  if (button_1_state == 1){
      Serial.println("button 1 pressed");
  }
  if (button_2_state == 1){
      Serial.println("button 2 pressed");
  }
  if (reset_state == 1){
    curState = Wait;
  }
}

/* The goal of this function is to figure out the values given by potentiometer readings */
void getPots() {
  int pot_1_state = analogRead(pot_1);
  int pot_2_state = analogRead(pot_2);
  Serial.println("Pot 1 Value: ");
  Serial.println(pot_1_state);
  Serial.println("Pot 2 Value: ");
  Serial.println(pot_2_state);
}

/* Testing for the first part of the pseudocode */
void buttonsWithPots() {
  int button_1_state = digitalRead(button_1);
  int button_2_state = digitalRead(button_2);
  while (button_1_state != PRESSED && button_2_state != PRESSED) {
    int pot_1_state = analogRead(pot_1);
    int pot_2_state = analogRead(pot_2);
    if (pot_1_state > 0 or pot_2_state > 0) {
      Serial.println("Pot 1 Value: ");
      Serial.println(pot_1_state);
      Serial.println("Pot 2 Value: ");
      Serial.println(pot_2_state);
    }
  }  
}

/* Updates the status of the leds */
void updateLEDS(int green_status,int yellow_status,int red_status){
  digitalWrite(green_led, green_status);
  digitalWrite(yellow_led, yellow_status);
  digitalWrite(red_led, red_status);
}

/* setsup screen to write to */
void setupScreen() {
  setSDA(screen_data);
  setSCL(screen_clock);
  Wire1.begin(SCREEN_ADDR);
}

/*
void refillDispensary() {
  int button_1_state = digitalRead(button_1);
  int button_2_state = digitalRead(button_2);
  while (button_1_state != PRESSED && button_2_state != PRESSED) {
    int pot_1_state = analogRead(pot_1);
    int pot_2_state = analogRead(pot_2);
    // need unit tests to work first before continuing 
  }
}
*/ 

void setup() {
  pinMode(pot_1, INPUT);
  pinMode(pot_2, INPUT);

  pinMode(button_1, INPUT);
  pinMode(button_2, INPUT);
  pinMode(reset_button, INPUT);

  pinMode(green_led, OUTPUT);
  pinMode(yellow_led, OUTPUT);
  pinMode(red_led, OUTPUT);

  pinMode(screen_data, OUTPUT);
  pinMode(screen_clock, OUTPUT);

  pinMode(load_cell, INPUT);
  pinMode(valve_1, OUTPUT);
  pinMode(valve_2, OUTPUT);

  Serial.begin(9600); // starts communication through the USB connection at a baud rate of 9600
  setupScreen();
}

void loop() {
  switch curState {
    case Wait:
      updateLEDS(1,0,0); // green
      button_1_state = digitalRead(button_1);
      button_2_state = digitalRead(button_2);
      reset_state =  digitalRead(reset_button);
      pot_1_state = analogRead(pot_1);
      pot_2_state = analogRead(pot_2);

      digitalWrite(valve_1,LOW); //ensure that valves are closed
      digitalWrite(valve_2,LOW);
      
      
      break;
    case Dispense:
      updateLEDS(0,1,0);  //yellow
      break;
    case Debug:
      updateLEDS(0,0,1); //red
      break;

    default:
      break;
  }
}
