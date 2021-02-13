import sys
import publisher_middleware as pubmiddleware
import time

import zmq
from random import randrange

published_topics = {"temp", "humidity"}
publisher_port = sys.argv[1] if len(sys.argv) > 1 else "5555"
middleware = pubmiddleware.PublisherMiddleware(publisher_port)

def topic_data_provider(topic):
    if topic == "temp":
        temp = randrange(1, 5)
        return str(temp)
    if topic == "humidity":
        humidity = randrange(20, 25)
        return str(humidity)

# keep publishing different topics
while True: 
    if not published_topics:
        print("No topic to publish") 
        break

    for topic in published_topics:
        topic_data = topic_data_provider(topic)
        middleware.publish(topic, topic_data)
    time.sleep(5)