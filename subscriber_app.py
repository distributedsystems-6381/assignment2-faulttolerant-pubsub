import sys
import zmq
import subscriber_middleware as middleware

def notify(topic, message):
	print("Data received by this app, topic: {}, message: {}".format(topic, message))

publisher_ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
print("publisher ip: {}".format(publisher_ip))

publisher_port = sys.argv[2] if len(sys.argv) > 2 else "5555"
print("publisher port: {}".format(publisher_port))

subscribed_topics = []

if len(sys.argv) > 3:
	for arg in sys.argv[3:]:
		subscribed_topics.append(arg)

print(subscribed_topics)

sub_middleware = middleware.SubscriberMiddleware(publisher_ip, publisher_port)
sub_middleware.register(subscribed_topics, notify)