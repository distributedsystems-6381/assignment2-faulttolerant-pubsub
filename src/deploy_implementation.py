#!/usr/bin/env python3

import os  # OS level utilities
import sys
import argparse  # for command line parsing
import shutil

from signal import SIGINT
from time import time

import subprocess

# These are all Mininet-specific
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import CLI
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.util import pmonitor

# This is our topology class created specially for Mininet
from pubsub_topology import PubSub_Topo

from mininet.node import OVSController


##################################
# Command line parsing
##################################
def parseCmdLineArgs():
    # parse the command line
    parser = argparse.ArgumentParser()

    # @NOTE@: You might need to make appropriate changes
    #                          to this logic. Just make sure.

    # add optional arguments
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1", help="Zookeeper IP, default 127.0.0.1")
    parser.add_argument("-p", "--port", type=int, default=2181, help="Zookeeper port, default is 2181")
    parser.add_argument("-r", "--racks", type=int, choices=[1, 2, 3, 4], default=1,
                        help="Number of racks, choices 1, 2, 3, or 4")
    parser.add_argument("-t", "--strategy", type=str, choices=["direct", "broker"], default="direct",
                        help="Dissemination strategy to use: direct or broker, default is direct")
    parser.add_argument("-P", "--publishers", type=int, default=1, help="Number of publishers, default 1")
    parser.add_argument("-PT", "--publishertopics", required=True, type=str, nargs='*', default="",
                        help="topics to publish")
    parser.add_argument("-S", "--subscribers", type=int, default=1, help="Number of subscribers, default 1")
    parser.add_argument("-ST", "--subscribertopics", required=True, type=str, nargs='*', default="",
                        help="topics to subscribe to")

    # add positional arguments in that order
    # parser.add_argument("datafile", help="Big data file")

    # parse the args
    args = parser.parse_args()

    return args


def convertToStr(input_seq):
    # Join all the strings in list
    final_str = ' '.join(input_seq)
    return final_str


##################################
#  Generate the commands file to be sources
#
# @NOTE@: You will need to make appropriate changes
#                          to this logic.
##################################
def genCommandsFile(args):
    try:
        # create the commands file. It will overwrite any previous file with the
        # same name.
        cmds = open("commands.txt", "w")
        cmdz = []

        # create zookeeper command
        zk_path = "/home/tito/workspace/zookeeper"
        zk_cmd = "sudo " + zk_path + "/bin/zkServer.sh start"
        cmdz.append(zk_cmd)
        cmds.write(zk_cmd)

        # create broker commands
        lamebroker_cmd = "python3 lamebroker.py 5000"
        broker_cmd = "python3 broker.py 5559 5560"
        for i in range(3):
            cmd_str = lamebroker_cmd if str(args.strategy) == "direct" else broker_cmd
            cmdz.append(cmd_str)
            cmds.write(cmd_str)

        #  next create the commands for the publishers
        for i in range(args.publishers):
            # extract subscriber topics
            pub_tops = convertToStr(args.publishertopics)
            if str(args.strategy) == "direct":
                cmd_str = "python3 publisher_app.py " + str(args.strategy) + " \"" + str(args.ip) + ":" + \
                          str(args.port) + "\"" + " 4000 " + pub_tops
            else:
                cmd_str = "python3 publisher_app.py " + str(args.strategy) + " \"" + str(args.ip) + ":" + \
                          str(args.port) + "\" " + pub_tops
            cmdz.append(cmd_str)
            cmds.write(cmd_str)

        #  next create the commands for subscribers
        k = 4 + args.publishers  # starting index for subscriber hosts (zookeeper + brokers + publishers)
        for i in range(args.subscribers):
            # extract subscriber topics
            sub_tops = convertToStr(args.subscribertopics)
            # write command
            cmd_str = "python3 subscriber_app.py " + str(args.strategy) + " \"" + str(args.ip) + ":" + \
                      str(args.port) + "\" " + sub_tops
            cmdz.append(cmd_str)
            cmds.write(cmd_str)

        # close the commands file.
        cmds.close()
        return cmdz

    except:
        print("Unexpected error in run mininet:", sys.exc_info()[0])
        raise


######################
# main program
######################
def main():
    # Create and run the publishers & subscribers via direct or broker strategy in Mininet topology

    # parse the command line
    parsed_args = parseCmdLineArgs()

    # instantiate our topology
    print("Instantiate topology")
    topo = PubSub_Topo(Racks=parsed_args.racks, P=parsed_args.publishers, S=parsed_args.subscribers)

    # create the network
    print("Instantiate network")
    net = Mininet(topo, link=TCLink, controller=OVSController)

    # activate the network
    print("Activate network")
    net.start()

    # debugging purposes
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)

    # debugging purposes
    print("Testing network connectivity")
    net.pingAll()

    # clean up data from previous zookeeper deploys
    dir_path = '/tmp/zookeeper/version-2'
    try:
        shutil.rmtree(dir_path)
        print("Directory '%s' has been removed successfully" % dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))

    # print("Generating commands file to be sourced")
    a = genCommandsFile(parsed_args)

    for i in range(len(net.hosts)):
        net.hosts[i].sendCmd(a[i])

    # run the cli
    CLI(net)

    # @NOTE@
    # You should run the generated commands by going to the
    # Mininet prompt on the CLI and typing:
    #     source commands.txt
    # Then, keep checking if all python jobs (except one) are completed
    # You can look at the *.out files which have all the debugging data
    # If there are errors in running the python code, these will also
    # show up in the *.out files.

    # cleanup
    # net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    main()
