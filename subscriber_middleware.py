import sys
import zmq
import subscriber_app


publisherIp = sys.argv[1] if len(sys.argv) > 1 else "localhost"   
port = "5555"
server_address = "tcp://{}:{}".format(publisherIp, port)

print("Connecting weather server at address: {}".format(server_address))
context = zmq.Context()
socket_temp = context.socket(zmq.SUB)
socket_temp.connect(server_address)
socket_temp.setsockopt_string(zmq.SUBSCRIBE, "temp:2")

socket_humidity = context.socket(zmq.SUB)
socket_humidity.connect(server_address)
socket_humidity.setsockopt_string(zmq.SUBSCRIBE, "humidity:21")

# Initialize poll set
poller = zmq.Poller()
poller.register(socket_temp, zmq.POLLIN)
poller.register(socket_humidity, zmq.POLLIN)

while True:
    sockets = dict(poller.poll())
    if (socket_temp in sockets and sockets[socket_temp] == zmq.POLLIN):
        message = socket_temp.recv_string()
        topic, messagedata = message.split(":")
        subscriber_app.notify(topic, messagedata)

    if (socket_humidity in sockets and sockets[socket_humidity] == zmq.POLLIN):
        message = socket_humidity.recv_string()
        topic, messagedata = message.split(":")
        subscriber_app.notify(topic, messagedata)
                