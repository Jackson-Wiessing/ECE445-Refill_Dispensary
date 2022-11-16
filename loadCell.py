from hx711 import HX711
from utime import sleep_us
from time import sleep

def remove_outliers():
        # this function needs to take the average of stabilized values & then convert it to a weight in grams
        print("entered remove outliers")
        vals = [-10, -10, -10, -10, -10, -10, -10]
        
        # 1. Get 7 readings from stable values
        print("getting readings")
        for i in range(len(vals)):
            print("reading in # ", i)
            reading = -10
            while reading < 0:
                reading = scales.stable_value()
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
        
        return average / 7
    
def scale_values(val):
    # TODO:
    return val


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
            weights.append(sum([1 for current in values if abs(prev - current) / (prev / 100) <= deviation]))
        return sorted(zip(values, weights), key=lambda x: x[1]).pop()[0]
    
                    

if __name__ == "__main__":
    scales = Scales(d_out=5, pd_sck=6)
    scales.tare()
    while True:
        #val = scales.stable_value()
       # print(val)
       res = remove_outliers()
       print(res)
       
    scales.power_off()
