import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_fargate_pyramid.cdk_fargate_pyramid_stack import CdkFargatePyramidStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_fargate_pyramid/cdk_fargate_pyramid_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkFargatePyramidStack(app, "cdk-fargate-pyramid")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
