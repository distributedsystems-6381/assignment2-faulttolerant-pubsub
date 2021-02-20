import zmq
import time
import sys

#args - python3 lamebroker.py 9000
topic_publishers = {}

def message_processor(message):
    msg_parts = message.split('#')
    if len(msg_parts) > 1:
        publisher_ip_port = msg_parts[0]
        topics = msg_parts[1].split(',')
        for topic in topics:
            if topic in topic_publishers:
                topic_publisher = topic_publishers[topic]
                topic_publishers[topic] = topic_publisher + ',' + publisher_ip_port
            else:
                topic_publishers[topic] = publisher_ip_port
        return "publisher registered"
    elif len(msg_parts) == 1:
        topic = msg_parts[0]       
        if topic in topic_publishers:
            return topic_publishers[topic]
    return ""         

port = "7000"
if len(sys.argv) > 1:
    port =  sys.argv[1]    

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

print('Lame broker started on port:{}'.format(port))

while True:
    #  Wait for next request from client
    message = socket.recv_string()
    print("Received request: {}", message)
    response = message_processor(message)
    print("Sending response: {}", message)   
    socket.send_string(response)