
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <string>

#/* Software for Refill Dispensary */
#define PRESSED 1 
#define SCREEN_ADDR 0x78
#define OVERFLOW -1
#define SUCCESS 0 
#define OUTOFSTOCK 1
from machine import Pin, I2C, ADC

from ssd1306 import SSD1306_I2C

from oled import Write, GFX, SSD1306_I2C

from oled.fonts import ubuntu_mono_15, ubuntu_mono_20

import utime

# # /* UI components */
# pot_1 = 32 # for user selection 1
# pot_2 = 34 # for user selection 2
# 
# button_1 = 12 # for user selection 1
# button_2 = 14 # for user selection 2
# reset_button = 15 # resets the entire machine
# 
# green_led = 16 # machine status LEDs
# yellow_led = 17
# red_led = 19
# 
# # /* Screen */
# screen_data = 2 # data line for communicating between screen & microcontroller  -> was pin 4
# screen_clock = 3 # was pin 5
# 
# # /* Dispensing part */
# load_cell = 31 # will send values to microcontroller
# valve_1 = 1
# valve_2 = 2

#/* Runs once at the beginning */
WIDTH =128

HEIGHT= 64

i2c=I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)
#def setup():
pot_1 = ADC(32)
pot_2 = ADC(34)

# pinMode(pot_1, INPUT)
# pinMode(pot_2, INPUT)

button_1 = Pin(12,Pin.IN)
button_2 = Pin(14,Pin.IN)
reset_button = Pin(15,Pin.IN)

# pinMode(button_1, INPUT)
# pinMode(button_2, INPUT)
# pinMode(reset_button, INPUT)

green_led=Pin(16,Pin.OUT)
yellow_led=Pin(17,Pin.OUT)
red_led=Pin(19,Pin.OUT)

# pinMode(green_led, OUTPUT)
# pinMode(yellow_led, OUTPUT)
# pinMode(red_led, OUTPUT)

pinMode(screen_data, OUTPUT)
pinMode(screen_clock, OUTPUT)


#pinMode(load_cell, INPUT)
load_cell=ADC(31)

valve_1=Pin(1,Pin.OUT)
valve_2=Pin(2,Pin.OUT)
# pinMode(valve_1, OUTPUT)
# pinMode(valve_2, OUTPUT)

#pinMode(LED_BUILTIN, OUTPUT)

  #Serial.begin(9600) #// starts communication through the USB connection at a baud rate of 9600
  #//setupScreen()

#   Wire.setSDA(screen_data) #// the 3 of these were previously Wire1
#   Wire.setSCL(screen_clock)
#   Wire.begin(SCREEN_ADDR) 
#   
#   
#   lcd.init()
#   lcd.backlight()


# /* States can be categorized by the following:
# Wait  - no buttons have been pressed
#       - nothing is being dispensed
#       - green status LED is on
#       - screen value changes as potentiometers are turned
#       - Conditions to check before entering the state: 
#             1. button is pressed and the corresponding potentiometer has a non-zero value
#             2. previous state was wait
#             3. load cell reads a value > X grams -> we originally said 19 grams
# Dispense  - machine status turns yellow
#           - "zeros" out the scale
#           - corresponding valve opens
#           - updates the screen every few seconds
#           - if the weight isn't changing after 10 seconds -> enter Debug mode bc something is out of stock 
#           - if weight gets picked up -> immediately stop!
#           - constantly checks if the load cell detects a weight within tolerance of requested quantity 
#               ---> when it does, it stops & closes the valve
#             - ensures that there's no overflow otherwise it will move into the debug state
# Debug - machine status is red
#       - all button presses and potentiometer spins get ignored until the reset button is hit
# */



# /* Tracks the current state of the machine */
#State curState

# /* Screen will be updating periodically to keep the user informed
# Normal - Selected Product X, Quantity = Y
# NoContainer - Error: Must Place Container!
# NoQuantity - Error: Must Select Quantity!
# */

#states
#enum State Wait, Start, Dispense, End, Debug
#enum ScreenText Select, NormalA, NormalB, NoContainer, NoQuantity, Overflow_text, OutOfStock
#ScreenText curText

#/* Initialize all UI components to off or 0 */
button_1_state, button_2_state, reset_state, pot_1_state, pot_2_state = '','','',0,0 

#/* Keeps track of the weight to dispense */
weight = 0 
pot1setting=0
pot2setting=0
buttonvalA=False
buttonvalB=False
# /* TESTING - The goal of this function is to let us know if we're properly understanding how the buttons work */
# void readButtons(int * buf)
#   int but_1_state = digitalRead(button_1)
#   int but_2_state = digitalRead(button_2)
#   int res_state =  digitalRead(reset_button)
#   
#   if (but_1_state == 1)
#       Serial.println("button 1 pressed")
#   
#   if (but_2_state == 1)
#       Serial.println("button 2 pressed")
#   
#   if (res_state == 1)
#     Serial.println("reset pressed")
#   
# 
# 
# /* TESTING - The goal of this function is to figure out the values given by potentiometer readings */
# void readPots() 
#   int p_1_state = analogRead(pot_1)
#   int p_2_state = analogRead(pot_2)
#   Serial.println("Pot 1 Value: ")
#   Serial.println(p_1_state)
#   Serial.println("Pot 2 Value: ")
#   Serial.println(p_2_state)
# 
# 
# /* TESTING - Testing for the first part of the pseudocode */
# void doButtonsAndPotsWork() 
#   int but_1_state = digitalRead(button_1)
#   int but_2_state = digitalRead(button_2)
#   int p_1_state = analogRead(pot_1)
#   int p_2_state = analogRead(pot_2)
# 
#   if (but_1_state == PRESSED and p_1_state > 0) 
#     Serial.println("Pot 1 Value: ")
#     Serial.println(p_1_state)
#     digitalWrite(LED_BUILTIN, HIGH)
#   
#   else if (but_2_state == PRESSED && p_2_state > 0) 
#     Serial.println("Pot 2 Value: ")
#     Serial.println(p_2_state)
#     digitalWrite(LED_BUILTIN, HIGH)
#   
# 
#   delay(100)
#   digitalWrite(LED_BUILTIN, LOW)
# 
# 
# /* Updates the status of the leds */

