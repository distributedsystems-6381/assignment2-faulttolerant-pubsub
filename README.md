# Distributed System(6381) Assignment1-pubsub
##### Group members
Satish & Tito
##### Pre-requisites
Mininet - https://github.com/mininet/mininet <br />
Zeromq <br />
Python3

**To install Zeromq, please run:** <br/>
sudo apt-get update <br/>
sudo apt-get install python3-dev python3-pip <br/>
sudo -H python3 -m pip install --upgrade pyzmq 


***To run this applcation:***
1. On a Ubuntu 20.04 machine, simulate a mininet network by running the command "sudo mn -x --topo=tree,fanout=3,depth=2"
2. On one of the mininet host, e.g. h2, run "ifconfig" and take a note of IPv4 address of the host machine e.g. 10.0.0.2
3. On 10.0.0.2 host, on the command prompt run e.g. "python3 publisher_app.py 6666", this will create the publisher app to publish the topics and data to port 6666. By default, the publisher publishes date to the "temp" and "humidity" topics. The data for the "temp" topic is generated randomly in the range of interger 1 to 5, and the date for the "himidity" topic is randomly generated in the range of interger 20 to 25. To publish the data to any other topic, please include the additional topic parameter e.g "python3 publisher_app.py 6666 topic1 topic2", and there will be rnadom data between 100 and 200 will be published for these topics.
4. On another host e.g. h7, start the subscriber by running e.g. "python3 subscriber_app.py 10.0.0.2 6666 temp:1 humidity:20", connecting to publisher server running on host with the Ip 10.0.0.2 on port 6666 with "temp:1" and "humidity:20" as the topic filter

Note - The publisher app publishes messages to 2 topics, temperature(temp) and humidity by calling the publish(topic, message) API on the publisher middleware. The subscriber registers the topics and a callback method to the subscriber middleware to receive the data for the registered topics, as and when the subscriber middleware receives topic data from the publisher, it call passes the data to subscriber app by calling the registered callback function.

