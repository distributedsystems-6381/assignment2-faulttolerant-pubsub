import zmq


class BrokerPubMiddleware():
    def __init__(self, broker_ip):
        self.broker_ip = broker_ip
        self.port = "5559"
        self.socket = None
        self.configure()

    def configure(self):
        print("configuring the publisher middleware to use the broker strategy")
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        binding_address = "tcp://{}:{}".format(self.broker_ip, self.port)
        self.socket.connect(binding_address)

    def publish(self, topic, value):
        print("publishing topic: {}, data: {}".format(topic, value))
        published_data = topic + ":" + str(value)
        self.socket.send_string(published_data)