def updateLEDS(green_status, yellow_status, red_status):
    green_led.value(green_status)
    yellow_led.value(yellow_status)
    red_led.value(red_status)


# /* Setsup screen to write to */
# //void setupScreen()  // recheck the pins for SDA or SCL
 
  

# //
# // enum ScreenText Normal, NoContainer, NoQuantity
# /* */
def updateScreen(text): 
  match text: 
    case 'Select':
      #//show both products, vals of potentiometers for both
      lcd.clear()
      lcd.setCursor(0,0)
      lcd.print("Product 1 quantity: ")
      lcd.print(pot1setting)
      lcd.setCursor(0,1)
      lcd.print("Product 2 quantity: ")
      lcd.print(pot2setting)
      break
    case 'NormalA':
      lcd.clear()
      lcd.setCursor(0,0)
      lcd.print("Selected Product 1, Quantity= ")
      lcd.print(weight)
      #// Selected Product X, Quantity = Y being dispensed
      break
    case 'NormalB':
      lcd.clear()
      lcd.setCursor(0,0)
      lcd.print("Selected Product 2, Quantity= ")
      lcd.print(weight)
      #// Selected Product X, Quantity = Y being dispensed
      break
      
    case 'NoContainer': 
      lcd.clear()
      lcd.setCursor(0,0)
      lcd.print("Error: Must Place Container!")
      break

    case 'NoQuantity':
      lcd.clear()
      lcd.setCursor(0,0)
      lcd.print("Error: Must Select Quantity!") 
      break

    case 'Overflow_text':
      lcd.clear()
      lcd.setCursor(0,0)
      lcd.print("Overflow detected") 
      break

    case 'OutOfStock':
      lcd.clear()
      lcd.setCursor(0,0)
      lcd.print("Item is out of stock") 
      break

    case other:
      break    
  



#/* Gets the status of the buttons & potentiometers */
def readUI(): 
  global button_1_state = button_1.value() 
  global button_2_state = button_2.value()
  global pot_1_state = pot_1.read_u16() 
  global pot_2_state = pot_2.read_u16() 
  global reset_state = reset_button.read_u16()



#/* opens the respective valve */
def openValve(v): 
  if v==1:
    valve_1.value(1)
  else if v==2:
    valve_2.value(1)

#/* closes both valves */
def closeValves():
  valve_1.value(0)
  valve_2.value(0)



res,text='',''

#/* this function is called as soon as a valve opens. It constantly checks the weight of the container with the weight of the load cell */
def fillUp(): 
  count = 0
  prev_value = -1
  load_cell_val = round(analogRead(load_cell)/65536* 5,2) #// get the value of the load cell here

  while (load_cell_val < (0.9 * weight)): 
    if (count == 10) 
      return 'OUTOFSTOCK'    
    
    
    if (prev_value == load_cell_val): 
      count +=1
    
    utime.sleep(0.01)
    prev_value = load_cell_val
  

  if (load_cell_val > (1.2 * weight)): 
    return 'OVERFLOW'
  
  else: 
    return 'SUCCESS'
  
  





#/* Constantly runs */
run=True
while run: 
  if (reset_state == 'PRESSED'): 
    closeValves()
    curState = 'Wait'
  
  match curState:  #//enum State Wait, Start, Dispense, End, Debug
    case 'Wait':
      #// closeValves() // idk if we want this here...
      updateLEDS(1,0,0) #// green
      readUI() 
      pot1setting=round(pot_1_state/65536* 5,2)  #originally (val/40905*100)/100
      pot2setting=round(pot_2_state/65536* 5,2)
      load_cell_val=round(load_cell.read_u16()/65536* 5,2)
      text=Select 
      if (button_1_state == 'PRESSED' and pot_1_state > 3 and load_cell_val>3): 
        buttonvalA=True
        curState = 'Dispense'
        weight = pot1setting
        openValve(1)
      
      else if (button_2_state == 'PRESSED' and pot_2_state > 3 and load_cell_val>3): 
        buttonvalB=True
        curState = 'Dispense'
        weight = pot2setting 
        openValve(2)
      
      else if ((button_1_state == 'PRESSED' and pot_1_state < 3) or (button_2_state == 'PRESSED' and pot_2_state < 3)):
        text='NoQuantity'
      
      else if (button_1_state == 'PRESSED' or button_2_state == 'PRESSED' and load_cell_val==0):
        text='NoContainer'
      
      break
    
    case 'Dispense':
      if (buttonvalA):
        text='NormalA'
      
      if (buttonvalB):
        text='NormalB'
      
      updateScreen(text)
      buttonvalA=False
      buttonvalB=False
      updateLEDS(0,1,0)  #// yellow
      res = fillUp()
      if (res == 'OVERFLOW' or res == 'OUTOFSTOCK'): 
        curState = 'Debug'
      
      else 
        curState = 'Wait'
      
      closeValves()
      break

    case 'Debug':
      updateLEDS(0,0,1) #// red
      if(res=='OVERFLOW'):
        text='Overflow_text'
      
      if(res=='OUTOFSTOCK'):
        text='OutOfStock'
      
      #// write to screen some error message
      if (reset_state == 'PRESSED'): 
        curState = 'Wait'
      
      global weight = 0
      closeValves()
      break
    
    default:
      break
  
  updateScreen(text)
