import publisher_middleware as pubmiddleware
import time

import zmq
from random import randrange


middleware = pubmiddleware.PublisherMiddleware()

# keep publishing different topics
while True:
    temp = randrange (1, 5)
    topic = "temp"
    message = str(temp)
    middleware.publish(topic, message)

    humidity = randrange (20, 101)   
    topic = "humidity" 
    message = str(humidity)
    middleware.publish(topic, message)
    time.sleep(5)