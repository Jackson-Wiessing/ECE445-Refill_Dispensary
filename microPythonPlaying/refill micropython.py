from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20
import utime


# screen setup 
WIDTH =128
HEIGHT = 64
i2c = I2C(0, scl = Pin(1), sda = Pin(0),freq = 200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)
# ---------------------

# port declarations
pot_1 = ADC(32)
pot_2 = ADC(34)
button_1 = Pin(12,Pin.IN)
button_2 = Pin(14,Pin.IN)
reset_button = Pin(15,Pin.IN)

green_led = Pin(16,Pin.OUT)
yellow_led = Pin(17,Pin.OUT)
red_led = Pin(19,Pin.OUT)

load_cell = ADC(31)

valve_1 = Pin(2,Pin.OUT) #used to be 1 and 2
valve_2 = Pin(3,Pin.OUT)
# -----------------------

button_1_state, button_2_state, reset_state, pot_1_state, pot_2_state = 0,0,0,0,0 

#/* Keeps track of the weight to dispense */
weight = 0 
pot1setting = 0
pot2setting = 0
buttonvalA = False
buttonvalB = False

def updateLEDS(green_status, yellow_status, red_status):
    green_led.value(green_status)
    yellow_led.value(yellow_status)
    red_led.value(red_status)


def updateScreen(text): 
  match text: 
    case 'Select':
      #//show both products, vals of potentiometers for both
      oled.fill(0)
      oled.text("Product 1 quantity: " + str(pot1setting), 0, 10)
      oled.text("Product 2 quantity: " + str(pot1setting), 0, 35)
      oled.show()

    case 'NormalA':
      oled.fill(0)
      oled.text("Selected Product 1, Quantity = ", 0, 10)
      oled.text(str(weight) + " grams", 5, 35)
      oled.show()
    
    case 'NormalB':
      oled.fill(0)
      oled.text("Selected Product 2, Quantity = ", 0,10)
      oled.text(str(weight) + " grams", 5, 35)
      oled.show()
      
    case 'NoContainer': 
      oled.fill(0)
      oled.text("Error: Must Place Container!", 0, 10)
      oled.show()

    case 'NoQuantity':
      oled.fill(0)
      oled.text("Error: Must Select Quantity!", 0, 10)
      oled.show()

    case 'Overflow_text':
      oled.fill(0)
      oled.text("Overflow detected", 0, 10)
      oled.show()

    case 'OutOfStock':
      oled.fill(0)
      oled.text("Item is out of stock", 0, 10)
      oled.show()


#/* Gets the status of the buttons & potentiometers */
def readUI(): 
  button_1_state = button_1.value() 
  button_2_state = button_2.value()
  pot_1_state = pot_1.read_u16() 
  pot_2_state = pot_2.read_u16() 
  reset_state = reset_button.read_u16()



#/* opens the respective valve */
def openValve(v): 
  if v == 1:
    valve_1.value(1)
  elif v == 2:
    valve_2.value(1)

#/* closes both valves */
def closeValves():
  valve_1.value(0)
  valve_2.value(0)

res, text = '',''

def fillUp(): 
  count = 0
  prev_value = -1
  load_cell_val = round(load_cell.read_u16()/65536* 5,2) #get the value of the load cell here

  while (load_cell_val < (0.9 * weight)): 
    if (count == 10): 
      return 'OUTOFSTOCK'    
    
    if (prev_value == load_cell_val): 
      count += 1
    
    utime.sleep(0.01)
    prev_value = load_cell_val
  

  if (load_cell_val > (1.2 * weight)): 
    return 'OVERFLOW'
  
  else: 
    return 'SUCCESS'
  
  

run = True

while run: 
  if (reset_state == 'PRESSED'): 
    closeValves()
    curState = 'Wait'
  
  match curState:  
    case 'Wait':
      updateLEDS(1, 0, 0) #// green
      readUI() 
      pot1setting = round(pot_1_state / 65536 * 5, 2)  #originally (val/40905*100)/100
      pot2setting = round(pot_2_state / 65536 * 5, 2)
      load_cell_val = round(load_cell.read_u16() / 65536 * 5, 2)
      text = 'Select' # might be an error here

      if (button_1_state == 1 and pot_1_state > 3 and load_cell_val>3): 
        buttonvalA=True
        curState = 'Dispense'
        weight = pot1setting
        openValve(1)
      
      elif (button_2_state == 1 and pot_2_state > 3 and load_cell_val>3): 
        buttonvalB=True
        curState = 'Dispense'
        weight = pot2setting 
        openValve(2)
      
      elif ((button_1_state == 1 and pot_1_state < 3) or (button_2_state == 'PRESSED' and pot_2_state < 3)):
        text = 'NoQuantity'
      
      elif (button_1_state == 1 or button_2_state == 1 and load_cell_val == 0):
        text = 'NoContainer'
      
      # break
    
    case 'Dispense':
      if (buttonvalA):
        text = 'NormalA'
      
      if (buttonvalB):
        text = 'NormalB'
      
      updateScreen(text)
      buttonvalA = False
      buttonvalB = False
      updateLEDS(0, 1, 0)  #// yellow
      res = fillUp()
      if (res == 'OVERFLOW' or res == 'OUTOFSTOCK'): 
        curState = 'Debug'
      else: 
        curState = 'Wait'
      
      closeValves()
     # break

    case 'Debug':
      updateLEDS(0,0,1) #// red
      if(res == 'OVERFLOW'):
        text = 'Overflow_text'
      
      if(res=='OUTOFSTOCK'):
        text = 'OutOfStock'
      
      # write to screen some error message
      if (reset_state == 1): 
        curState = 'Wait'
      
      weight = 0
      closeValves()
      #break
    
  
  updateScreen(text)
