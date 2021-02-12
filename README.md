# assignment1-pubsub
##### group members
To run this application
1. On a Ubuntu 20.04 machine, simulate a network mininet by running the command "sudo mn -x --topo=tree,fanout=3,depth=2"
2. On one the mininet host run "ifconfig" and take a note of IPv4 address of the host machine e.g. 10.0.0.2
3. On 10.0.0.2 host, the command prompt run "Python3 publisher_app.py", this will create the publisher app to publish the topics and data
4. On another host, example 10.0.0.7, start the subscriber by running "python3 subscriber_middleware.py 10.0.0.2", connecting to publisher server running on host   with the Ip 10.0.0.2

Note - The publisher app publishes messages to 2 topics, temperature and humidity by calling the publish(topic, message) API on the publisher middleware. The subscriber middleware calls notify(topic, message) API on the subscriber app when it receives the messages for the topics it's interested in.

