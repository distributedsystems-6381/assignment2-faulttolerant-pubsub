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

**High Level Design
![alternativetext](/fault-tolerant-pub-sub-using-zookeeper.PNG)

***To run the publisher and subscriber - direct implementation:***
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
1. Access one of the created mininet hosts via an XTerm that pops-up, e.g. h8
   - from the XTerm find and take note of the host machine's IP
     ```
     ifconfig | grep -e "inet\s"
     ```
      - `127.0.0.1` is the localhost loopback, the IP will be something similar to `10.0.0.8`: 
   
   - from the same host run the lame broker:
      ```
     python3 lamebroker.py {port_on_which_lamebroker_will_run}
     ```
     ```
     e.g. python3 lamebroker.py 8000
     ``` 
1. Access one of the created mininet hosts via an XTerm that pops-up, e.g. h2
   - from the XTerm find and take note of the host machine's IP
     ```
     ifconfig | grep -e "inet\s"
     ```
      - `127.0.0.1` is the localhost loopback, the IP will be something similar to `10.0.0.2`: 
   
   - from the same host run the publisher:
      ```
     python3 publisher_app.py direct {lame_broker_ip:port} {publisher_port} topic1 topic2 etc.
     ```
     ```
     e.g. python3 publisher_app.py direct "10.0.0.8:8000" 2000 topic1 topic2
     ```
      - This will register the publisher with the lame-broker with 10.0.0.8:8000 of the publishers and the publishing topics
      - This will create the publisher app to publish the topics and data to port 2000
      - The publisher publishes "temp", "humidity", "topic1" and "topic2" topics
      - The data for the "temp" topic is generated randomly in the range of integers 1 to 5
      - The data for the "humidity" topic is randomly generated in the range of integers 20 to 25
      - The data for the "topic1" and "topic2" is randomly generated in the range of integers 100 to 200

1. On another host, e.g. h1, start the subscriber by running:
      ```
      python3 subscriber_app.py direct {lame_broker_ip:port} temp humidity
      ```
      ```
      e.g. python3 subscriber_app.py direct "10.0.0.8:8000" temp humidity
      ```
   - The subscriber will connect to the lamebroker on 10.0.0.8:8000 to get the ip:port of the publishers publishing on these topics
   - The subscriber will connect to publishers application running on publising hosts host with the IP 10.0.0.2 on port 2000
   - "temp" and "humidity" will be applied as the topic filters
    
_**NOTES**_
   - By default. the publisher app publishes messages to 2 topics
   - Temperature (temp) and humidity by calling the method `publish(topic, message)` via the publisher middleware API
   - To publish the data to any other topics, please include the additional topic parameter e.g "python3 publisher_app.py "10.0.0.8:8000" 2000 topic1 topic2", and there will be rnadom data between 100 and 200 will be published for these topics.
   - The subscriber registers the topics via the subscriber middleware API and uses a callback method to receive the data for the registered topics
   - When the subscriber middleware receives topic data from the publisher related to the subscriber's registered topics, it passes the data to subscriber app by calling the registered callback function

***To run the publisher and subscriber - broker implementation:***
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
    - this host will serve as the broker
      ```
      ifconfig | grep -e "inet\s"
      ```
        - `127.0.0.1` is the localhost loopback, the IP will be something similar to `10.0.0.2`:

    - from the same host run the broker:
    - the arguments, in order, are port to listen for traffic from publishing nodes and port to serve traffic to listening nodes
      ```
      python3 broker.py 5559 5560
      ```
        - This will create the broker app to that acts as an intermediary between the all publishers and subscribers
        - In the above example, publishers send messages to the broker at `10.0.0.2:5559` and subscribers listen for messages from the broker at `10.0.0.2:5560`

1. On another host, e.g. h1, start a subscriber by running:
   ```
   python3 subscriber_app.py broker "10.0.0.2:5560" temp humidity
   ```
    - arguments for running in broker mode are:
      - `broker`
      - a quoted string `"IP:PORT"`
      - any topics to subscribe to - by default the publisher produces messages for the topics `temp` and `humidity` 
    - the subscriber will connect to broker application at IP 10.0.0.2 on port 5559
    - the subsciber does not listen to any topics by default, so the user must submit a valid topic to receive messages
