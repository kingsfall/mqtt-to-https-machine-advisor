import paho.mqtt.client as mqtt
import requests
import json
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("FACTORY_NAME/MACHINE1") # subscribe based on required topic
    client.subscribe("FACTORY_NAME/MACHINE2") # subscribe based on required topic

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    metrics = msg.payload.decode("utf-8")
    metrics = json.loads(metrics)

    if "MACHINE1" in msg.topic: # associate topic based on machine_advisor_endpoints' array index
        index = 0
    if "MACHINE2" in msg.topic: # associate topic based on machine_advisor_endpoints' array index
        index = 1


    try:
        machine_advisor_token = machine_advisor_endpoints[index]["machine_advisor_token"]
        machine_advisor_url = machine_advisor_endpoints[index]["machine_advisor_url"]
        print(f'Sending data to machine advisor endpoint: {machine_advisor_endpoints[index]["nickname"]}')
        machine_advisor_post(metrics,machine_advisor_token,machine_advisor_url)
    except:
        pass


# This function will send data to Schneider Electric Machine Advisor
def machine_advisor_post(metrics,machine_advisor_token,machine_advisor_url):
    
    machine_advisor_headers = {
        "Authorization": machine_advisor_token,
        "Content-Type":"application/json"
    }

    machine_advisor_payload = {
        "metrics": metrics
    }
    machine_advisor_post_message = requests.post(url=machine_advisor_url, data=json.dumps(machine_advisor_payload), headers=machine_advisor_headers)
    print(f'Machine Advisor Post Status Code: {machine_advisor_post_message.status_code}')


# Key in MQTT broker information
broker_ipaddress = "localhost" # "localhost" if running broker and client in same machine
broker_portnumber = 1883
broker_username = "username" # configure broker username
broker_password = "password" # configure broker password

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(broker_username, broker_password)
client.connect(broker_ipaddress, broker_portnumber, 60)


# Key in machine advisor endpoints as in an object in an array
machine_advisor_endpoints = [
    {
    "nickname": "ENDPOINT_NICKNAME1",
    "machine_advisor_token": "MACHINE_ADVISOR_TOKEN", # Remove Authorization; before keying into machine_advisor_token
    "machine_advisor_url": "https://cnm-ih-na.azure-devices.net/devices/urn:dev:ops:000000-EMA-prod-bec5acada1f6df13c6d0f31d/messages/events?api-version=2016-11-14"
},
    {
    "nickname": "ENDPOINT_NICKNAME2",
    "machine_advisor_token": "MACHINE_ADVISOR_TOKEN", # Remove Authorization; before keying into machine_advisor_token
    "machine_advisor_url": "https://cnm-ih-na.azure-devices.net/devices/urn:dev:ops:000000-EMA-prod-bec5acada1f6df13c6d0f31d/messages/events?api-version=2016-11-14"
}
]


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()


