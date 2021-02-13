import sys
import zmq

class SubscriberMiddleware():
    def __init__ (self, publisher_ip, port):
        self.publisherIp = publisher_ip
        self.port = port        
        self.notifyCallback = None
        self.sockets = []
        self.registered_topics = None                   

    def register(self, topics, callback = None):
        self.registered_topics = topics
        self.notifyCallback = callback
        self.configure()

    def configure(self):
        print("configuring the subscriber middleware")        
        server_address = "tcp://{}:{}".format(self.publisherIp, self.port)

        print("Connecting weather server at address: {}".format(server_address))
        context = zmq.Context()

        for topic in self.registered_topics:
            socket = context.socket(zmq.SUB)
            socket.connect(server_address)
            socket.setsockopt_string(zmq.SUBSCRIBE, topic)
            self.sockets.append(socket)        
        
        poller = zmq.Poller()
        for socket in self.sockets:
            poller.register(socket, zmq.POLLIN)

        while True:
            sockets = dict(poller.poll())
            for socket in sockets:
                message = socket.recv_string()
                topic, messagedata = message.split(":")                
                if self.notifyCallback != None:
                    self.notifyCallback(topic, messagedata) 
                