1. On a third host, e.g. h5, start a publisher by running:
   ```
   python3 publisher_app.py broker "10.0.0.2:5559" topic1 topic2 topic3 ... topicN
   ```
    - arguments for running in broker mode are:
      - `broker`
      - a quoted string `"IP:PORT"`
      - any topics beyond the default to publish
        - by default the publisher produces messages for the topics `temp` and `humidity`
        - the publisher will connect to broker application at IP 10.0.0.2 on port 5559

***All the below test scenarios assume running on mininet***
    
- as previously mentioned, use this command to create a VNet with mininet:
    ```
    sudo mn -x --topo=tree,fanout=3,depth=2
    ```
- the available hosts will be h1, h2, h3, ... , h9 with corresponding IPs 10.0.0.1, 10.0.0.2, 10.0.0.3, ... , 10.0.0.9

***Test Scenarios for Direct Implementation:***
1. One publisher publishing 2 topics, 1 subscriber subscribing to 1 topic
	- On host 10.0.0.8 start the lamebroker on port 8000 by running `python3 lamebroker.py 8000`
	- On host 10.0.0.1, start a publisher by running `python3 publisher_app.py direct "10.0.0.8:8000" 1000`, this will start publishing "temp" and "humidity" topics
	- On any other host, e.g. 10.0.0.3, start a subscriber that listens for the "temp" topic by running `python3 subscriber_app.py direct "10.0.0.8:8000" temp` 
        - The published and subscribed data will start showing up on the XTerm console

1. One publisher publishing 3 topics, 1 subscriber subscribing to 2 topics
	- On host 10.0.0.8 start the lamebroker on port 8000 by running `python3 lamebroker.py 8000`
	- On host 10.0.0.1, start a publisher by running `python3 publisher_app.py direct "10.0.0.8:8000" 1000 topic1`, this will start publishing "topic1", "temp" and "humidity" topics
	- On any other host e.g. 10.0.0.3 start a subscriber that listens for "temp" and "topic1" topics by running `python3 subscriber_app.py direct "10.0.0.8:8000" temp topic1`
        - The published and subscribed data will start showing up on the XTerm console
    
1. Two publisher publishing 3 topics, 1 subscriber subscribing to 1 topic
	- On host 10.0.0.8 start the lamebroker on port 8000 by running `python3 lamebroker.py 8000`
	- On host 10.0.0.1, start a publisher by running `python3 publisher_app.py direct "10.0.0.8:8000" 1000 topic1`, this will start publishing "topic1", "temp" and "humidity" topics
    - On another host, e.g. 10.0.0.2, run another publisher with the topics "temp", "humidity" and "topic1" via `python3 publisher_app.py direct "10.0.0.8:8000" 2000 topic1`
	- On any other host, e.g. 10.0.0.3, start a subscriber that listens for "topic1" from both publishers by running `python3 subscriber_app.py direct "10.0.0.8:8000" topic1`
        - The published and subscribed data will start showing up on the XTerm console

1. Two publisher publishing 4 topics, 1 subscriber subscribing to 2 topics
	- On host 10.0.0.8 start the lamebroker on port 8000 by running `python3 lamebroker.py 8000`
	- On host 10.0.0.1, start a publisher by running `python3 publisher_app.py direct "10.0.0.8:8000" 1000 topic1`
        - this will start publishing the topics "temp", "humidity" and "topic1"
    - On another host, e.g. 10.0.0.2 start running another publisher `python3 publisher_app.py direct "10.0.0.8:8000" 2000 topic1 topic2`
        - this will start publishing the topics "temp", "humidity", "topic1" and "topic2"
	- On any other host, e.g. 10.0.0.3, start a subscriber `python3 subscriber_app.py "10.0.0.8:8000" topic1 topic2` 
        - this will subscribe to "topic1"
        - the published and subscribed data will start showing up on the XTerm console

***Test Scenarios for Broker Implementation:***
1. One publisher publishing 2 topics, one subscriber subscribing to 1 topic, via a single broker
    - On host 10.0.0.2, start a broker: `python3 broker.py 5559 5560`
    - On host 10.0.0.9, start a subscriber: `python3 subscriber_app.py broker "10.0.0.2:5560" temp`
    - On host 10.0.0.5, start publisher: `python3 publisher_app.py broker "10.0.0.2:5559"`
        - this will start publishing "temp" and "humidity" topics
        - the subscriber will only listen for the "temp" topic 
    
