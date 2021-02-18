import sys
import csv
from datetime import datetime
import threading

import host_ip_provider
import direct_sub_middleware as dmw
import broker_sub_middleware as bmw


# capture subscriber IP for use in logger_function
subscriber_ip = host_ip_provider.get_host_ip()


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


# create topics array, extract strategy, extract publishers
subscribed_topics = []
strategy = sys.argv[1] if len(sys.argv) > 1 else print("Please submit valid strategy (direct || broker)")
publishers_ip_port = sys.argv[2] if len(sys.argv) > 2 else "localhost:5555"
print("publisher ip: {}".format(publishers_ip_port))
publishers = publishers_ip_port.split(',')

# add additional topics if provided
if len(sys.argv) > 3:
    for arg in sys.argv[3:]:
        subscribed_topics.append(arg)
    print("topics to subscribe:\n {}".format(subscribed_topics))

# initiate messaging based on which strategy is submitted
if strategy == "direct" and publishers is not None:
    direct_messaging_strategy(publishers, subscribed_topics)
elif strategy == "broker" and publishers is not None:
    broker_messaging_strategy(publishers, subscribed_topics)
else:
    print("Check that all necessary values have been submitted")
