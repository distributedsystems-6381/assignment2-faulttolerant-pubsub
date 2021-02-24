import sys
import time
import zmq
from random import randrange
import src.direct_pub_middleware as dmw
import src.broker_pub_middleware as bmw
import src.host_ip_provider as hip

# direct args => python3 publisher_app.py direct {lamebroker_ip:port} {publishing_port} topic1 topic2
#       e.g. "python3 publisher_app.py direct "10.0.0.6:7000" 5000 topic1 topic2"
# broker args => "python3 publisher_app.py broker {message_broker_ip:port} {publishing_port} topic1 topic2
#       e.g. "python3 publisher_app.py broker "10.0.0.6:7000" topic1 topic2"
# METHODS
# provides the topic data for a given topic
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
    # keep publishing different topics
    while True:
        if not topics:
            print("No topic to publish")
            break

        for topic in topics:
            topic_data = topic_data_provider(topic)
            strategy.publish(topic, topic_data)
        time.sleep(5)


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

#Register publisher ip and port to the lamebroker
publisher_port = ""
if strategy == "direct":
    broker_ip_port = ""
    if len(sys.argv) > 2:
        broker_ip_port = sys.argv[2]         

    if broker_ip_port == "":
        print("No broker ip:port provided")
        sys.exit()
    
    #Add additional topics if provided for the direct strategy
    if len(sys.argv) > 3:
        publisher_port = sys.argv[3]

    if len(sys.argv) > 4:
        for arg in sys.argv[4:]:
            publish_topics.append(arg)

    #Register the publisher to the broker
    context = zmq.Context()
    print("Connecting to broker at ip:port=> {}".format(broker_ip_port))
    broker_socket = context.socket(zmq.REQ)
    broker_socket.connect("tcp://{}".format(broker_ip_port))
    publisher_ip_port = hip.get_host_ip() + ":" + publisher_port
    register_publisher_data_to_broker = publisher_ip_port + '#'

    counter = 1
    for topic in publish_topics:
        if counter < len(publish_topics):
            register_publisher_data_to_broker = register_publisher_data_to_broker + topic + ','
        else:
            register_publisher_data_to_broker = register_publisher_data_to_broker + ',' + topic

    print("Registering publisher to the broker: {}".format(register_publisher_data_to_broker))
    broker_socket.send_string(register_publisher_data_to_broker)
    message = broker_socket.recv_string()
    print("Message received from broker: {}".format(message))
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
    broker_ip_port = sys.argv[2] if len(sys.argv) > 2 else "10.0.0.2:5559"
    broker_messaging_strategy(broker_ip_port, publish_topics)