1. One publisher publishing 3 topics, one subscriber subscribing to 2 topics, via a single broker
    - On host 10.0.0.3, start a broker: `python3 broker.py 5500 6500`
    - On host 10.0.0.8, start a subscriber: `python3 subscriber_app.py broker "10.0.0.3:6500" temp topic1`
    - On host 10.0.0.1, start publisher: `python3 publisher_app.py broker "10.0.0.3:5500" topic1`
        - this will start publishing "temp", "humidity" and "topic1" topics
        - the subscriber will only listen for the "temp" and "topic1" topics 
    
1. Two publishers publishing 3 topics, one subscriber subscribing to 1 topic, via a single broker
    - On host 10.0.0.4, start a broker: `python3 broker.py 4000 5000`
    - On host 10.0.0.9, start a subscriber: `python3 subscriber_app.py broker "10.0.0.4:5000" humidity`
    - On host 10.0.0.5, start publisher: `python3 publisher_app.py broker "10.0.0.4:4000" topic1`
    - On host 10.0.0.6, start another publisher: `python3 publisher_app.py broker "10.0.0.4:4000" topic1`
        - this produces 2 publishers, publishing "temp", "humidity" and "topic1" topics
        - the subscriber will only listen for the "humidity" topic
            - in the log output you should observe that messages are coming from both 10.0.0.5 and 10.0.0.6 

1. Two publishers publishing 4 topics, one subscriber subscribing to 2 topics, via a single broker
    - On host 10.0.0.1, start a broker: `python3 broker.py 4554 5445`
    - On host 10.0.0.2, start a subscriber: `python3 subscriber_app.py broker "10.0.0.1:5445" topic1 topic3`
    - On host 10.0.0.3, start publisher: `python3 publisher_app.py broker "10.0.0.1:4554" topic1`
    - On host 10.0.0.4, start another publisher: `python3 publisher_app.py broker "10.0.0.1:4554" topic3`
        - this produces 2 publishers, the first publishes "temp", "humidity" and "topic1" topics, the second publishes "temp", "humidity" and "topic3"
        - the subscriber will only listen for the "topic1" and "topic3" topics
            - in the log output you should observe that messages are coming from both 10.0.0.3 and 10.0.0.4

1. Three publishers publishing 6 topics, three subscribers listening to 3 topics each, via two brokers
    - On host 10.0.0.4, start a broker: `python3 broker.py 5559 5560`
    - On host 10.0.0.5, start a second broker: `python3 broker.py 5559 5560`
    - On host 10.0.0.1, start a subscriber: `python3 subscriber_app.py broker "10.0.0.4:5560" temp humidity topic1`
    - On host 10.0.0.2, start a second subscriber: `python3 subscriber_app.py broker "10.0.0.4:5560,10.0.0.5:5560" temp topic2 topic3`
    - On host 10.0.0.3, start a third subscriber: `python3 subscriber_app.py broker "10.0.0.5:5560" humidity topic3 topic4`
    - On host 10.0.0.6, start publisher: `python3 publisher_app.py broker "10.0.0.4:5559" topic2`
    - On host 10.0.0.7, start another publisher: `python3 publisher_app.py broker "10.0.0.4:5559" topic1`
    - On host 10.0.0.8, start another publisher: `python3 publisher_app.py broker "10.0.0.5:5559" topic1 topic2 topic3 topic4`
        - configuration for 3 publishers:
            - the first publishes "temp", "humidity" and "topic2" topics to broker at 10.0.0.4
            - the second publishes "temp", "humidity" and "topic2" to broker at 10.0.0.4
            - the third publishes "temp", "humidity", "topic1", "topic2", "topic3", "topic4" to broker at 10.0.0.5  
        - configuration for 3 subscribers:
            - first subscriber listens for the "temp", "humidity" and "topic1" topics from broker at 10.0.0.4
               - will receive messages from 10.0.0.6 and 10.0.0.7
            - second subscriber listens for the "temp", "topic2" and "topic3" topics from brokers at 10.0.0.4 and 10.0.0.5
               - will receive messages from 10.0.0.6, 10.0.0.7 and 10.0.0.8
            - third subscriber listens for "topic3" and "topic4" topics from broker at 10.0.0.5
               - will receive messages from only 10.0.0.8

***Logging and Graph:*** 
   Running subscriber app generates a comma seperated log text file at the root of the project containing publisher_ip, subscriber_ip, message_id and time taken in milliseconds to receive the message from publisher. The graph and it's test data for the above test scenarios are located in the folder /perf-data-graphs
