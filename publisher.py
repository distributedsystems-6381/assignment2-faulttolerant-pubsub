import sys

import zmq
from random import randrange


context = zmq.Context()

server_address = sys.argv[1] if len(sys.argv) > 1 else "localhost"
connection_string = "tcp://" + server_address + ":5555"

socket = context.socket(zmq.PUB)
print ("Publisher connecting to proxy at: {}".format(connection_string))
socket.connect(connection_string)

# keep publishing 
while True:
    zipcode = randrange(1, 100000)
    temperature = randrange(-80, 135)
    relhumidity = randrange(10, 60)

    print ("Sending: %i %i %i" % (zipcode, temperature, relhumidity))
    socket.send_string("%i %i %i" % (zipcode, temperature, relhumidity))