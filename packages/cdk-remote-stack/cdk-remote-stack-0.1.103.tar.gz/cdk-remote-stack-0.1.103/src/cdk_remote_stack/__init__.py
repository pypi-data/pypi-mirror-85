"""
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

cdk.CfnOutput(stack_jP, "TopicName", value="foo")

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

## always get the latest stack output

By default, the `StackOutputs` construct will always try to get the latest output from the source stack, you may opt out by setting `alwaysUpdate` to `false` to turn this feature off.

For example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
outputs = StackOutputs(stack_uS, "Outputs",
    stack=stack_jP,
    always_update=False
)
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


class StackOutputs(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-remote-stack.StackOutputs",
):
    """Represents the StackOutputs of the remote CDK stack."""

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        stack: aws_cdk.core.Stack,
        always_update: typing.Optional[builtins.bool] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param stack: The remote CDK stack to get the outputs from.
        :param always_update: Indicate whether always update the custom resource to get the new stack output. Default: true
        """
        props = StackOutputsProps(stack=stack, always_update=always_update)

        jsii.create(StackOutputs, self, [scope, id, props])

    @jsii.member(jsii_name="getAttString")
    def get_att_string(self, key: builtins.str) -> builtins.str:
        """Get the attribute value from the outputs.

        :param key: output key.
        """
        return jsii.invoke(self, "getAttString", [key])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> aws_cdk.core.CustomResource:
        """The outputs from the remote stack."""
        return jsii.get(self, "outputs")


@jsii.data_type(
    jsii_type="cdk-remote-stack.StackOutputsProps",
    jsii_struct_bases=[],
    name_mapping={"stack": "stack", "always_update": "alwaysUpdate"},
)
class StackOutputsProps:
    def __init__(
        self,
        *,
        stack: aws_cdk.core.Stack,
        always_update: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Properties of the StackOutputs.

        :param stack: The remote CDK stack to get the outputs from.
        :param always_update: Indicate whether always update the custom resource to get the new stack output. Default: true
        """
        self._values: typing.Dict[str, typing.Any] = {
            "stack": stack,
        }
        if always_update is not None:
            self._values["always_update"] = always_update

    @builtins.property
    def stack(self) -> aws_cdk.core.Stack:
        """The remote CDK stack to get the outputs from."""
        result = self._values.get("stack")
        assert result is not None, "Required property 'stack' is missing"
        return result

    @builtins.property
    def always_update(self) -> typing.Optional[builtins.bool]:
        """Indicate whether always update the custom resource to get the new stack output.

        :default: true
        """
        result = self._values.get("always_update")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackOutputsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "StackOutputs",
    "StackOutputsProps",
]

publication.publish()
