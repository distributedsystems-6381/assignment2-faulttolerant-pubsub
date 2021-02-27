import zmq
import time, threading
import sys
import zk_leaderelector as le
import constants as const
import zk_clientservice as kzcl

'''
The functions of the broker:
 Command line params: i) zookeeper_ip:port ii) broker_port e.g. pyhton3 lamebroker.py "127.0.0.1:2181" 5000
 1. Creates an ehemeral sequence node in the zookeeper under /leaderelection using LeaderEelector object
    e.g. /leaderelection/broker_0000000001, node_value = "brokerip:port"
 2. Try to elect leader with LeaderEelector, and keep watch on the other stand-by broker nodes 
    by registering a callback function with LeaderEelector object, which is called when a broker leader node changes.
    And as part of this callback refreshes the topic publisgers list as well
 3. Also, every 5 seconds keep refreshing the connected publishers
 4. Bind to a tcp socket on all network interfaces on the given port, by default it binds to port 7000
    for the subscribers to connect to retrive publisher's topics and ip:port
'''
#publisher refresh_interval in seconds
REFRESH_PUBS_IN_SECONDS = 5
#args - python3 lamebroker.py 9000
topic_publishers = {}

lock = threading.Lock()

port = "7000"
if len(sys.argv) > 1:
    port =  sys.argv[1]

print('Lame broker started on port:{}'.format(port))

#message parameter format= pub_ip:port#topic1, topic2, topic3 etc.
def message_processor(message):
    msg_parts = message.split('#')
    #Register publishers ip:port and topics (this data comes from publishers)
    try:
        lock.acquire()
        if len(msg_parts) > 1:
            publisher_ip_port = msg_parts[0]
            topics = msg_parts[1].split(',')
            for topic in topics:
                if topic in topic_publishers:
                    topic_publisher = topic_publishers[topic]
                    topic_publishers[topic] = topic_publisher + ',' + publisher_ip_port
                else:
                    topic_publishers[topic] = publisher_ip_port
            return "publisher registered"
        #get the publishers for the given topic (this is call from subscriber)
        elif len(msg_parts) == 1:
            topic = msg_parts[0]       
            if topic in topic_publishers:
                return topic_publishers[topic]
    finally:
        lock.release()
    return "" 

zk_client_svc = kzcl.ZkClientService()
def refresh_publishers():
    publishers_nodes = zk_client_svc.get_children(const.PUBLISHERS_ROOT_PATH)
    if publishers_nodes != None and len(publishers_nodes) > 0:        
        for pub_node in publishers_nodes:
            pub_node_data = zk_client_svc.get_node_value(const.PUBLISHERS_ROOT_PATH + '/' + pub_node)
            message_processor(pub_node_data)            
    print("list of topic publishers: {}".format(topic_publishers))    

threading.Timer(REFRESH_PUBS_IN_SECONDS, refresh_publishers).start()

def leader_election_callback():
    print("Performing leader election work")
    #hydrate publishers and topic
    refresh_publishers()

#Try to elect a broker leader
leader_elector = le.LeaderEelector(zk_client_svc, const.LEADER_ELECTION_ROOT_ZNODE, const.BROKER_NODE_PREFIX)
leader_elector.try_elect_leader(leader_election_callback, port)

#Bind the tcp socket to the supplied port
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

while True:
    #Wait for next request from client
    message = socket.recv_string()
    print("Received request: {}", message)
    response = message_processor(message)
    print("Sending response: {}", message)   
    socket.send_string(response)