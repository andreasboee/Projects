import paho.mqtt.client as mqtt
import stmpy
from threading import Thread
import json
import time

MQTT_BROKER = '10.22.6.12'
MQTT_PORT = 1883

MQTT_TOPIC_INPUT = 'alexa/timer/command'
MQTT_TOPIC_OUTPUT = 'alexa/timer/answer'


class TimerLogic:
    def __init__(self, name, duration, component):
        self.name = name
        self.duration = duration
        self.component = component

        t0 = {'source' : 'initial',
              'target' : 'active',
              'effect': 'start'}

        t1 = {'trigger' : 'status',
              'source' : 'active',
              'target' : 'active',
              'effect': 'report_status'}

        t2 = {'trigger' : 't',
              'source' : 'active',
              'target' : 'end_state',
              'effect': 'timer_completed'}

        self.stm = stmpy.Machine(name=name, transitions=[t0, t1, t2], obj=self)

    def start(self):
        self.stm.start_timer("t", self.duration)

    def timer_completed(self):
        self.component.on_completed(self.name)
        self.stm.terminate()

    def report_status(self):
        msg = self.name+", has "+str(self.stm.get_timer("t")/1000)+"s left"
        print(self.name+", has "+str(self.stm.get_timer("t")/1000)+"s left")
        self.component.on_report_status(msg)



class TimerManagerComponent:


    def on_report_status(self,msg):
        self.mqtt_client.publish(MQTT_TOPIC_OUTPUT,msg)        #uncomment

    def on_completed(self,name):
        msg = json.dumps({'name': name, 'status': "done"})
        self.mqtt_client.publish(MQTT_TOPIC_OUTPUT,msg)        #uncomment
        print("Post: " + msg)

        if self.timer_ids.__contains__(name):
            self.timer_ids.remove(name)

    def on_connect(self, client, userdata, flags, rc):
        print("Is connected!")

    def on_message(self, client, userdata, msg):
        j = json.loads(msg.payload)
        if j["command"] == "new_timer":
            print("New timer"+ str(j["name"])+" lasting "+str(j["duration"]/1000)+"s")

            timer = TimerLogic(j["name"],j["duration"],self)
            self.stm_driver.add_machine(timer.stm)
            self.timer_ids.append(j["name"])

        if j["command"] == "status_all_timers":
            for id in self.timer_ids:
                self.stm_driver.send("status",id)

        if j["command"] == "status_single_timer":
            if self.timer_ids.__contains__(j["name"]):
                self.stm_driver.send("status",j["name"])
                print("status timer: "+ str(j["name"]))


    def __init__(self):
        self.timer_ids = list()

        # create a new MQTT client
        self.mqtt_client = mqtt.Client()                   #decomment
        # callback methods
        self.mqtt_client.on_connect = self.on_connect              #decomment
        self.mqtt_client.on_message = self.on_message              #decomment
        # Connect to the broker
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT)           #decomment
        # subscribe to proper topic(s) of your choice
        self.mqtt_client.subscribe(MQTT_TOPIC_INPUT)               #decomment
        # start the internal loop to process MQTT messages
        self.mqtt_client.loop_start()                          #decomment

        self.stm_driver = stmpy.Driver()
        self.stm_driver.start(keep_active=True)


    def stop(self):
        # stop the MQTT client
        self.mqtt_client.loop_stop()

        # stop the state machine Driver
        self.stm_driver.stop()


t = TimerManagerComponent()

# Testing JSON commands:
s1 = '{"command": "new_timer", "name": "spaghetti", "duration":5000 }'
s2 = '{"command": "status_all_timers"}'
s3 = '{"command": "status_single_timer", "name": "spaghetti"}'

#t.on_message("","",s1)
#time.sleep(3)
#t.on_message("","",s2)
#t.on_message("","",s3)
print("started")