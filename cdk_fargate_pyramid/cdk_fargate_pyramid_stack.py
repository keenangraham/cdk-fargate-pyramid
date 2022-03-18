import aws_cdk as cdk

from aws_cdk.aws_ec2 import SecurityGroup
from aws_cdk.aws_ec2 import InstanceType
from aws_cdk.aws_ec2 import InstanceClass
from aws_cdk.aws_ec2 import InstanceSize
from aws_cdk.aws_ec2 import SubnetSelection
from aws_cdk.aws_ec2 import SubnetType

from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_ecs import Secret

from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedTaskImageOptions

from aws_cdk.aws_rds import DatabaseInstance
from aws_cdk.aws_rds import DatabaseInstanceEngine
from aws_cdk.aws_rds import PostgresEngineVersion

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
        engine = DatabaseInstanceEngine.postgres(
            version=PostgresEngineVersion.VER_14_1
        )
        database_name = 'igvfd'
        database = DatabaseInstance(
            self,
            'TestFargatePyramidAppPostgres',
            database_name=database_name,
            engine=engine,
            instance_type=InstanceType.of(
                InstanceClass.BURSTABLE3,
                InstanceSize.MEDIUM,
            ),
            vpc=vpcs.default_vpc,
            vpc_subnets=SubnetSelection(
                subnet_type=SubnetType.PUBLIC,
            ),
            allocated_storage=10,
            max_allocated_storage=20,
            security_groups=[
                security_group,
            ],
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
                environment={
                    'DB_HOST': database.instance_endpoint.hostname,
                    'DB_NAME': database_name,
                },
                secrets={
                    'DB_PASSWORD': Secret.from_secrets_manager(
                        database.secret,
                        'password'
                    ),
                },
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
