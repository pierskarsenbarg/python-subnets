import pulumi
from pulumi_awsx import ec2


class Network(pulumi.ComponentResource):
    vpc: ec2.Vpc

    def __init__(self, name: str, opts: pulumi.ResourceOptions = None):
        super().__init__("x:index:network", name, None, opts)

        self.vpc = ec2.Vpc("pk-vpc",
                           cidr_block="10.0.0.0/16",
                           subnet_strategy="Auto",
                           subnet_specs=[ec2.SubnetSpecArgs(
                               type=ec2.SubnetType.PUBLIC,
                               name="piers-subnet",
                               
                           )],
                           nat_gateways=ec2.NatGatewayConfigurationArgs(
                               strategy=ec2.NatGatewayStrategy.NONE
                           ))
        self.register_outputs({
            "vpc": self.vpc
        })
