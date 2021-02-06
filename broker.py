import zmq
from random import randrange

context = zmq.Context()

publishers: {
    "topic1": ""
}

subscribers: {
    "topic1": "sub_ip"
}

# This is a proxy. We create the XSUB and XPUB endpoints
print ("This is proxy: creating xsub and xpubsockets")
xsubsocket = context.socket(zmq.XSUB)
xsubsocket.bind("tcp://*:5555")

xpubsocket = context.socket (zmq.XPUB)
xpubsocket.setsockopt(zmq.XPUB_VERBOSE, 1)
xpubsocket.bind ("tcp://*:5556")

# This proxy is needed to connect the two sockets.
# But what this means is that we cannot do anything here.
# We are just relaying things internally.
# This blocks
zmq.proxy (xsubsocket, xpubsocket)


def register_pub(topic, pub_identity):
    print("pub details")

def register_sub(topic, sub_identity):
    print("sub details")
