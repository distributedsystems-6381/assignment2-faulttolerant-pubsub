import sys
import subscriber_middleware as directmiddleware
import broker_sub_middleware as brokermiddleware


def notify(topic, message):
    print("Data received by this app, topic: {}, message: {}".format(topic, message))


# direct implementation
def direct_messaging_strategy(ip, port, topics):
    print("publisher ip: {}".format(ip))
    print("publisher port: {}".format(port))

    # create the SubscriberMiddleware and register the topics of interest and the notify callback function
    direct_middleware = directmiddleware.SubscriberMiddleware(ip, port)
    direct_middleware.register(topics, notify)


def broker_messaging_strategy(ip, port, topics):
    print("broker ip: {}".format(ip))
    print("broker port: {}".format(port))

    # create the BrokerSubscriberMiddleware and register the topics of interest and the notify callback function
    broker_middleware = brokermiddleware.BrokerSubMiddleware(ip, port)
    broker_middleware.register(topics, notify)


# create topics array & extract strategy
publish_topics = []
strategy = sys.argv[1] if len(sys.argv) > 1 else print("Please submit valid strategy (direct || broker)")

# extract publisher/broker info
ip = sys.argv[2] if len(sys.argv) > 2 else print("Please submit valid IP")
port = sys.argv[3] if len(sys.argv) > 3 else print("Please submit valid port")

# add additional topics if provided
if len(sys.argv) > 4:
    for arg in sys.argv[4:]:
        publish_topics.append(arg)

    print("topics to publish: {}".format(publish_topics))

# initiate messaging based on which strategy is submitted
if strategy == "direct" and ip is not None and port is not None:
    direct_messaging_strategy(ip, port, publish_topics)
elif strategy == "broker" and ip is not None and port is not None:
    broker_messaging_strategy(ip, port, publish_topics)
else:
    print("Check that all necessary values have been submitted")