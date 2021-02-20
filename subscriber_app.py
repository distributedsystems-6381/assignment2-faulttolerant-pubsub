import sys
import csv
from datetime import datetime
import threading

import host_ip_provider
import direct_sub_middleware as dmw
import broker_sub_middleware as bmw
import zmq

#e.g args "python3 subscriber_app.py direct 10.0.0.6:7000 topic1 topic2"
# capture subscriber IP for use in logger_function
subscriber_ip = host_ip_provider.get_host_ip()

#Extract the strategy to discover and disseminate the messages
strategy = ""
if len(sys.argv) > 1:    
    strategy = sys.argv[1]

if strategy != "direct" and strategy != "broker":
    print("Please submit valid strategy (direct || broker)")
    sys.exit()

#Get broker ip and port, passed in arg[2] as ip:port e.g. 10.0.0.5:4000
broker_ip_port = ""
if len(sys.argv) > 2:
    broker_ip_port = sys.argv[2] 

if broker_ip_port == "":
    print("No broker ip:port provided")
    sys.exit()

#Add topics of interests
subscribed_topics = []
if len(sys.argv) > 3:
    for arg in sys.argv[3:]:
        subscribed_topics.append(arg)
    print("Topics to subscribe:{}".format(subscribed_topics))

if len(subscribed_topics) == 0:
    print("Please provide topics to subscribe)")
    sys.exit()

publishers = []
#publishers for direct message based strategy
if strategy == "direct":
    context = zmq.Context()
    print("Retrieving topic publishers from broker running at ip:port => {}".format(broker_ip_port))
    broker_socket = context.socket(zmq.REQ)
    broker_socket.connect("tcp://{}".format(broker_ip_port))   
    for topic in subscribed_topics:
        broker_socket.send_string(topic)
        message = broker_socket.recv_string()
        print("Message received from broker: {}".format(message))
        topic_publishers = message.split(',')
        for topic_publisher in topic_publishers:
           publishers.append(topic_publisher)
#publishers for broker based message strategy - this will be broker ip:port
else:
    publishers = broker_ip_port.split(',')

print(publishers)

def logger_function(message):
    topic_data, message_id, message_sent_at_timestamp, publisher_ip = message.split("#")
    datetime_sent_at = datetime.strptime(message_sent_at_timestamp, '%Y-%m-%dT%H::%M::%S.%f')
    date_diff = datetime.now() - datetime_sent_at
    total_time_taken_milliseconds = date_diff.total_seconds() * 1000
    print('topic_data: {},'
          'message_id: {},'
          'message_sent_at_timestamp: {},'
          'publisher_ip: {}'.format(topic_data, message_id, datetime_sent_at, publisher_ip))

    with open('topic_meta_data.txt', mode='a') as topic_meta_data_file:
        topic_meta_data_writer = csv.writer(topic_meta_data_file, delimiter=',', quotechar='"',
                                            quoting=csv.QUOTE_MINIMAL)
        topic_meta_data_writer.writerow([publisher_ip, subscriber_ip, message_id, total_time_taken_milliseconds])


def notify(topic, message):
    print("Data received by this app, topic: {}, message: {}".format(topic, message))
    logger_thread = threading.Thread(target=logger_function, args=(message,), daemon=True)
    logger_thread.start()


# direct implementation
def direct_messaging_strategy(pubs, topics):
    # create the SubscriberMiddleware and register the topics of interest and the notify callback function
    publisher = dmw.DirectSubMiddleware(pubs)
    publisher.register(topics, notify)


def broker_messaging_strategy(brokers, topics):
    # create the BrokerSubscriberMiddleware and register the topics of interest and the notify callback function
    broker = bmw.BrokerSubMiddleware(brokers)
    broker.register(topics, notify)

# initiate messaging based on which strategy is submitted
if strategy == "direct" and publishers is not None:
    direct_messaging_strategy(publishers, subscribed_topics)
elif strategy == "broker" and publishers is not None:    
    broker_messaging_strategy(publishers, subscribed_topics)
else:
    print("Check that all necessary values have been submitted")