import sys
import zmq
import subscriber_middleware as middleware
import subprocess
import csv
from datetime import datetime
import threading

publisher_ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
print("publisher ip: {}".format(publisher_ip))

publisher_port = sys.argv[2] if len(sys.argv) > 2 else "5555"
print("publisher port: {}".format(publisher_port))

subscribed_topics = []

#any other arguments from 3 onwards are the topic filters
if len(sys.argv) > 3:
	for arg in sys.argv[3:]:
		subscribed_topics.append(arg)

print(subscribed_topics)

subscriber_ip = subprocess.Popen(['ifconfig | grep -e "inet\s" | awk \'NR==1{print $2}\''], stdout=subprocess.PIPE, shell=True)
(IP,errors) = subscriber_ip.communicate()
subscriber_ip.stdout.close()
subscriber_ip_string = IP.decode('utf-8').strip("\n")

def logger_function(message):
	topic_data, message_id, message_sent_at_timestamp = message.split("#")
	datetime_sent_at = datetime.strptime(message_sent_at_timestamp, '%Y-%m-%dT%H::%M::%S.%f')
	date_diff = datetime.now() - datetime_sent_at
	total_time_taken_milliseconds = date_diff.total_seconds()*1000
	print('topic_data: {}, message_id: {}, message_sent_at_timestamp: {}'.format(topic_data, message_id, datetime_sent_at))

	with open('topic_meta_data.txt', mode='a') as topic_meta_data_file:
		topic_meta_data_writer = csv.writer(topic_meta_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		topic_meta_data_writer.writerow([publisher_ip, subscriber_ip_string, message_id, total_time_taken_milliseconds])		


def notify(topic, message):
	print("Data received by this app, topic: {}, message: {}".format(topic, message))
	logger_thread = threading.Thread(target=logger_function, args=(message,), daemon=True)
	logger_thread.start()
	
#create the SubscriberMiddleware and register the topics of interest and the notify callback function
sub_middleware = middleware.SubscriberMiddleware(publisher_ip, publisher_port)
sub_middleware.register(subscribed_topics, notify)