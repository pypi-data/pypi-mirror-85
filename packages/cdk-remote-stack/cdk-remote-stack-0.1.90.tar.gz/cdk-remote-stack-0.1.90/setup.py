import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-remote-stack",
    "version": "0.1.90",
    "description": "Get outputs from cross-regional AWS CDK stacks",
    "license": "Apache-2.0",
    "url": "https://github.com/pahud/cdk-remote-stack.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud Hsieh<hunhsieh@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/pahud/cdk-remote-stack.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_remote_stack",
        "cdk_remote_stack._jsii"
    ],
    "package_data": {
        "cdk_remote_stack._jsii": [
            "cdk-remote-stack@0.1.90.jsii.tgz"
        ],
        "cdk_remote_stack": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-iam>=1.62.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.62.0, <2.0.0",
        "aws-cdk.aws-logs>=1.62.0, <2.0.0",
        "aws-cdk.aws-sns>=1.62.0, <2.0.0",
        "aws-cdk.core>=1.62.0, <2.0.0",
        "aws-cdk.custom-resources>=1.62.0, <2.0.0",
        "constructs>=3.2.0, <4.0.0",
        "jsii>=1.14.1, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
