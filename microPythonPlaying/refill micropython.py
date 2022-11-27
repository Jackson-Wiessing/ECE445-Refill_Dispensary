from machine import Pin, I2C, ADC, machine
from ssd1306 import SSD1306_I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20
import utime

# screen setup
WIDTH = 128
HEIGHT = 64
i2c = I2C(0, sda = Pin(4), scl = Pin(5), freq = 200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# port declarations
#pot_1 = ADC(27)
#pot_2 = ADC(28)
pot_1 = machine.ADC(27)
pot_2 = machine.ADC(28)

button_1 = Pin(9, Pin.IN)
button_2 = Pin(10, Pin.IN)
reset_button = Pin(11, Pin.IN)

green_led = Pin(12, Pin.OUT)
yellow_led = Pin(13, Pin.OUT)
red_led = Pin(14, Pin.OUT)

valve_1 = Pin(1, Pin.OUT) 
valve_2 = Pin(2, Pin.OUT)

load_cell = ADC(26)

# tracks the state of all UI components 
button_1_state, button_2_state, reset_state, pot_1_state, pot_2_state = 0, 0, 0, 0, 0 

# Keeps track of the weight to dispense 
weight = 0 
pot1setting = 0
pot2setting = 0
buttonvalA = False
buttonvalB = False

res, text = '', ''

def updateLEDS(green_status, yellow_status, red_status):
  green_led.value(green_status)
  yellow_led.value(yellow_status)
  red_led.value(red_status)

def updateScreen(text): 
  if text == 'Select': # show both products, vals of potentiometers for both
    oled.fill(0)
    oled.text("Product 1 quantity: " + str(pot1setting), 0, 10)
    oled.text("Product 2 quantity: " + str(pot1setting), 0, 35)
    oled.show()

  if text == 'NormalA':
    oled.fill(0)
    oled.text("Selected Product 1, Quantity = ", 0, 10)
    oled.text(str(weight) + " grams", 5, 35)
    oled.show()

  if text== 'NormalB':
    oled.fill(0)
    oled.text("Selected Product 2, Quantity = ", 0, 10)
    oled.text(str(weight) + " grams", 5, 35)
    oled.show()
      
  if text == 'NoContainer': 
    oled.fill(0)
    oled.text("Error: Must Place Container!", 0, 10)
    oled.show()

  if text == 'NoQuantity':
    oled.fill(0)
    oled.text("Error: Must Select Quantity!", 0, 10)
    oled.show()

  if text == 'Overflow_text':
    oled.fill(0)
    oled.text("Overflow detected", 0, 10)
    oled.show()

  if text == 'OutOfStock':
    oled.fill(0)
    oled.text("Item is out of stock", 0, 10)
    oled.show()
    utime.sleep_ms(100)


# Gets the status of the buttons & potentiometers 
def readUI(): 
  button_1_state = button_1.value() 
  button_2_state = button_2.value()
  reset_state = reset_button.value()
  pot_1_state = pot_1.read_u16() 
  pot_2_state = pot_2.read_u16()

  if pot_1_state > 50000:
    pot_1_state = 50000
  elif pot_1_state < 400:
    pot_1_state = 0

  pot_1_state = round(pot_1_state / 50000, 2)

  if pot_2_state > 50000:
    pot_2_state = 50000
  elif pot_2_state < 400:
    pot_2_state = 0
  
  pot_2_state = round(pot_2_state / 50000, 2)

# opens the respective valve
def openValve(v): 
  if v == 1:
    valve_1.value(1)
  elif v == 2:
    valve_2.value(1)

# closes both valves 
def closeValves():
  valve_1.value(0)
  valve_2.value(0)



# this function is called as soon as a valve opens. 
# It constantly checks the weight of the container with the weight of the load cell
def fillUp(): 
  count = 0
  prev_value = -1
  load_cell_val = round(load_cell.read_u16() / (65536 * 5),2) # get the value of the load cell here

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
  
  
def writeEmpty():
  f = open("bottle_status.txt", "w")
  f.write("Empty")
  f.close()
    
def writeFilled():
  f = open("bottle_status.txt", "w")
  f.write("Filled")
  f.close()
    

#read bottle status file to see if the bottles are empty or not ----> unused as of rn, CALL IT AT THE BEGINING!!!!!!!!
def getBottleStatus():
  f = open("bottle_status.txt", "r")
  if f.readline() == "Empty":
    curState ='Debug'
    res = "OUTOFSTOCK"
  else:
    curState = "Wait"
    
  #f.close()    NOT SURE WHY THESE 2 LINES ARE HERE YET
  #closeValves()


# Constantly runs 
def refillDispensary():
  while True: 
    if (reset_state == 1):
      closeValves() 
      writeFilled()
      curState = 'Wait'
    
    if curState == 'Wait':
      updateLEDS(1, 0, 0)                                # green
      readUI() 

      load_cell_val = round(load_cell.read_u16() / (65536 * 5), 2)
      text ='Select'

      if (button_1_state == 1 and pot_1_state > 3 and load_cell_val > 3): 
        buttonvalA = True
        curState = 'Dispense'
        weight = pot1setting
        openValve(1)
      elif (button_2_state == 1 and pot_2_state > 3 and load_cell_val > 3): 
        buttonvalB = True
        curState = 'Dispense'
        weight = pot2setting 
        openValve(2)
      elif ((button_1_state == 1 and pot_1_state < 3) or (button_2_state == 'PRESSED' and pot_2_state < 3)):
        text = 'NoQuantity'      
      elif (button_1_state == 1 or button_2_state == 1 and load_cell_val == 0):
          text = 'NoContainer'
      
    if curState == 'Dispense':
      if (buttonvalA):
        text = 'NormalA'
      elif (buttonvalB):
        text = 'NormalB'
        
      updateScreen(text)
      buttonvalA = False
      buttonvalB = False
      updateLEDS(0, 1, 0)  # yellow
      res = fillUp()
        
      if (res == 'OVERFLOW' or res == 'OUTOFSTOCK'): 
        curState = 'Debug'
      else: 
        curState = 'Wait'  
      closeValves()

    if curState == 'Debug':
      updateLEDS(0,0,1) # red
      if (res == 'OVERFLOW'):
        text = 'Overflow_text'
        
      if (res == 'OUTOFSTOCK'):
        text = 'OutOfStock'
        writeEmpty()
      # write to screen some error message
      if (reset_state == 1): 
        curState = 'Wait'
        
      weight = 0  # might need to be changed
      closeValves()
    updateScreen(text)