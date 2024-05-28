import RPi.GPIO as GPIO
from time import sleep
import numpy as np
import pickle
import json
import requests

# Light sensor :
import smbus

# Voltage sensor :
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Temperature sensor :
import Adafruit_DHT

# Light code :
DEVICE = 0x23
ONE_TIME_HIGH_RES_MODE_1 = 0x20 # 1lx resolution, 120 ms, power down after reading
bus = smbus.SMBus(1)

# Voltage code :
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
def on(pin):
    GPIO.output(pin, GPIO.LOW)
def off(pin):
    GPIO.output(pin, GPIO.HIGH)

class Demand:
    def __init__(self, relay_id, arrival_time, max_load, relay_solar, relay_conventional, voltage_channel, current_channel):
        self.relay_id = relay_id
        self.arrival_time = arrival_time
        self.burst_time = 2  # 10 second allotment
        self.max_load = max_load
        self.source = None
        self.relay_solar = relay_solar
        self.relay_conventional = relay_conventional
        self.voltage_channel = voltage_channel
        self.current_channel = current_channel

    def voltage_reading(self):
        return eval('AnalogIn(ads, ADS.{}).voltage'.format(self.voltage_channel))

    def current_reading(self):
        return eval('AnalogIn(ads, ADS.{}).voltage'.format(self.current_channel))

demand_list = []
demand_provided = []
appliances = [Demand(3, 0, 1.031 * .001, 5, 4, 'P0', 'P1')]
solar_power = None
conventional_power = None

solar_channel = AnalogIn(ads, ADS.P2)
solar_dht_sensor = Adafruit_DHT.DHT11

lr_voltage = pickle.load(open('lr_voltage.sav', 'rb'))
lr_current = pickle.load(open('lr_current.sav', 'rb'))
p_url = 'http://43.205.120.224:5000/predict_pv'
l_url = 'http://43.205.120.224:5000/predict_load'

def fcfs_with_min_load_priority():
    data = data = bus.read_i2c_block_data(DEVICE,ONE_TIME_HIGH_RES_MODE_1)
    light = (data[1] + (256 * data[0])) / 1.2
    voltage = lr_voltage.predict(np.array(solar_channel.voltage).reshape(-1,1))

    humidity, temperature = Adafruit_DHT.read(solar_dht_sensor, 6); humidity = 30 if humidity == None else humidity; temperature = 35 if temperature == None else temperature

    solar_power, estimated_demand = None, None
    pv_data = {'light': float(light), 'voltage': float(abs(voltage[0]))}
    pv_response = requests.post(p_url, json=pv_data)
    if pv_response.status_code == 200:
        pv_result = pv_response.json()
        solar_power = pv_result['solar_power']
        print('Predicted Solar Power:', solar_power)
    else:
        print('Error predicting solar power:', pv_response.text)

    # Request to predict Load
    load_response = requests.post(l_url)
    if load_response.status_code == 200:
        load_result = load_response.json()
        estimated_demand = load_result['estimated_demand']
        print('Estimated Demand:', estimated_demand)
    else:
        print('Error predicting load:', load_response.text)

    if solar_power < 0.01:
        solar_power = 0
    if solar_power > estimated_demand:
        conventional_power = 0
    else:
        conventional_power = estimated_demand - solar_power
    # Control conventional steam generator output

    # Remaining power calculated, after removing allotments
    global demand_provided
    c_power, s_power = 0, 0
    for i in demand_provided:
        if i.source == 0:
            s_power += i.max_load
        elif i.source == 1:
            c_power += i.max_load
    solar_power -= s_power
    conventional_power -= c_power

    # Check for demand
    global demand_list
    global appliances
    for app in appliances:
        if app.voltage_reading() > 0.001:
            flag = 0
            # If not alloted then allot demand
            for i in demand_provided:
                if i.relay_id == app.relay_id:
                    flag = 1
            if flag==0:
                demand_list.append(app)
        else: # Appliance switched off, remove allotment
            for i in demand_provided:
                if i.relay_id == app.relay_id:
                    demand_provided.remove(i)

    # Sort the demands
    demand_list.sort(key=lambda x: (x.arrival_time, x.max_load))

    # Assigning power source to demands
    for i in demand_list:
        if i.max_load <= solar_power:
            i.burst_time = 2
            i.source = 0
            solar_power -= i.max_load
            print('on SOLAR off CONVENTIONAL')
            off(i.relay_conventional)
            on(i.relay_solar)
            print('on SOLAR off CONVENTIONAL')
            demand_provided.append(i)
        elif i.max_load <= conventional_power:
            i.source = 1
            i.burst_time = 2
            conventional_power -= i.max_load
            print('off SOLAR on CONVENTIONAL')
            off(i.relay_solar)
            on(i.relay_conventional)
            print('off SOLAR on CONVENTIONAL')
            demand_provided.append(i)
        else:
            pass  # Load shedding on user line, or a battery line can be provided
    demand_list = []

    # Keep reducing the burst time of allotted demands
    for i in demand_provided:
        i.burst_time -= 1
        print(i.burst_time)
        if i.burst_time <= 0:
            if i.source == 0:
                solar_power += i.max_load
            elif i.source == 1:
                conventional_power += i.max_load
            print('off SOLAR and CONVENTIONAL')
            off(i.relay_solar)
            off(i.relay_conventional)
            demand_provided.remove(i)

    # Actual demand
    tot_v, tot_i = 0, 0
    for app in appliances:
        tot_v += lr_voltage.predict(np.array(app.voltage_reading()).reshape(-1,1))
        tot_i += lr_current.predict(np.array(app.current_reading()).reshape(-1,1))
    tot_power = abs(tot_v * tot_i * .001)

    data = {
        'light': float(light),
        'voltage': float(voltage[0]),
        'temperature': float(temperature),
        'humidity': float(humidity),
        'solar_power': float(solar_power + s_power),
        'estimated_demand': float(estimated_demand),
        'conventional_power': float(conventional_power + c_power),
        'actual_demand': float(tot_power[0])
    }

    with open('generation_data.json', 'w') as json_file:
        json.dump(data, json_file)
    print(data)
    sleep(10) # 10 second delay

def main():
    lr_voltage = pickle.load(open('lr_voltage.sav', 'rb'))
    lr_current = pickle.load(open('lr_current.sav', 'rb'))
    while(True):
        fcfs_with_min_load_priority()
main()
