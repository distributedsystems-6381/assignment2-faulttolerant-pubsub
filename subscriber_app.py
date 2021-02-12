import sys
import zmq

"""
#Socket to talk to server
context = zmq.Context()

socket = context.socket(zmq.SUB)

server_address = sys.argv[1] if len(sys.argv) > 1 else "localhost"
connection_string = "tcp://" + server_address + ":5555"

print("Collecting updates from weather server at: {}".format(connection_string))
socket.connect(connection_string)

temp_filter = sys.argv[2] if len(sys.argv) > 2 else "temp:1"
print("temperature-filter: {}".format(temp_filter))

if isinstance(temp_filter, bytes):
    temp_filter = temp_filter.decode('ascii')

socket.setsockopt_string(zmq.SUBSCRIBE, temp_filter)
while True:
	received_string = socket.recv_string()
	print("Received data from weather server: {}".format(received_string))
"""

def notify(topic, message):
	print("Data received by this app, topic: {}, message: {}".format(topic, message))
