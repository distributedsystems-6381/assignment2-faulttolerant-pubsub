import sys
import zmq


class BrokerSubMiddleware():
    def __init__(self, broker_ip, broker_port):
        self.broker_ip = broker_ip
        self.broker_port = broker_port
        self.notifyCallback = None
        self.sockets = []
        self.registered_topics = None

    def register(self, topics, callback=None):
        self.registered_topics = topics
        self.notifyCallback = callback
        self.configure()

    def configure(self):
        print("configuring the subscriber middleware to use the broker strategy")
        server_address = "tcp://{}:{}".format(self.broker_ip, self.broker_port)

        print("Connecting to broker at address: {}".format(server_address))
        context = zmq.Context()

        # for all of the registered topics set filter
        for topic in self.registered_topics:
            socket = context.socket(zmq.SUB)
            socket.connect(server_address)
            socket.setsockopt_string(zmq.SUBSCRIBE, topic)
            self.sockets.append(socket)

        # keep polling for the sockets
        poller = zmq.Poller()
        for socket in self.sockets:
            poller.register(socket, zmq.POLLIN)

        while True:
            sockets = dict(poller.poll())
            for socket in sockets:
                message = socket.recv_string()
                topic, messagedata = message.split(":")
                # send the received data to the subscriber app using the registered callback
                if self.notifyCallback != None:
                    self.notifyCallback(topic, messagedata)
