[![awscdk-jsii-template](https://img.shields.io/badge/built%20with-awscdk--jsii--template-blue)](https://github.com/pahud/awscdk-jsii-template)
[![NPM version](https://badge.fury.io/js/cdk-remote-stack.svg)](https://badge.fury.io/js/cdk-remote-stack)
[![PyPI version](https://badge.fury.io/py/cdk-remote-stack.svg)](https://badge.fury.io/py/cdk-remote-stack)
![Release](https://github.com/pahud/cdk-remote-stack/workflows/Release/badge.svg)

# cdk-remote-stack

Get outputs from cross-regional AWS CDK stacks

# Why

AWS CDK cross-regional cross-stack reference is not easy with the native AWS CDK construct library.

`cdk-remote-stack` aims to simplify the cross-regional cross-stack reference to help you easily build cross-regional multi-stack AWS CDK apps.

# Sample

Let's say we have two cross-region CDK stacks in the same cdk app:

1. **stackJP** - cdk stack in `JP` to create a SNS topic
2. **stackUS** - cdk stack in `US` to get the Outputs from `stackJP` and print out the SNS `TopicName` from `stackJP` Outputs.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_remote_stack import StackOutputs
import aws_cdk.core as cdk
import aws_cdk.aws_sns as sns

app = cdk.App()

env_jP = {
    "region": "ap-northeast-1",
    "account": process.env.CDK_DEFAULT_ACCOUNT
}

env_uS = {
    "region": "us-west-2",
    "account": process.env.CDK_DEFAULT_ACCOUNT
}

# first stack in JP
stack_jP = cdk.Stack(app, "demo-stack-jp", env=env_jP)

topic = sns.Topic(stack_jP, "Topic")

cdk.CfnOutput(stack_jP, "TopicName", value=topic.topic_name)

# second stack in US
stack_uS = cdk.Stack(app, "demo-stack-us", env=env_uS)

# ensure the dependency
stack_uS.add_dependency(stack_jP)

# get the stackJP stack outputs from stackUS
outputs = StackOutputs(stack_uS, "Outputs", stack=stack_jP)

remote_output_value = outputs.get_att_string("TopicName")

# the value should be exactly the same with the output value of `TopicName`
cdk.CfnOutput(stack_uS, "RemoteTopicName", value=remote_output_value)
```
