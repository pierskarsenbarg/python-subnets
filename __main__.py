"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import ec2
from components.network import Network
from components.subnets import ProcessSubnets, ProcessSubnetsArgs

network = Network("network")

subnet_ids = ProcessSubnets("subnets", ProcessSubnetsArgs(
    network=network
))

pulumi.export("subnet_ids", subnet_ids.subnet_ids)
