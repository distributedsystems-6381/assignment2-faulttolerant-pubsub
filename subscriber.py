import sys
import zmq
import broker

#Socket to talk to server
context = zmq.Context()

socket = context.socket(zmq.SUB)

server_address = sys.argv[1] if len(sys.argv) > 1 else "localhost"
connection_string = "tcp://" + server_address + ":5556"


print("Collecting updates from weather server proxy at: {}".format(connection_string))
socket.connect(connection_string)

zip_filter = sys.argv[2] if len(sys.argv) > 2 else "10001"

if isinstance(zip_filter, bytes):
    zip_filter = zip_filter.decode('ascii')

socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)


# Process 5 updates
total_temp = 0
for update_nbr in range(5):
    string = socket.recv_string()
    zipcode, temperature, relhumidity = string.split()
    total_temp += int(temperature)

print("Average temperature for zipcode '%s' was %dF" % (zip_filter, total_temp / (update_nbr+1))