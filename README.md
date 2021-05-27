# mqtt-to-https-machine-advisor

## Configure and spin up droplet

Create an account with [DigitalOcean](https://digitalocean.com), create, setup and configure the droplet as below. The cheapest plan is more than sufficient for 50 connected devices.

![Create droplet](./images/step1.png)
![Configure droplet](./images/step2.png)
![Select plan](./images/step3.png)

It is recommended to secure your droplet by enabling only ssh keys. Follow the guide by DigitalOcean to create a ssh keys.

![Configure ssh keys](./images/step4.png)

Finish up your configuration by selecting the location of your droplet. You should probably choose a location closest to your connected devices. Spinning up the droplet will take between 1-2mins. Thereafter, copy the ip address of your droplet so that you can access it by ssh.

![Spinning up droplet](./images/step5.png)
![Copy ipaddress](./images/step6.png)

## Setup & Install MQTT broker

1. Login to droplet via ssh.

```shell
ssh root@128.199.191.234
```

2. Install GIT so that you can clone mqtt-to-https-machine-advisor GIT repository.

```shell
yum -y install git
git clone https://github.com/kingsfall/mqtt-to-https-machine-advisor.git
```

3. Run bash script to install dependencies

```shell
 cd mqtt-to-https-machine-advisor/
 bash ./src/setup_droplet.sh
```

4. Start MQTT broker & configure MQTT broker to run on startup.

```shell
systemctl start mosquitto
systemctl enable mosquitto
```

5. Remove exisiting mosquitto.conf file.

```shell
rm -f /etc/mosquitto/mosquitto.conf
```

6. Configure MQTT broker USERNAME & PASSWORD

```shell
mosquitto_passwd -c /etc/mosquitto/passwd <USERNAME>
```

7. Reconfigure mosquitto.conf file to allow only login with password

```shell
cat > /etc/mosquitto/mosquitto.conf 
allow_anonymous false 
password_file /etc/mosquitto/passwd
```

8. Restart MQTT broker.

```shell
systemctl restart mosquitto
```

9. Install python libraries for MQTT client

```shell
pip3 install -r requirements.txt
```

10. modify paho-mqtt-client.py

```shell
vim ./src/paho-mqtt-client.py
```

Inside python code, you need to configure:
1. MQTT broker login credentials
2. Topic to subscribe
3. Machine Advisor Endpoints

For MQTT broker login credentials, we make changes to the code:
```python
# Key in MQTT broker information
broker_ipaddress = "localhost" # "localhost" if running broker and client in same machine
broker_portnumber = 1883 # default MQTT port number is 1883
broker_username = "username" # configure broker username
broker_password = "password" # configure broker password
```

For topics to subscribe, we make changes to the code:
```python
client.subscribe("FACTORY_NAME/MACHINE1") # subscribe based on required topic
client.subscribe("FACTORY_NAME/MACHINE2") # subscribe based on required topic
```
For Machine Advisor Endpoints, we make 2 changes to the code:
First, configure Machine Advisor Endpoints as an object/dictionary inside an array.
```python
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
```
To select the right Machine Advisor Endpoint for MQTT client to send to, we need to associate the subscribed topic to the endpoint.
```python
if "MACHINE1" in msg.topic: # associate topic based on machine_advisor_endpoints' array index
    index = 0
if "MACHINE2" in msg.topic: # associate topic based on machine_advisor_endpoints' array index
    index = 1
```

11. When you are done with the changes exit vim and start python script.
```shell
python3 ./src/paho-mqtt-client.py
```

## Deleting droplet

Make sure to delete your droplet or else DigitalOcean will continue to charge you even when your droplet is offline. To delete droplet, follow steps below.

![Deleting droplet](./images/step7.png)
![Confirm delete droplet](./images/step8.png)