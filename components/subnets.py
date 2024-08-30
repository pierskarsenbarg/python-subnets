from typing import Mapping, Sequence
import pulumi
from components.network import Network
import pulumi_aws as aws


class ProcessSubnetsArgs:
    def __init__(
            self,
            network: Network
    ):
        self.network = network


class ProcessSubnets(pulumi.ComponentResource):
    subnet_ids: tuple[pulumi.Output[str], pulumi.Output[str], pulumi.Output[str]]

    def __init__(
        self, name: str, args: ProcessSubnetsArgs, opts: pulumi.ResourceOptions = None
    ):
        super().__init__("x:index:processsubnets", name, {}, opts)

        self.subnet_ids = args.network.vpc.subnets.apply(lambda subnet_args: process_subnets(subnet_args))

        self.register_outputs({
            "subnet_ids": self.subnet_ids
        })

        def process_subnets(subnets: Sequence[aws.ec2.Subnet]):
            login_subnets = pulumi.Output.from_input("") 
            control_subnets = pulumi.Output.from_input("")
            worker_subnets = pulumi.Output.from_input("")

            for subnet in subnets:     
                login_subnets = pulumi.Output.all(subnet.tags, subnet.id, login_subnets).apply(lambda args: check_tags(args[0], args[1], args[2], "login_subnets"))
                control_subnets = pulumi.Output.all(subnet.tags, subnet.id, control_subnets).apply(lambda args: check_tags(args[0], args[1], args[2], "control_subnets"))
                worker_subnets = pulumi.Output.all(subnet.tags, subnet.id, worker_subnets).apply(lambda args: check_tags(args[0], args[1], args[2], "worker_subnets"))

            return trim_subnet_string(login_subnets), trim_subnet_string(control_subnets), trim_subnet_string(worker_subnets)
        
        def check_tags(tags: Mapping[str, str], subnet_id: str, subnet_id_string: str, tag_name: str):
                        if tag_name in tags:
                            subnet_id_string = f"{subnet_id_string}{subnet_id},"
                        return subnet_id_string

        def trim_subnet_string(subnet_string: pulumi.Output[str]):
            return subnet_string.apply(lambda subnet_str: subnet_str[:-1])
