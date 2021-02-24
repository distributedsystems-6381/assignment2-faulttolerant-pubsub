import zk_clientservice as zkcls
import host_ip_provider as hip

LEADER_ELECTION_ROOT_ZNODE = "/leaderelection"
BROKER_NODE_PREFIX = "/broker_"

host_ip = hip.get_host_ip()
current_broker_ip_port = ""

'''
    1. Create an emphemeral node
    2. Try to elect leader
    3. Set watch on the child nodes
'''

try:
    zk_service = zkcls.ZkClientService("127.0.0.1:2181")
    @zk_service.zk_client.ChildrenWatch(LEADER_ELECTION_ROOT_ZNODE)
    def watch_children(children):
        print("Children are now: %s" % children)

    zk_service.create_node(LEADER_ELECTION_ROOT_ZNODE, "leader_elector_root", False, False)
    zk_service.create_node(LEADER_ELECTION_ROOT_ZNODE + LEADER_ELECTION_ROOT_ZNODE, host_ip + ":4000", True, True)

finally:
    zk_service.zk_client.stop()
