import sys
import unittest
import zk_clientservice as zkcls
import host_ip_provider as hip

class TestZKClientServiceMethods(unittest.TestCase):
    def setUp(self):
        self.zk_client_service = zkcls.ZkClientService('127.0.0.1:2181')
    
    def test_create_non_emphemeral(self):
        node_path = '/my/znode/n_'
        create_node_path = self.zk_client_service.create_node(node_path, hip.get_host_ip(), False, False, True)
        self.assertTrue(create_node_path.startswith(node_path))

    def test_create_emphemeral_node(self):
        node_path = '/my/znode/n_'
        create_node_path = self.zk_client_service.create_node(node_path, hip.get_host_ip(), False, True, True)
        self.assertTrue(create_node_path.startswith(node_path))

if __name__ == '__main__':
    unittest.main()