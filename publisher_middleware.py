import zmq
import uuid
from datetime import datetime

class PublisherMiddleware():
    def __init__ (self, port, broker_ip, broker_port):
        self.port = port
        self.socket = None
        self.broker_ip = broker_ip
        self.broker_port = broker_port
        self.configure()       


    def configure(self):
        context = zmq.Context()        
        binding_address = "tcp://*:%s" % self.port

        if self.broker_ip != "" and self.broker_port != "":
            print("Connecting to broker at ip: {} and port: {}".format(self.broker_ip, self.broker_port))
        else:
            # acquire a publisher type socket
            print ("Publisher middleware binding on all interfaces on port {}".format(self.port))
            self.socket = context.socket(zmq.PUB)
            self.socket.bind(binding_address)
    
    def publish(self, topic, value):
        print ("publishing topic: {}, data: {}".format(topic, value))
        message_id = str(uuid.uuid4())
        message_sent_at_timestamp = datetime.now().strftime('%Y-%m-%dT%H::%M::%S.%f')
        #topic:data:message_id:message_sent_at_timestamp
        published_data = topic + "#" + str (value) + "#" + message_id + "#"+ message_sent_at_timestamp
        self.socket.send_string(published_data)