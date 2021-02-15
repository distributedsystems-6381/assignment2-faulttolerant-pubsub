import zmq
import random
import sys
import time

port = "5559"
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://10.0.0.2:%s" % port)
publisher_id = random.randrange(0, 9999)
while True:
    topic = random.randrange(1, 10)
    messagedata = "server#%s" % publisher_id
    print("%s %s" % (topic, messagedata))
    socket.send_string("%d %s" % (topic, messagedata))
    time.sleep(1)
