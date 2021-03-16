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

**High Level Design:**

![alternativetext](/design-fault-tolerant-pub-sub-with-zookeeper.PNG)

***Command to run publishers, brokers and subscribers - direct implementation:***
1. Change directories to your workspace and clone this project 
   ```
   cd ~/workspace
   git clone https://github.com/distributedsystems-6381/assignment2-faulttolerant-pubsub
   cd assignment2-faulttolerant-pubsub
   ```
1. Run publishers by executing the below commnad:  
     ```
      python3 publisher_app.py direct "{zookeeper_ip_port}" "{publisher's_topics_publishing_port}" "{topic_name_1}" "{topic_name_2}"....."{topic_name_n}"
      e.g. python3 publisher_app.py direct "27.0.0.1:2181" "2000" "topic1" "topic2"
     ```
1. Run lamebrokers by executing below command:  
     ```
     python3 lamebroker.py {broker_req_response_binding_port}
     e.g. python3 lamebroker.py 3000
     
***Command to run brokers, publishers and subscribers - broker implementation:***
1. Change directories to your workspace and clone this project 
   ```
   cd ~/workspace
   git clone https://github.com/distributedsystems-6381/assignment2-faulttolerant-pubsub
   cd assignment2-faulttolerant-pubsub
   ```
1. Run brokers by executing the below commnad:  
     ```
      python3 broker.py "{listening_port_for_the_publishers}" "{publishing_port_for_the_subscribers}"
      e.g. python3 broker.py 2000 2001
     ```
1. Run publishers by executing below command:  
     ```
     python3 publisher_app.py broker "{zookeeper_ip_port}" "{topic_name_1}" "{topic_name_2}"....."{topic_name_n}"
     e.g. python3 publisher_app.py broker "27.0.0.1:2181" "topic1" "topic2"
     
_**NOTES**_
   - By default. the publisher app publishes messages to 2 topics
   - Temperature (temp) and humidity by calling the method `publish(topic, message)` via the publisher middleware API
   - To publish the data to any other topics, please include the additional topic parameter, and there will be rnadom data between 100 and 200 will be published for these topics.
   - The subscriber registers the topics via the subscriber middleware API and uses a callback method to receive the data for the registered topics
   - When the subscriber middleware receives topic data from the publisher related to the subscriber's registered topics, it passes the data to subscriber app by calling the registered callback function

***Test Scenarios for Direct Implementation:***
- Start one publisher publishing "topic1" and "topic2"
- Run two instances of the lamebroker process
- Start a subscriber listening for "topic2"
- Start another publisher publishing "topic2", lamebrokerbroker will refresh the list of publishers
- Kill one broker process by keyboard interrupt e.g. "Ctrl + C", the second broker will resume the role of the leader	
- The subscriber will be notified of the broker change and will refresh the publishers from the new broker
- Stop all brokers, the subscriber will be notified of no brokers in the system and will shutdown
	
***Test Scenarios for Broker Implementation:***
- Start couple of brokers, the broker with minimum sequence node will become the leader
- Run two instances of the publishers publishing "topic1" and "topic2"
- Start a subscriber listening for "topic2"
- Stop the current leader broker process, the second broker will become the leader
- The topic publishers and subscribers will be notified of the broker change and will reconnect to the new broker node and start receving the topics			- 
- Stop all brokers, the subscriber will shutdown with the message there's no broker in the system	

***Logging and Graph:*** 
   Running subscriber app generates a comma seperated log text file at the root of the project containing publisher_ip, subscriber_ip, message_id and time taken in milliseconds to receive the message from publisher. The graph and it's test data for the above test scenarios are located in the folder /perf-data-graphs
