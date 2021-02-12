import zmq

class PublisherMiddleware():
    def __init__ (self):
        self.port = "5555"
        self.socket = None
        self.configure()


    def configure(self):
        context = zmq.Context()
        binding_address = "tcp://*:%s" % self.port
        # acquire a publisher type socket
        print ("Publisher middleware binding on all interfaces on port 5555")
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(binding_address)
    
    def publish(self, topic, message):
        print ("Sending: {}".format (topic))
        publiher_topic = topic + ":" + str (message)
        self.socket.send_string(publiher_topic)