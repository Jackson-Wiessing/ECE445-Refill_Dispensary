/* Software for Refill Dispensary */

/* UI components */
int pot_1 = 39; // for user selection 1
int pot_2 = 40; // for user selection 2
int button_1 = 12; // for user selection 1
int button_2 = 13; // for user selection 2
int reset_button = 14; // resets the entire machine

int screen_data =  4; // data line for communicating between screen & microcontroller
int screen_clock = 5;

int green_status = 15; // machine status LEDs
int yellow_status = 16;
int red_status = 17;

int load_cell = 38; // will send values to microcontroller

void setup() {
  // put your setup code here, to run once:
  pinMode(pot_1, INPUT);
  pinMode(pot_2, INPUT);

  pinMode(button_1, INPUT);
  pinMode(button_2, INPUT);
  pinMode(reset_button, INPUT);

  pinMode(screen_data, OUTPUT);
  pinMode(screen_clock, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

}
