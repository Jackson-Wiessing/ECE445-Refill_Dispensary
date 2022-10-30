#include <Wire.h>

/* Software for Refill Dispensary */
#define PRESSED 1 
#define RELEASED 0 // probs don't need this at all 

/* UI components */
#define pot_1 32 // for user selection 1
#define pot_2 34 // for user selection 2

#define button_1 12 // for user selection 1
#define button_2 14 // for user selection 2
#define reset_button 15 // resets the entire machine

#define green_status  16 // machine status LEDs
#define yellow_status  17
#define red_status  19

/* Screen */
#define screen_data  4 // data line for communicating between screen & microcontroller
#define screen_clock  5

/* Dispensing part */
#define load_cell  31// will send values to microcontroller
#define valve_1  1
#define valve_2  2


#define Screen_addr 0x78



enum State {Wait, Dispense, Debug};
State curState;

void setup() {
  // ***** might need to add something else for PWM vs Analog or whatever ..... *******
  // put your setup code here, to run once:
  int button_1_state,button_2_state,reset_state,pot_1_state,pot_2_state = 0; 
  pinMode(pot_1, INPUT);
  pinMode(pot_2, INPUT);

  pinMode(button_1, INPUT);
  pinMode(button_2, INPUT);
  pinMode(reset_button, INPUT);

  pinMode(screen_data, OUTPUT);
  pinMode(screen_clock, OUTPUT);
  
  pinMode(green_status, OUTPUT);
  pinMode(yellow_status, OUTPUT);
  pinMode(red_status, OUTPUT);

  pinMode(load_cell, INPUT);

  pinMode(valve_1, OUTPUT);
  pinMode(valve_2, OUTPUT);

  Serial.begin(9600); // starts communication through the USB connection at a baud rate of 9600
  Screen();
}

/* The goal of this function is to let us know if we're properly understanding how the buttons work */
void doButtonsWork() {
  int button_1_state = digitalRead(button_1);
  int button_2_state = digitalRead(button_2);
  int count = 0;
  while(count < 5) {
    if (button_1_state == PRESSED) {
      Serial.println("button 1 pressed");
      count ++;
    }
    if (button_2_state == PRESSED) {
      Serial.println("button 2 pressed");
      count ++;
    }
  }
}
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
void doButtonsWithPotsWork() {
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

/* setsup screen to write to*/
void Screen() {
  setSDA(screen_data);
  setSCL(screen_clock);
  Wire1.begin(Screen_addr);
}

void refillDispensary() {
  int button_1_state = digitalRead(button_1);
  int button_2_state = digitalRead(button_2);
  while (button_1_state != PRESSED && button_2_state != PRESSED) {
    int pot_1_state = analogRead(pot_1);
    int pot_2_state = analogRead(pot_2);
    // need unit tests to work first before continuing 
  }
}
void LEDS(int green,int yellow,int red){
  digitalWrite(green_status,green);
  digitalWrite(yellow_status,yellow);
  digitalWrite(red_status,red);
}

void loop() {
  switch curState{
    case Wait:
      LEDS(1,0,0); //green
      button_1_state = digitalRead(button_1);
      button_2_state = digitalRead(button_2);
      reset_state =  digitalRead(reset_button);
      pot_1_state = analogRead(pot_1);
      pot_2_state = analogRead(pot_2);

      digitalWrite(valve_1,LOW); //ensure that valves are closed
      digitalWrite(valve_2,LOW);
      
      
      break;
    case Dispense:
      LEDS(0,1,0);  //yellow
      break;
    case Debug:
      LEDS(0,0,1); //red
      break;

    default:
      break;
  }


}
