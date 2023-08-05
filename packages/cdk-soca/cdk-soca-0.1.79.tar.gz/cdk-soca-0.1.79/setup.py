import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-soca",
    "version": "0.1.79",
    "description": "cdk-soca is an AWS CDK construct library that allows you to create the Scale-Out Computing on AWS with AWS CDK in TypeScript or Python",
    "license": "Apache-2.0",
    "url": "https://github.com/pahud/cdk-soca.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud Hsieh<pahudnet@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/pahud/cdk-soca.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_soca",
        "cdk_soca._jsii"
    ],
    "package_data": {
        "cdk_soca._jsii": [
            "cdk-soca@0.1.79.jsii.tgz"
        ],
        "cdk_soca": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-ec2>=1.63.0, <2.0.0",
        "aws-cdk.aws-efs>=1.63.0, <2.0.0",
        "aws-cdk.aws-elasticsearch>=1.63.0, <2.0.0",
        "aws-cdk.aws-iam>=1.63.0, <2.0.0",
        "aws-cdk.aws-s3>=1.63.0, <2.0.0",
        "aws-cdk.core>=1.63.0, <2.0.0",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
