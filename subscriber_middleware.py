import zmq

class SubscriberMiddleware():
    def __init__ (self, publisher_address):
        self.port = "5555"
        self.socket_temp = None
        self.socket_humidity = None        
        self.publisherIp = publisher_address
        self.configure()

    def configure(self):
        context = zmq.Context()
        binding_address = "tcp://*:%s" % self.port
        # acquire a publisher type socket
        print ("Publisher middleware binding on all interfaces on port 5555")
        self.socket_temp = context.socket(zmq.PUB)
        self.socket.bind(binding_address)
    
    def publish(self, topic, message):
        print ("Sending: {}".format (topic))
        publiher_topic = topic + ":" + str (message)
        self.socket.send_string(publiher_topic)