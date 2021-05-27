import paho.mqtt.client as mqtt
import requests
import json
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("vm-test/POWERTAG_M262")
    client.subscribe("vm-test/PackagingMachine")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    metrics = msg.payload.decode("utf-8")
    metrics = json.loads(metrics)

    if "POWERTAG_M262" in msg.topic:
        index = 0


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
broker_ipaddress = "128.199.160.225" # "localhost" if running broker and client in same machine
broker_portnumber = 1883
broker_username = "admin"
broker_password = "adminpassword"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(broker_username, broker_password)
client.connect(broker_ipaddress, broker_portnumber, 60)

# metrics ={"assetName":"Powertag_150","var12":899,"var12_timestamp":1622104416360,"var13":777,"var13_timestamp":1622104416360}
# Remove Authorization; before keying into machine_advisor_token

# Key in machine advisor endpoints as in an object in an array
machine_advisor_endpoints = [
    {
    "nickname": "Powertag_150",
    "machine_advisor_token": "SharedAccessSignature sr=cnm-ih-na.azure-devices.net%2Furn%3Adev%3Aops%3A000000-EMA-prod-bec5acada1f6df13c6d0f31d&sig=j1uxypRCOgbbwgfHOKQU7FB0cy%2BaQ9WGk9Q3sd2hfcM%3D&se=1650979638",
    "machine_advisor_url": "https://cnm-ih-na.azure-devices.net/devices/urn:dev:ops:000000-EMA-prod-bec5acada1f6df13c6d0f31d/messages/events?api-version=2016-11-14"
}
]


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()


