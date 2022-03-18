import aws_cdk as cdk

from cdk_fargate_pyramid.cdk_fargate_pyramid_stack import CdkFargatePyramidStack

from shared_infrastructure.cherry_lab.environments import US_WEST_2


app = cdk.App()

CdkFargatePyramidStack(
    app,
    'CdkFargatePyramidStack2',
    env=US_WEST_2,
)

app.synth()
