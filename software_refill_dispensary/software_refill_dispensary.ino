#include <Wire.h>

/* Software for Refill Dispensary */
#define PRESSED 1 
#define SCREEN_ADDR 0x78
#define OVERFLOW -1
#define SUCCESS 0 
#define OUTOFSTOCK 1

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
const int screen_data = 2; // data line for communicating between screen & microcontroller  -> was pin 4
const int screen_clock = 3; // was pin 5

/* Dispensing part */
const int load_cell = 31; // will send values to microcontroller
const int valve_1 = 1;
const int valve_2 = 2;

/* States can be categorized by the following:
Wait  - no buttons have been pressed
      - nothing is being dispensed
      - green status LED is on
      - screen value changes as potentiometers are turned
      - Conditions to check before entering the state: 
            1. button is pressed and the corresponding potentiometer has a non-zero value
            2. previous state was wait
            3. load cell reads a value > X grams -> we originally said 19 grams
Dispense  - machine status turns yellow
          - "zeros" out the scale
          - corresponding valve opens
          - updates the screen every few seconds
          - if the weight isn't changing after 10 seconds -> enter Debug mode bc something is out of stock 
          - if weight gets picked up -> immediately stop!
          - constantly checks if the load cell detects a weight within tolerance of requested quantity 
              ---> when it does, it stops & closes the valve
            - ensures that there's no overflow otherwise it will move into the debug state
Debug - machine status is red
      - all button presses and potentiometer spins get ignored until the reset button is hit
*/
enum State {Wait, Dispense, Debug};

/* Tracks the current state of the machine */
State curState;

/* Screen will be updating periodically to keep the user informed
Normal - Selected Product X, Quantity = Y
NoContainer - Error: Must Place Container!
NoQuantity - Error: Must Select Quantity!
*/
enum ScreenText {Normal, NoContainer, NoQuantity};
ScreenText curText;

/* Initialize all UI components to off or 0 */
int button_1_state, button_2_state, reset_state, pot_1_state, pot_2_state = 0; 

/* Keeps track of the weight to dispense */
int weight = 0; 

/* TESTING - The goal of this function is to let us know if we're properly understanding how the buttons work */
void readButtons(int * buf){
  int but_1_state = digitalRead(button_1);
  int but_2_state = digitalRead(button_2);
  int res_state =  digitalRead(reset_button);
  
  if (but_1_state == 1){
      Serial.println("button 1 pressed");
  }
  if (but_2_state == 1){
      Serial.println("button 2 pressed");
  }
  if (res_state == 1){
    Serial.println("reset pressed");
  }
}

/* TESTING - The goal of this function is to figure out the values given by potentiometer readings */
void readPots() {
  int p_1_state = analogRead(pot_1);
  int p_2_state = analogRead(pot_2);
  Serial.println("Pot 1 Value: ");
  Serial.println(p_1_state);
  Serial.println("Pot 2 Value: ");
  Serial.println(p_2_state);
}

/* TESTING - Testing for the first part of the pseudocode */
void doButtonsAndPotsWork() {
  int but_1_state = digitalRead(button_1);
  int but_2_state = digitalRead(button_2);
  int p_1_state = analogRead(pot_1);
  int p_2_state = analogRead(pot_2);

  if (but_1_state == PRESSED && p_1_state > 0) {
    Serial.println("Pot 1 Value: ");
    Serial.println(p_1_state);
    digitalWrite(LED_BUILTIN, HIGH);
  }
  else if (but_2_state == PRESSED && p_2_state > 0) {
    Serial.println("Pot 2 Value: ");
    Serial.println(p_2_state);
    digitalWrite(LED_BUILTIN, HIGH);
  }

  delay(100);
  digitalWrite(LED_BUILTIN, LOW);
}

/* Updates the status of the leds */
void updateLEDS(int green_status, int yellow_status, int red_status){
  digitalWrite(green_led, green_status);
  digitalWrite(yellow_led, yellow_status);
  digitalWrite(red_led, red_status);
}

/* Setsup screen to write to */
void setupScreen() { // recheck the pins for SDA or SCL
/*
  Wire.setSDA(screen_data); // the 3 of these were previously Wire1
  Wire.setSCL(screen_clock);
  Wire.begin(SCREEN_ADDR); 
  */
}

/* Gets the status of the buttons & potentiometers */
void readUI() {
  button_1_state = digitalRead(button_1);
  button_2_state = digitalRead(button_2);
  pot_1_state = analogRead(pot_1);
  pot_2_state = analogRead(pot_2);
  reset_state = analogRead(reset_button);
}

// enum ScreenText {Normal, NoContainer, NoQuantity};
/* */
void updateScreen(ScreenText text) {
  switch (text) {
    case Normal:
      // Selected Product X, Quantity = Y 
      break;
      
    case NoContainer: 
      // Error: Must Place Container!
      break;

    case NoQuantity:
      // Error: Must Select Quantity! 
      break;
      
    default:
      break;    
  }
}

/* opens the respective valve */
void openValve(int v) {
  digitalWrite(v, HIGH);
}

/* closes both valves */
void closeValves() {
  digitalWrite(valve_1,LOW); //ensure that valves are closed
  digitalWrite(valve_2,LOW);
}

/* this function is called as soon as a valve opens. It constantly checks the weight of the container with the weight of the load cell */
int fillUp() {
  int count = 0;
  int prev_value = -1;
  int load_cell_val = 0; // get the value of the load cell here

  while (load_cell_val < (.9 * weight)) {
    if (count == 10) {
      return OUTOFSTOCK;    
    }
    
    if (prev_value == load_cell_val) {
      count ++;
    }
    delay (10);
    prev_value = load_cell_val;
  }

  if (load_cell_val > (1.1 * weight)) {
    return OVERFLOW;
  }
  else {
    return SUCCESS;
  }
  
}

/* Runs once at the beginning */
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

  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600); // starts communication through the USB connection at a baud rate of 9600
  setupScreen();
}

int res; 
/* Constantly runs */
void loop() {
  if (reset_state == PRESSED) {
    closeValves();
    curState = Wait;
  }
  switch (curState) { //enum State {Wait, Start, Dispense, End, Debug};
    case Wait:
      // closeValves(); // idk if we want this here...
      updateLEDS(1,0,0); // green
      readUI(); 
      if (button_1_state == PRESSED && pot_1_state > 3) {
        curState = Dispense;
        weight = pot_1_state;
        openValve(valve_1);
      }
      else if (button_2_state == PRESSED && pot_2_state > 3) {
        curState = Dispense;
        weight = pot_2_state;
        openValve(valve_2);
      }
      break;
    
    case Dispense:
      updateLEDS(0,1,0);  // yellow
      res = fillUp();
      if (res == OVERFLOW || res == OUTOFSTOCK) {
        curState = Debug;
      }
      else {
        curState = Wait;
      }
      closeValves();
      break;

    case Debug:
      updateLEDS(0,0,1); // red
      // write to screen some error message
      if (reset_state == PRESSED) {
        curState = Wait;
      }
      weight = 0;
      closeValves();
      break;
    
    default:
      break;
  }
}
