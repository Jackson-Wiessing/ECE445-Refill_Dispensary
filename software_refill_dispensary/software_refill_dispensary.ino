/* Software for Refill Dispensary */
#define PRESSED 1 
#define RELEASED 0 // probs don't need this at all 

/* UI components */
int pot_1 = 32; // for user selection 1
int pot_2 = 34; // for user selection 2

int button_1 = 12; // for user selection 1
int button_2 = 14; // for user selection 2
int reset_button = 15; // resets the entire machine

int green_status = 16; // machine status LEDs
int yellow_status = 17;
int red_status = 19;

/* Screen */
int screen_data = 4; // data line for communicating between screen & microcontroller
int screen_clock = 5;

/* Flash Memory */


/* Dispensing part */
int load_cell = 31; // will send values to microcontroller
int valve_1 = 1;
int valve_2 = 2;


void setup() {
  // ***** might need to add something else for PWM vs Analog or whatever ..... *******
  // put your setup code here, to run once:
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
}

void doButtonsWork() {
  int button_1_state = digitalRead(button_1);
  int button_2_state = digitalRead(button_2);
  
  if (button_1_state == PRESSED) {
    Serial.println("button 1 pressed");
  }
  if (button_2_state == PRESSED {
    Serial.println("button 2 pressed");
  }
}

void doPotsWork() {
  int pot_1_state = analogRead(pot_1);
  int pot_2_state = analogRead(pot_2);
  while(1) {
    Serial.println("Pot 1 Value: ");
    Serial.println(pot_1_state);
    Serial.println("Pot 2 Value: ");
    Serial.println(pot_2_state);
  }
}

void doButtonsWithPotsWork() {
  
}

void loop() {
  // put your main code here, to run repeatedly:
  int button_1_state = digitalRead(button_1);
  int button_2_state = digitalRead(button_2);
  while (button_1_state != PRESSED && button_2_state != PRESSED) {
    int pot_1_state = analogRead(pot_1);
    int pot_2_state = analogRead(pot_2);
  }

}
