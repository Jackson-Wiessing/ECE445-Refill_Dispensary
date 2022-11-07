//const int pot_1 = 31;

const int LED_1 = 15;
const int pot_1 = 26;
const int but_1 = 14;

const int LED_2 = 0;
const int pot_2 = 27;
const int but_2 = 13;

const int screen_rst = 18;
const int screen_scl = 17;
const int screen_sda = 16;


int count = 0;
int but_1_state, but_2_state;
int pot_1_state,pot_2_state =0;

void setup() {
  // put your setup code here, to run once:
  //pinMode(pot_1, INPUT);
  pinMode(LED_1, OUTPUT);
  pinMode(pot_1, INPUT);
  pinMode(but_1, INPUT);

  pinMode(LED_2, OUTPUT);
  pinMode(pot_2, INPUT);
  pinMode(but_2, INPUT);
  
  Serial.begin(9600);
}

void doButtonsAndPotsWork() {
  but_1_state = digitalRead(but_1);
  but_2_state = digitalRead(but_2);
  pot_1_state = analogRead(pot_1);
  pot_2_state = analogRead(pot_2);

  if (but_1_state == HIGH && pot_1_state > 20) {
    digitalWrite(LED_1, HIGH);
    digitalWrite(LED_2, LOW);
    Serial.println(pot_1_state);
  }
  else if (but_2_state == HIGH && pot_2_state > 20) {
    digitalWrite(LED_2, HIGH);
    digitalWrite(LED_1, LOW);
    Serial.println(pot_2_state);
  }
  delay(1000);
}



void loop() {
  doButtonsAndPotsWork();
}
