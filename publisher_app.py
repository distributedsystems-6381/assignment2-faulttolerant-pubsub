import sys
import publisher_middleware as pubmiddleware
import time

import zmq
from random import randrange    

published_topics = ["temp", "humidity"]
publisher_port = sys.argv[1] if len(sys.argv) > 1 else "5555"
broker_ip = sys.argv[2] if len(sys.argv) > 2 else ""
broker_port = sys.argv[3] if len(sys.argv) > 3 else ""
middleware = pubmiddleware.PublisherMiddleware(publisher_port, broker_ip, broker_port)

#any other arguments from 2nd and onwards are the topics to publish the messages
if len(sys.argv) > 2:
	for arg in sys.argv[2:]:
		published_topics.append(arg)
        
print("published topics: {}".format(published_topics))
#provides the topic data for a given topic
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
# keep publishing different topics
while True: 
    if not published_topics:
        print("No topic to publish") 
        break

    for topic in published_topics:
        topic_data = topic_data_provider(topic)
        middleware.publish(topic, topic_data)
    time.sleep(1)