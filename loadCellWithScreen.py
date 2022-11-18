from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20
import utime
from hx711 import HX711
from utime import sleep_us
from time import sleep


WIDTH =128

HEIGHT= 64

i2c = I2C(0, scl = Pin(1), sda = Pin(0), freq=200000)

 #print("i2c initialization done")

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

#print("post line 22")

def display_weight(weight):
    oled.fill(0)
    write15 = Write(oled, ubuntu_mono_15)

    write20 = Write(oled, ubuntu_mono_20)

    write15.text("Weight is", 0, 10)

    oled.text(str(int(weight)), 5, 35)
    oled.text("grams", 60, 35)

    oled.show()

def display_calculating():
    oled.fill(0)
    oled.text("Calculating", 10, 35)
    oled.show()


def remove_outliers():
        print("entered remove outliers")
        vals = [-10, -10, -10, -10, -10, -10, -10]
        
        # 1. Get 7 readings from stable values
        print("getting readings")
        for i in range(len(vals)):
            print("reading in # ", i)
            reading = -10
            while reading < 0:
                reading = scales.stable_value()
                print(reading)
            vals[i] = reading
            
        # 2. check for outliers
        print("checking for outliers")
        vals.sort()
        print("vals: ", vals)
        median = vals[3]
        upper_fence = median + 1000
        lower_fence = median - 1000


        outlier_idx = []
        for i in range(len(vals)):
            if i > upper_fence or i < lower_fence:
                outlier_idx.append(i)
    
        print("outliers are at indices: ", outlier_idx)
        
        for i in outlier_idx:
            r = scales.stable_value()
            while (r < lower_fence or r > upper_fence):
                r = scales.stable_value()
            vals[i] = r
        
        average = 0
        for i in vals:
            average += i
            
        if (average == 0):
            return 0
        
        return average / 7
    
def scale_values():
    # TODO:
    # my phone is 227.8 grams
    display_calculating()
    res = remove_outliers()
    print("res = ", res)
    print("scaled value: ", res / 7.6997)
    return res / 7.6997
    


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
        return self.read() - self.offset

    def stable_value(self, reads=10, delay_us=500):
        values = []
        for _ in range(reads):
            values.append(self.raw_value())
            sleep_us(delay_us)
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
    
                    

if __name__ == "__main__":
    scales = Scales(d_out=5, pd_sck=6)
    scales.tare()
    #while True:
        #val = scales.stable_value()
       # print(val)
      # res = remove_outliers()
       #print(res)
    while True:
        print(scales.stable_value())
        sleep(2)
    weight = scale_values()
    print(weight)
    
    display_weight(weight)
    #scales.power_off()

