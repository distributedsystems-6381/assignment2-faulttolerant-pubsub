import zmq
import sys


def run_broker(listening_port, publishing_port):
    print("starting ZMQ broker")
    try:
        context = zmq.Context(1)
        # Socket facing clients
        frontend = context.socket(zmq.SUB)
        frontend.bind("tcp://*:{}".format(listening_port))
        print("configured to listen to publisher interfaces via port {}".format(listening_port))

        frontend.setsockopt_string(zmq.SUBSCRIBE, "")

        # Socket facing services
        backend = context.socket(zmq.PUB)
        backend.bind("tcp://*:{}".format(publishing_port))
        print("configured to publish to registered subscribers via port {}".format(publishing_port))

        zmq.device(zmq.FORWARDER, frontend, backend)
        print("configuration complete")
    except Exception as e:
        print(e)
        print("bringing down ZMQ device")
    finally:
        pass
        frontend.close()
        backend.close()
        context.term()


# extract broker config
listen = sys.argv[1] if len(sys.argv) > 1 else print("Please submit valid port")
publish = sys.argv[2] if len(sys.argv) > 2 else print("Please submit valid port")
if publish == listen:
    print("Listening port and Publishing port cannot be the same")
else:
    run_broker(listen, publish)

