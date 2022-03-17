import aws_cdk as cdk

from aws_cdk.aws_ec2 import SecurityGroup

from aws_cdk.aws_ecs import ContainerImage

from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedTaskImageOptions

from constructs import Construct

from shared_infrastructure.cherry_lab.vpcs import VPCs


class CdkFargatePyramidStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpcs = VPCs(
            self,
            'VPCs'
        )
        security_group = SecurityGroup.from_security_group_id(
            self,
            'encd_sg',
            'sg-022ea667',
            mutable=False
        )
        application_image = ContainerImage.from_asset(
            'cdk_fargate_pyramid/pyramid/'
        )
        fargate_service = ApplicationLoadBalancedFargateService(
            self,
            'TestFargatePyramidApp',
            vpc=vpcs.default_vpc,
            cpu=1024,
            desired_count=1,
            task_image_options=ApplicationLoadBalancedTaskImageOptions(
                image=application_image,
            ),
            memory_limit_mib=2048,
            public_load_balancer=True,
            security_groups=[
                security_group,
            ],
            assign_public_ip=True,
        )
        fargate_service.target_group.configure_health_check(
            interval=cdk.Duration.seconds(60),
        )
        scalable_task = fargate_service.service.auto_scale_task_count(
            max_capacity=4,
        )
        scalable_task.scale_on_request_count(
            'RequestCountScaling',
            requests_per_target=600,
            target_group=fargate_service.target_group,
            scale_in_cooldown=cdk.Duration.seconds(60),
            scale_out_cooldown=cdk.Duration.seconds(60),
        )
