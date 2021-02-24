import sys
import logging as logger

import kazoo.client as kzcl
import kazoo.exceptions as ke

class ZkClientService():
    #zkservice_ip_ports is the comma separated ip:port where zookeeper services are running
    #e.g 127.0.0.1:2181,127.0.0.1:2020
    def __init__(self, zkservice_ip_ports):        
        self.zk_client = kzcl.KazooClient(zkservice_ip_ports)
        self.zk_client.start()
    
    def create_node(self, node_path_to_create, node_value, is_ephemeral, is_sequential):
        print("Creating node")
        created_node_path = ""
        try:
            node_stat = self.zk_client.exists(node_path_to_create)
            if node_stat is None:
                created_node_path = self.zk_client.create(node_path_to_create,node_value.encode('utf-8'), ephemeral=is_ephemeral, sequence=is_sequential)
            else:
                created_node_path = node_path_to_create

        except ke.KazooException as e:
            logger.error('Kazoo exception: '+ str(e))

        except Exception as e:
            logger.error('Exception occured: '+ str(e))
        
        return created_node_path
    
    def watch_node(self, node_path, watch_func):
        try:
            self.zk_client.get_children(node_path, watch=watch_func)

        except ke.KazooException as e:
            logger.error('Kazoo exception: '+ str(e))

        except Exception as e:
            logger.error('Exception occured: '+ str(e))
    
    def get_children(self, node_path):
        print("Creating node")
        childNodes = None
        try:
            childNodes = self.zk_client.get_children(node_path)              
        except ke.KazooException as e:
            logger.error('Kazoo exception: '+ str(e))
        except Exception as e:
            logger.error('Exception occured: '+ str(e))
        
        return childNodes
