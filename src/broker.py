import zmq
import sys
import zk_clientservice as kzcl
import zk_leaderelector as le
import constants as const


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
    #Try to elect a broker leader
    zk_client_svc = kzcl.ZkClientService()
    leader_elector = le.LeaderEelector(zk_client_svc, const.LEADER_ELECTION_ROOT_ZNODE, const.BROKER_NODE_PREFIX)
    #The broker node value for broker strategy e.g. node_path = /leaderelection/broker_0000000001, node_value = broker_ip:publishing_port,listening_port
    # e.g node_value = 10.0.0.5:2000,3000
    leader_elector.try_elect_leader(None, publish + "," + listen)
    run_broker(listen, publish)

