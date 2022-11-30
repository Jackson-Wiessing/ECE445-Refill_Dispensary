from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20
from hx711 import HX711
import utime

# CHECK ALL THE PINS AGAIN BEFORE RUNNING THE CODE

# screen setup
WIDTH = 128
HEIGHT = 64
i2c = I2C(1, sda = Pin(2), scl = Pin(3), freq = 200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# for HX711 chip
#scales = Scales(d_out = 5, pd_sck = 6) # must confirm  MUST FIX THIS BEFORE USING IT

# port declarations
pot_1 = machine.ADC(27)
pot_2 = machine.ADC(28)

button_1 = Pin(9, Pin.IN,Pin.PULL_UP)
button_2 = Pin(10, Pin.IN,Pin.PULL_UP)
reset_button = Pin(11, Pin.IN,Pin.PULL_UP)

green_led = Pin(12, Pin.OUT)
yellow_led = Pin(13, Pin.OUT)
red_led = Pin(14, Pin.OUT)

valve_1 = Pin(0, Pin.OUT) 
valve_2 = Pin(1, Pin.OUT)

load_cell = ADC(26)

# tracks the state of all UI components
#button_1_state, button_2_state, reset_state, pot_1_state, pot_2_state = 0, 0, 0, 0, 0 

# Keeps track of the weight to dispense 
#weight = 0 
pot1setting = 0
pot2setting = 0
buttonvalA = False
buttonvalB = False

text = ''

class Scales(HX711):
    def __init__(self, d_out, pd_sck):
        super(Scales, self).__init__(d_out, pd_sck)
        self.offset = 0

    def reset(self):
        self.power_off()
        self.power_on()

    def tare(self):
        self.offset = self.read()

    def raw_value(self):
        return (self.read() - self.offset) / 4.057

    def stable_value(self, reads=10, delay_us=500):
        values = []
        for _ in range(reads):
            values.append(self.raw_value())
            #sleep_us(delay_us)
        return self._stabilizer(values)

    @staticmethod
    def _stabilizer(values, deviation=10):
        weights = []
        for prev in values:
            if prev == 0:
                weights.append(0)
            else:
                weights.append(sum([1 for current in values if abs(prev - current) / (prev / 100) <= deviation]))
        return sorted(zip(values, weights), key=lambda x: x[1]).pop()[0]


def updateLEDS(green_status, yellow_status, red_status):
  green_led.value(green_status)
  yellow_led.value(yellow_status)
  red_led.value(red_status)


def updateScreen(text, pot_1_state, pot_2_state, w = 0):
 # print(text)
  if (w < 0):
      w = w * -1
      
  if text == 'Select': # show both products, vals of potentiometers for both
    oled.fill(0)
    oled.text("Product 1 ", 0, 10)
    oled.text("quantity: " + str(pot_1_state), 0, 20)
    oled.text("Product 2: ", 0, 30)
    oled.text("quantity: " + str(pot_2_state), 0, 40)
    oled.show()
  
  elif text == 'Dispense':
    print("weight: ", w)
    oled.fill(0)
    oled.text(str(w) + " grams", 5, 10)
    oled.show()
  
  elif text == 'SUCCESS':
    oled.fill(0)
    oled.text("Dispensed ", 0, 10)
    oled.text(str(w) + "grams", 0, 20)
    oled.show()

  elif text == 'NormalA':
    oled.fill(0)
    oled.text("Selected ", 0, 10)
    oled.text("Product 1", 0, 20)
    oled.text("Quantity = ", 0, 30)
    oled.text(str(pot_1_state) + " grams", 0, 40)
    oled.show()

  elif text== 'NormalB':
    oled.fill(0)
    oled.text("Selected ", 0, 10)
    oled.text("Product 2", 0, 20)
    oled.text("Quantity = ", 0, 30)
    oled.text(str(pot_2_state) + " grams", 0, 40)
    oled.show()
      
  elif text == 'NoContainer': 
    oled.fill(0)
    oled.text("Error: ", 0, 10)
    oled.text("Must Place", 0, 20)
    oled.text("Container!", 0, 30)
    oled.show()

  elif text == 'NoQuantity':
    oled.fill(0)
    oled.text("Error: ", 0, 10)
    oled.text("Must Select", 0, 20)
    oled.text("Quantity!", 0, 30)
    oled.show()

  elif text == 'Reset':
    oled.fill(0)
    oled.text("Maintence ", 0, 10)
    oled.text("Required", 0, 20)
    oled.text("Out of order!", 0, 30)
    oled.show()

  elif text == 'OVERFLOW':
    oled.fill(0)
    oled.text("Overflow", 0, 10)
    oled.text("Detected", 0, 20)
    oled.show()

  elif text == 'OUTOFSTOCK':
    oled.fill(0)
    oled.text("Item is ", 0, 10)
    oled.text("out of stock", 0, 20)
    oled.show()
    #utime.sleep_ms(100)
  else:
      print("ERROR with text to display")


# Gets the status of the buttons & potentiometers 
def readUI(button_1_state, button_2_state, reset_state, pot_1_state, pot_2_state):
  button_1_state = not (button_1.value())
  button_2_state = not (button_2.value())
  reset_state = not (reset_button.value())
  pot_1_state = pot_1.read_u16() 
  pot_2_state = pot_2.read_u16()

  if pot_1_state > 50000:
    pot_1_state = 50000
  elif pot_1_state < 400:
    pot_1_state = 0

  if pot_2_state > 50000:
    pot_2_state = 50000
  elif pot_2_state < 400:
    pot_2_state = 0
  
  pot_1_state = int(pot_1_state / 50000)
  pot_2_state = int(pot_2_state / 50000)
  

  #print("button 1: ", button_1_state)
  #print("button 2: ", button_2_state)
  #print("reset :", reset_state)
  #print("pot 1 val: ", pot_1_state)
  #print("pot 2 val: ", pot_2_state)
  



# opens the respective valve
def openValve(v):
  print("opening valve ", v)
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

# 'OVERFLOW', 'OUTOFSTOCK', 'SUCCESS'
def fillUp(w):
    updateLEDS(0, 1, 0)
    scales = Scales(d_out = 5, pd_sck = 6)
    scales.tare()
    print("Filling UP")
    count = 0
    prev_value = 0
    print("scales.raw_value")
    load_cell_val = round(scales.raw_value() / (2**22) * 30000, 2)
    utime.sleep(1)
    reset_state = not (reset_button.value())
    
    while (load_cell_val < (0.9 * w) and load_cell_val != w):
        #updateScreen('Dispense', 0, 0, load_cell_val)
        reset_state = not (reset_button.value())
        if reset_state:
            resetState()
            
        print("count: ", count, " load cell val: ", load_cell_val)
        load_cell_val = round(scales.raw_value() / (2**22) * 30000, 2)

        if (load_cell_val > (3 * w)):
            print("overflow")
            updateScreen('OVERFLOW', 0, 0, 0)
            updateLEDS(0, 1, 0)
            closeValves()
            return 'OVERFLOW'
        if (count == 50):
            print("out of stock")
            updateScreen('OUTOFSTOCK', 0, 0, 0)
            updateLEDS(0, 1, 0)
            closeValves()
            return 'OUTOFSTOCK'
        
        if prev_value == load_cell_val:
            count = count + 1
        else:
            count = 0
        
       # if prev_value < (1.05 * load_cell_val) and prev_value > (.95 * load_cell_val):
        #    count = count + 1
            
        if load_cell_val < prev_value:
            load_cell_val = prev_value
        else:
          updateScreen("Dispense", 0 , 0, load_cell_val)

        prev_value = load_cell_val
        utime.sleep(0.01)
       # print("load cell says: ", load_cell_val)
       # print("prev value says: ", prev_value)
    print("success")
    updateScreen('SUCCESS', 0, 0, round((scales.raw_value() / (2**22)) * 30000, 2))
    updateLEDS(1, 0, 0)
    closeValves()
    return 'SUCCESS'
    

def resetState():
    closeValves()
    utime.sleep(3)
    while True:
        reset_state = not (reset_button.value())
        if reset_state:
            refillDispensary()

def refillDispensary():
    res = ""
    button_1_state, button_2_state, reset_state, pot_1_state, pot_2_state = 0, 0, 0, 0, 0 
    # global weight
    scales = Scales(d_out = 5, pd_sck = 6)
    scales.tare()
    print("started")
    updateScreen('Select', pot_1_state, pot_2_state, 0)
    updateLEDS(1, 0, 0) # green LED
    closeValves()
    
    while True:
        button_1_state = not (button_1.value())
        button_2_state = not (button_2.value())
        reset_state = not (reset_button.value())
        pot_1_state = pot_1.read_u16() 
        pot_2_state = pot_2.read_u16()

        if pot_1_state > 50000:
            pot_1_state = 50000
        elif pot_1_state < 400:
            pot_1_state = 0

        if pot_2_state > 50000:
            pot_2_state = 50000
        elif pot_2_state < 400:
            pot_2_state = 0
  
        pot_1_state = int(pot_1_state / 50)
        pot_2_state = int(pot_2_state / 50)
        #print("pot 1: ", pot_1_state)
        #print("pot 2: ", pot_2_state)
        #valve_1.value(0)
        if (button_1_state):
            print("button 1 pressed")
            print("pot_1 = ", pot_1_state)
            if pot_1_state < .01:
                updateScreen('NoQuantity', pot_1_state, pot_2_state)
            else:
                updateScreen('NormalA', pot_1_state, pot_2_state)
                updateLEDS(0, 0, 1)
                #openValve(1)
                valve_2.value(1)
                res = fillUp(pot_1_state)
            utime.sleep(10)
        elif (button_2_state):
            print("button 2 pressed")
            print("pot_2 = ", pot_2_state)
            if pot_2_state < .01:
                updateScreen('NoQuantity', pot_1_state, pot_2_state)
            else:
                updateLEDS(0, 0, 1)
                updateScreen('NormalB', pot_1_state, pot_2_state)
                #openValve(2)
                valve_1.value(1)
                res = fillUp(pot_2_state)
            utime.sleep(10)
        elif (reset_state):
            updateLEDS(0, 1, 0)
            print("reset pressed")
            updateScreen('Reset', pot_1_state, pot_2_state)
            valve_1.value(0)
            valve_2.value(0)
            resetState()
        else:
            updateScreen('Select', pot_1_state, pot_2_state)


refillDispensary()
#closeValves()

