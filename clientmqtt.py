# -*- coding: utf-8 -*-
## attention python version 3.6
import paho.mqtt.client as mqtt
import os
from urllib.parse import urlparse
import requests as api

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    
###......... Partie philips Hue..................................
    
    if msg.topic.find("rl") != -1:
        #philips hue user url
        user_url="http://192.168.220.52/api/e74Af0XLvMQG3N60KIuGK2PctoeaGQzBG0-qm2vq/"
        on = '{"on": true}'
        off = '{"on": false}'
        id = msg.topic.split("/")[len(msg.topic.split("/"))-1]
        if msg.topic.find("rl/state/light") != -1:
            #print(id)
            room=user_url+"lights/"+ id + "/state" ##☺ ajouter l'id du light à prendre
            if str(msg.payload).find("ON") != -1:
                api.put(room,on)
            elif str(msg.payload).find("OFF") != -1:
                api.put(room,off)

###...... partie update base de données........................
    if msg.topic.find("bd") != -1:
        #databaseurl
        bd_url = "https://glacial-plateau-99461.herokuapp.com/api/rooms"
        id = msg.topic.split("/")[len(msg.topic.split("/"))-1]
        
        if msg.topic.find("bd/state/light") != -1:
            room = bd_url + "/"+id+"/switch-light"
            if str(msg.payload).find("ON") != -1:
                api.post(room,data="ON")
            elif str(msg.payload).find("OFF") != -1:
                api.post(room,data="OFF")
       
        elif msg.topic.find("bd/state/noise") != -1:
            room = bd_url + "/"+id+"/switch-ringer"
            if str(msg.payload).find("ON") != -1:
                api.post(room,data="ON")
            elif str(msg.payload).find("OFF") != -1:
                api.post(room,data="OFF")
            
        elif msg.topic.find("bd/level/light") != -1:
            level=str(msg.payload).split("'")[len(str(msg.payload).split("'"))-2]
            #☻print(str(msg.payload),str(msg.payload).split("'"))
            room = bd_url + "/"+id+"/update-lightlevel/"+level
            #print(room)
            api.post(room)
        elif msg.topic.find("bd/level/noise") != -1:
            level=str(msg.payload).split("'")[len(str(msg.payload).split("'"))-2]
            room = bd_url + "/"+id+"/update-noiselevel/"+level
            #print(room)
            api.post(room)
            

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
#mqttc.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)
url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
url = urlparse(url_str)
topic = url.path[1:] or 'test'

# Connect
mqttc.username_pw_set("ndtzubom","yGCB-nJ4kcOC")
mqttc.connect("m23.cloudmqtt.com", 14984)

# Start subscribe, with QoS level 0
mqttc.subscribe("#", 0)


# Publish a message
mqttc.publish("connection", "successful !")

# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = mqttc.loop()
print("rc: " + str(rc))
 