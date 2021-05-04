# import libraries
import paho.mqtt.client as mqtt
import time
import grovepi
import grove_rgb_lcd 
from grovepi import*
from grove_rgb_lcd import*

# LED setup
led_pin = [3,4]
led = {1:led_pin[0],2:led_pin[1]} # channel one controls port3, channel two controls port4
pinMode(led_pin,"OUTPUT")
led1 = 'OFF' # channel1 LED status 
led2 = 'OFF' # channel2 LED status
digitalWrite(3,0) # set red LED at channel1 (P3) to be off by default
digitalWrite(4,0) # set blue LED at channel2 (P4) to be off by default

# LCD setup
setRGB(255,255,255) # LCD backlit

# channel setting
current_channel = 1 # by default, set channel to 1 (port3)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("zhuoyaoc/LED_control") # subscribe to gesture control topic
    client.message_callback_add("zhuoyaoc/LED_control", LCD_LED_response) # associate callback that adjusts LED and LCD

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def LCD_LED_response(client,userdata,message):
    cmd = message.payload.decode(encoding='UTF-8',errors='strict') # decode the payload
    print(cmd)
    global current_channel
    global led1
    global led2
    if cmd == 'Open': # when open palm gesture detected, turn on led corresponds to current channel
        digitalWrite(led[current_channel],1)
        if current_channel == 1:
            led1 = 'ON'
        elif current_channel == 2:
            led2 = 'ON'
    elif cmd == 'Close': # when close palm gesture detected, turn off led corresponds to current channel
        digitalWrite(led[current_channel],0)
        if current_channel == 1:
            led1 = 'OFF'
        elif current_channel == 2:
            led2 = 'OFF'
    elif cmd == 'One': # when hand gesture number one detected, switch to control led1
        current_channel = 1
    elif cmd == 'Two': # when hand gesture number two detected, switch to control led2
        current_channel = 2
    setText_norefresh('LED1(red): %s \nLED2(blue): %s' %(led1,led2)) # update led status on LCD

# MQTT broker connection setup 
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
client.loop_start()

while True:
    pass
