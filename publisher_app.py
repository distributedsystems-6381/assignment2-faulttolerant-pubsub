import sys
import time
from random import randrange
import publisher_middleware as pubmiddleware
import broker_pub_middleware as brokermiddleware


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
    middleware = pubmiddleware.PublisherMiddleware(port)
    publish(middleware, topics)


# broker implementation
def broker_messaging_strategy(ips_ports, topics):
    broker = brokermiddleware.BrokerPubMiddleware(ips_ports)
    publish(broker, topics)


# create base topics & extract strategy
publish_topics = ["temp", "humidity"]
strategy = sys.argv[1] if len(sys.argv) > 1 else print("Please submit valid strategy (direct || broker)")

# add additional topics if provided
if len(sys.argv) > 3:
    for arg in sys.argv[3:]:
        publish_topics.append(arg)

    print("topics to publish: {}".format(publish_topics))

# initiate messaging based on which strategy is submitted
if strategy == "direct":
    publisher_port = sys.argv[2] if len(sys.argv) > 2 else "5555"
    direct_messaging_strategy(publisher_port, publish_topics)
elif strategy == "broker":
    broker_ip_port = sys.argv[2] if len(sys.argv) > 2 else "10.0.0.2:5559"
    broker_messaging_strategy(broker_ip_port, publish_topics)
