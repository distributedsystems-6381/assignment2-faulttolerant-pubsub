# Distributed System(6381) Assignment1-pubsub
##### Group members
Satish & Tito
##### Pre-requisites
   - [Ubuntu 20.04 machine](https://ubuntu.com/download/desktop)
   - [Mininet](https://github.com/mininet/mininet)
   - [ZeroMQ](https://zeromq.org/)
   - [Python3](https://www.python.org/)

**To install python3 and Zeromq, please run:**
```
sudo apt-get update && \
sudo apt-get install python3-dev python3-pip && \
sudo -H python3 -m pip install --upgrade pyzmq
```

***To run the publisher and subscriber:***
1. Change directories to your workspace and clone this project 
   ```
   cd ~/workspace
   git clone https://github.com/distributedsystems-6381/assignment1-pubsub
   cd assignment1-pubsub
   ```
1. Simulate a network with mininet by running the following command:
   - running this command from the directory with the assigment code in it is a convenience, as it will default to opening the XTerm windows to the same directory
   - the below mininet command will create very basic network topology with a single switch and two hosts
     ```
     sudo mn -x --topo=tree,fanout=3,depth=2
     ```
1. Access one of the created mininet hosts via an XTerm that pops-up, e.g. h2
   - from the XTerm find and take note of the host machine's IP
     ```
     ifconfig | grep -e "inet\s"
     ```
      - 127.0.0.1 is the localhost loopback, the IP will be something similar to 10.0.0.2: 
   
   - from the same host run the publisher:
     ```
     python3 publisher_app.py 6666
     ```
      - This will create the publisher app to publish the topics and data to port 6666 
      - The publisher publishes "temp" and "humidity" topics
      - The data for the "temp" topic is generated randomly in the range of integers 1 to 5
      - The date for the "humidity" topic is randomly generated in the range of integers 20 to 25

1. On another host, e.g. h1, start the subscriber by running
   - the subscriber will connect to publisher application running on host with the IP 10.0.0.2 on port 6666
   - "temp" and "humidity" will be applied as the topic filters
      ```
      python3 subscriber_app.py "10.0.0.2:6666" temp humidity
      ```

_**NOTES**_
   - By default. the publisher app publishes messages to 2 topics
   - Temperature (temp) and humidity by calling the method `publish(topic, message)` via the publisher middleware API
   - To publish the data to any other topic, please include the additional topic parameter e.g "python3 publisher_app.py 6666 topic1 topic2", and there will be rnadom data between 100 and 200 will be published for these topics.
   - The subscriber registers the topics via the subscriber middleware API and uses a callback method to receive the data for the registered topics
   - When the subscriber middleware receives topic data from the publisher related to the subscriber's registered topics, it passes the data to subscriber app by calling the registered callback function

***Test Scenarios:***
1. One publisher publishing 2 topic, 1 subscriber subscribing 1 topic
	-On host 10.0.0.1, start publisher by running <<python3 publisher_app.py 4000>>, this will start publishing "temp" and "humidity" topic
	-On any other host e.g. 10.0.0.3 starts subscriber subscribing to "temp" topic by running <<python3 subscriber_app.py "10.0.0.1:4000" temp>>. The published and subscribed data will start showing up on the console

1. One publisher publishing 3 topic, 1 subscriber subscribing 2 topic
	- On host 10.0.0.1, start publisher by running <<python3 publisher_app.py 4000 topic1>>, this will start publishing "topic1", "temp" and "humidity" topic
	- On any other host e.g. 10.0.0.3 starts subscriber subscribing to "temp" and "topic1" topic by running <<python3 subscriber_app.py "10.0.0.1:4000" temp topic1>>. The published and subscribed data will start showing up on the console	
1. Two publisher publishing 3 topic, 1 subscriber subscribing 1 topic
	- On host 10.0.0.1, start publisher by running <<python3 publisher_app.py 4000 topic1>>, this will start publishing "topic1", "temp" and "humidity" topic, on another host 10.0.0.2 start running another publisher publishing on "temp", "humidity" and "topic1" by running <<python3 publisher_app.py 5000 topic1>>
	- On any other host e.g. 10.0.0.3 starts subscriber subscribing to "topic1" topic by running <<python3 subscriber_app.py "10.0.0.1:4000,10.0.0.2:5000" topic1>>. The published and subscribed data will start showing up on the console

1. Two publisher publishing 4 topic, 1 subscriber subscribing 2 topic
	- On host 10.0.0.1, start publisher by running <<python3 publisher_app.py 4000 topic1>>, this will start publishing "topic1", "temp" and "humidity" topic, on another host 10.0.0.2 start running another publisher publishing on "temp", "humidity", "topic1" and "topic2" by running <<python3 publisher_app.py 5000 topic1 topic2>>
	- On any other host e.g. 10.0.0.3 starts subscriber subscribing to "topic1" topic by running <<python3 subscriber_app.py "10.0.0.1:4000,10.0.0.2:5000" topic1 topic2>>. The published and subscribed data will start showing up on the console
	
***Logging and Graph:*** 
   Running subscriber app generates a comma seperated log text file at the root of the project containing publisher_ip, subscriber_ip, message_id and time taken in milliseconds to receive the message from publisher. The graph and it's test data for the above test scenarios are located in the folder /perf-data-graphs
