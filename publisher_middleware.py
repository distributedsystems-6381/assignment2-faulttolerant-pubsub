import zmq

class PublisherMiddleware():
    def __init__ (self, port):
        self.port = port
        self.socket = None
        self.configure()


    def configure(self):
        context = zmq.Context()
        binding_address = "tcp://*:%s" % self.port
        # acquire a publisher type socket
        print ("Publisher middleware binding on all interfaces on port {}".format(self.port))
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(binding_address)
    
    def publish(self, topic, value):
        print ("publishing topic: {}, data: {}".format(topic, value))
        published_data = topic + ":" + str (value)
        self.socket.send_string(published_data)