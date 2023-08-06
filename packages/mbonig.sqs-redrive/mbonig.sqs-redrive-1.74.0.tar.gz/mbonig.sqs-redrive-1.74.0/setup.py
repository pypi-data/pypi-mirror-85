import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "mbonig.sqs-redrive",
    "version": "1.74.0",
    "description": "A redrive construct to use with an SQS queue and it's dead letter queue",
    "license": "MIT",
    "url": "https://github.com/mbonig/sqs-redrive",
    "long_description_content_type": "text/markdown",
    "author": "Matthew Bonig<matthew.bonig@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mbonig/sqs-redrive"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "mbonig.sqs_redrive",
        "mbonig.sqs_redrive._jsii"
    ],
    "package_data": {
        "mbonig.sqs_redrive._jsii": [
            "sqs-redrive@1.74.0.jsii.tgz"
        ],
        "mbonig.sqs_redrive": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-lambda-nodejs>=1.67.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.67.0, <2.0.0",
        "aws-cdk.aws-sqs>=1.67.0, <2.0.0",
        "aws-cdk.core>=1.67.0, <2.0.0",
        "constructs>=3.0.4, <4.0.0",
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
