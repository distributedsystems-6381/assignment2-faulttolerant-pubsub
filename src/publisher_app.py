import sys
import time
import zmq
from random import randrange
import direct_pub_middleware as dmw
import broker_pub_middleware as bmw
import host_ip_provider as hip
import zk_clientservice as kzcl
import constants as const

# direct args => python3 publisher_app.py direct {lamebroker_ip:port} {publishing_port} topic1 topic2
#       e.g. "python3 publisher_app.py direct "10.0.0.6:7000" 5000 topic1 topic2"
# broker args => "python3 publisher_app.py broker {message_broker_ip:port} {publishing_port} topic1 topic2
#       e.g. "python3 publisher_app.py broker "10.0.0.6:7000" topic1 topic2"
# METHODS
# provides the topic data for a given topic
'''
    1. Args {messaging_strategy: direct or broker} {zookeepr ip:port} {publishing_port - applicable for direct}  {topics}
       e.g. For Direct messaging strategy
       python3 publisher_app.py direct "127.0.0.1:2181" 4000 topic1 topic2 topic3.....topicn
       Broker messaging strategy
       python3 publisher_app.py broker "127.0.0.1:2181" topic1 topic2 topic3.....topicn
'''
def topic_data_provider(topic):
    if topic == "temp":
        temp = randrange(1, 5)
        return str(temp)
    elif topic == "humidity":
        humidity = randrange(20, 25)
        return str(humidity)
    else:
        rand_data = randrange(100, 200)
        return str(rand_data)


# publish using specified strategy
def publish(strategy, topics):
    # keep publishing different topics every 5 seconds
    while True:
        if not topics:
            print("No topic to publish")
            break

        for topic in topics:
            topic_data = topic_data_provider(topic)
            strategy.publish(topic, topic_data)
        time.sleep(10)


# direct implementation
def direct_messaging_strategy(port, topics):
    subscriber = dmw.DirectPubMiddleware(port)
    publish(subscriber, topics)


# broker implementation
def broker_messaging_strategy(ips_ports, topics):
    broker = bmw.BrokerPubMiddleware(ips_ports)
    publish(broker, topics)


# create base topics & extract strategy
publish_topics = ["temp", "humidity"]
strategy = sys.argv[1] if len(sys.argv) > 1 else print("Please submit valid strategy (direct || broker)")

if strategy != 'direct' and strategy != 'broker':
    print("Please submit valid strategy (direct || broker)")
    sys.exit()

zookeeper_ip_port = ""
if len(sys.argv) > 2:
    zookeeper_ip_port = sys.argv[2]         

if zookeeper_ip_port == "":
    print("No zookeeper ip:port provided, terminating publisher app :(")
    sys.exit()

#Register publisher ip and port to the lamebroker
kzclient = kzcl.ZkClientService()
publisher_port = ""
if strategy == "direct":    
    #get the publisher port
    if len(sys.argv) > 3:
        publisher_port = sys.argv[3]

    #Add additional topics if provided for the direct strategy
    if len(sys.argv) > 4:
        for arg in sys.argv[4:]:
            publish_topics.append(arg)

    #Register the publisher to the zookeeper
    publisher_ip_port = hip.get_host_ip() + ":" + publisher_port
    print("Connecting to zookeeper at ip:port=> {}".format(zookeeper_ip_port))
    register_publisher_data_to_zookeeper = publisher_ip_port + '#'

    counter = 1
    for topic in publish_topics:
        if counter < len(publish_topics):
            register_publisher_data_to_zookeeper = register_publisher_data_to_zookeeper + topic + ','
        else:
            register_publisher_data_to_zookeeper = register_publisher_data_to_zookeeper + topic
        counter = counter + 1
    print("Registering publisher to the broker: {}".format(register_publisher_data_to_zookeeper))
    kzclient.create_node(const.PUBLISHERS_ROOT_PATH + const.PUBLISHERS_NODE_PREFIX, register_publisher_data_to_zookeeper, True, True)
else:
    #Add additional topics if provided for the broker strategy
    if len(sys.argv) > 3:
        for arg in sys.argv[3:]:
            publish_topics.append(arg)

print("Topics to publish: {}".format(publish_topics))

# initiate messaging based on which strategy is submitted
if strategy == "direct":   
    direct_messaging_strategy(publisher_port, publish_topics)
elif strategy == "broker":
    #Get the broker_ip_port for the broker strategy
    active_broker_node_value = kzcl.ZkClientService().get_broker(const.LEADER_ELECTION_ROOT_ZNODE)    
    broker_ip = active_broker_node_value.split(':')[0]
    broker_listening_port = active_broker_node_value.split(':')[1].split(',')[1]
    broker_ip_port = broker_ip + ":" + broker_listening_port
    broker_messaging_strategy(broker_ip_port, publish_topics)
