#pip install stmpy
#pip install paho-mqtt

import paho.mqtt.client as mqtt
import stmpy
import os
from threading import Thread
import json
from pi_FSM import pi_fsm
import time
from Arbitrator3 import arbitrator
from Scanner import scanner
from sound import Sound

MQTT_BROKER = '10.22.6.228'
MQTT_PORT = 1883

MQTT_TOPIC_INPUT = 'studyair/HkMDdNVGVl5q/command'
MQTT_TOPIC_OUTPUT = 'studyair/HkMDdNVGVl5q/data' #+ userID when this is received


#update_all_har_sensors: updates all sensors in the SenseHat: humidity, air pressure and temperature
#update_sound_sensors: updates the sound sensor value, has logic for registering sound(time,avg)
#update_on_button: updates all sensor values if some button is pressed
#update_on_time: updates all sensor values every x mins/sec
#wait: waits until next reg.time

class Controller:
    def __init__(self):  # Starter systemet ved å legge til oppforsel og sensorobjektene
        # create a new MQTT client
        self.mqtt_client = mqtt.Client()
        # callback methods
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        # Connect to the broker
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        # subscribe to proper topic(s) of your choice
        self.mqtt_client.subscribe(MQTT_TOPIC_INPUT)
        # start the internal loop to process MQTT messages
        self.mqtt_client.loop_start()
        self.stm_driver = stmpy.Driver()
        self.stm_driver.start(keep_active=True)
        pi_FSM = pi_fsm("the_STM",self)
        self.pi_stm = pi_FSM
        self.MQTT_TOPIC_INPUT = MQTT_TOPIC_INPUT
        self.MQTT_TOPIC_OUTPUT = MQTT_TOPIC_OUTPUT
        self.userID = ""
        self.stm_driver.add_machine(self.pi_stm.stm)
        self.Scanner = scanner()
        self.SoundScanner = Sound()
        self.soundValue = 0
        #set start soundvalue to 0, will obviously be updated the longer the program runs.

    def stop(self):
        # stop the state machine Driver
        self.stm_driver.stop()

    def on_connect(self, client, userdata, flags, rc):
        print("connected!")

    def on_message(self, client, userdata, msg):
        print("test")
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        print(m_decode)
        if "userID" in m_decode:
            self.userID = m_decode[9:-1]
            print("message mottatt")
            print("user id: " + self.userID)
            
            self.MQTT_TOPIC_OUTPUT = "studyair/" + self.userID + "/data"
            print(self.MQTT_TOPIC_OUTPUT)
            
        self.stm_driver.send("update","the_STM") #do we really need this line?

    def calibrate_temp(self, temp):

        #calibrating temperature to represent the real world is really hard.
        #cpu temperature definitely affects the results, and perfecting this
        #to be identical with real world results is close to impossible.
        
        r = os.popen("vcgencmd measure_temp").readline()
        cpu_temp = (r.replace("temp=",""))
        cpu_temp = (cpu_temp.replace("'C\n", ""))
        cpu_temp = float(cpu_temp)
        temp = temp - 13

        if cpu_temp > 60:
            f = cpu_temp - 60
            f = f / 2.5
            print(f)
            temp = temp - f
        return round(temp, 2)

    def requesting_sensor_values(self):
        self.Scanner.update()
        temp = self.Scanner.getTemp()
        temp = self.calibrate_temp(temp) #an attempt to calibrate temperature value, if cpu is hot
        pressure = self.Scanner.getPressure()
        humidity = self.Scanner.getHumidity()
        sound = self.getSound()
        measurements = {'temp:':temp, 'humidity:': humidity, 'airPressure:': pressure, 'sound:':sound}
        print(measurements)
        data_json = json.dumps(measurements)
        self.pi_stm.set_data(data_json)
		
        if temp == -1 or pressure == -1 or humidity == -1 or sound = -1:
            self.pi_stm.set_data("")
            print("One, or more of the sensors are not working.")

        self.stm_driver.send("data_msg","the_STM")

    def arbitrator_evaluation(self, data_json):
        print("evaluating...")
        Arbitrator = arbitrator()
        state = Arbitrator.choose_action(data_json)
        self.pi_stm.set_state(state) #"state") # state value: good,cold,warm,dry,moist
        self.stm_driver.send("arbitrator","the_STM")
		
        if state == "good":
            self.Scanner.setGreenLight()
        else:
            self.Scanner.setRedLight()
			

    def terminate(self):
        print("TERMINATED")
        self.mqtt_client.publish(MQTT_TOPIC_OUTPUT,"terminate")


    def publish_state(self,data_json,state):
        splitted = json.loads(data_json)
        splitted['state'] = state
        json.dumps(splitted)
        print("publish data!")
        print("published in " + self.MQTT_TOPIC_OUTPUT)
        self.mqtt_client.publish(self.MQTT_TOPIC_OUTPUT,data_json)

    def update_sound(self):
        try:
            soundValue = self.SoundScanner.check_sound()
            self.soundValue = soundValue
        except:
            self.soundValue = -1

    def getSound(self):
        return self.soundValue

t = Controller()
t.Scanner.setBlackLight()

while True:
    t.update_sound()
    if t.Scanner.checkJoyStick() == True:
        t.pi_stm.stm.start_timer("t", 1)
