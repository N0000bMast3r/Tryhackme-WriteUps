#https://github.com/eclipse/paho.mqtt.python#getting-started
#https://0xsanz.medium.com/broker-tryhackme-2a80dabaea56
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("secret_chat")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.10.108.148", 1883, 60) # CHANGE THE IP ADDRESS TO THM's ROOMs IP

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()