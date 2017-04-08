 #!/usr/bin/python3

#required libraries
import sys                                 
import ssl
import json
import paho.mqtt.client as mqtt

# for motion sensor
import RPi.GPIO as GPIO
import time
from datetime import datetime


#called while client tries to establish connection with the server 
def on_connect(mqttc, obj, flags, rc):
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
        mqttc.subscribe("$aws/things/raspberry-pi/shadow/update/acceptd", qos=0)
    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")

#called when a topic is successfully subscribed to
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos)+"data"+str(obj))

#called when a message is received by a topic
def on_message(mqttc, obj, msg):
    print("Received message from topic: "+msg.topic+" | QoS: "+str(msg.qos)+" | Data Received: "+str(msg.payload))

#creating a client with client-id=mqtt-test
mqttc = mqtt.Client(client_id="cgao")

mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set(ca_certs="/home/pi/aws_iot/rootCA.pem.crt",
	            certfile="/home/pi/aws_iot/473bedb809-certificate.pem.crt",
	            keyfile="/home/pi/aws_iot/473bedb809-private.pem.key",
              tls_version=ssl.PROTOCOL_TLSv1_2, 
              ciphers=None)

#connecting to aws-account-specific-iot-endpoint
mqttc.connect("AAFBRWW6W9FLP.iot.us-west-2.amazonaws.com", port=8883) #AWS IoT service hostname and portno

#automatically handles reconnecting
#start a new thread handling communication with AWS IoT
mqttc.loop_start()

sensor = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(sensor,GPIO.IN)
previous_state = False
current_state = False
rc=0
i=0
try:
    while rc == 0:
        #i = GPIO.input(sensor)
        time.sleep(0.1)
        previous_state = current_state
        current_state = GPIO.input(sensor)
        if current_state != previous_state:
            i = "HIGH" if current_state else "LOW"
            #print("GPIO pin %s is %s" % (sensor, new_state))    
        print(i)     # i = 1: Motion detected; i = 0: No Motion
        data={}
        data['motion']=i
        data['time']=datetime.now().strftime('%Y/%m/%d %H:%M:%s')
        playload = '{"state":{"reported":'+json.dumps(data)+'}}'
        print(playload)

        #the topic to publish to
        #the names of these topics start with $aws/things/thingName/shadow.
        msg_info = mqttc.publish("$aws/things/raspberry-pi/shadow/update", playload, qos=1)

        time.sleep(1.5)  

except KeyboardInterrupt:
    pass

GPIO.cleanup()
