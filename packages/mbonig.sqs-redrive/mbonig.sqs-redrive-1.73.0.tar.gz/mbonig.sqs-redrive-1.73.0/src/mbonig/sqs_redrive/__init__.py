"""
# SQS Redrive

This construct creates a Lambda function that you can use to move SQS messages from one queue to another. This is often used for moving Dead Letter Queue messages back to the original queue for reprocessing.

# This is a pre-release!

This is a quick first-draft. All the options that will likely need to be added to accomodate a large
number of use-cases are still needed. If you'd like to make requests or help update this construct, please
open an [Issue](https://github.com/mbonig/cicd-spa-website/issues) or a [PR](https://github.com/mbonig/cicd-spa-website/pulls).

## What Gets Created

A Lambda function and related policy which moves SQS queue messages from one queue to another.

## Example

This creates two external queues and then creates the Lambda to move from the deadLetterQueue to the mainQueue

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from ...lib.sqs_redrive import SqsRedrive
from aws_cdk.aws_sqs import Queue

app = cdk.App()
stack = cdk.Stack(app, "test-stack")

main_queue = Queue(stack, "main-queue")
dead_letter_queue = Queue(stack, "dlq-queue")
SqsRedrive(stack, "SqsRedriveConstructStack",
    main_queue=main_queue,
    dead_letter_queue=dead_letter_queue
)
```

*Note: this is the integration test (`cdk synth`).*

## Input Properties

What are the inputs to your constructs?

|property|description|example
|---|---|---
|mainQueue|The destination queue for the messages.|`new Queue(stack, 'main-queue')`
|deadLetterQueue|The source queue of the messages.|`new Queue(stack, 'dead-letter-queue')`

## Overriding Lambda Props

You can supply your own properties to the Lambda Function constructor. They're mashed together with some defaults.
Pay attention to the order:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
self.redrive_function = NodejsFunction(self, f"{id}-queue-redrive",
    function_name=id,
    entry=join(__dirname, "sqs-redrive.queue-redrive.ts"),
    (SpreadAssignment ...props.lambdaProps
      props.lambda_props),
    environment={
        "QUEUE_URL": props.main_queue.queue_url,
        "DLQ_URL": props.dead_letter_queue.queue_url,
        (SpreadAssignment ...props?.lambdaProps?.environment
          props.lambda_props.environment)
    }
)
```

`functionName` and `entry` can be overridden. Environment variables will always be splatted with the two queue URLs so
you never have to worry about specifying those (you can, of course, override them, but if you're going that far then
why are you using this construct?).

## Output Properties

After constructed, you can gain access to the Lambda Function:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
redrive = SqsRedrive(stack, "SqsRedriveConstructStack",
    main_queue=main_queue,
    dead_letter_queue=dead_letter_queue
)
```

## Design Notes

This is early design and serves one very specific use-case. If you have suggestions on how to make this better, please open an [Issue in Github](https://github.com/mbonig/sqs-redrive/issues).

## Contributing

Please open Pull Requests and Issues on the [Github Repo](https://github.com/mbonig/sqs-redrive).

## License

MIT
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

import aws_cdk.aws_lambda
import aws_cdk.aws_lambda_nodejs
import aws_cdk.aws_sqs
import aws_cdk.core


class SqsRedrive(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/sqs-redrive.SqsRedrive",
):
    """A construct that encompasses a Lambda Function that will move all messages from a source queue (dlq) to a destination queue (main)."""

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        dead_letter_queue: aws_cdk.aws_sqs.IQueue,
        main_queue: aws_cdk.aws_sqs.IQueue,
        lambda_props: typing.Optional[aws_cdk.aws_lambda_nodejs.NodejsFunctionProps] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param dead_letter_queue: The SQS Queue that holds dead-letters.
        :param main_queue: The SQS Queue that will re-process the DLQ messages.
        :param lambda_props: Props to hand to the underlying Lambda Function that does all the heavy lifting. These props are applied after the default functionName and entry file, but before the environment variables are setup:: functionName: id, entry: join(__dirname, 'sqs-redrive.queue-redrive.ts'), ...props.lambdaProps, environment: { QUEUE_URL: props.mainQueue.queueUrl, DLQ_URL: props.deadLetterQueue!.queueUrl, ...props?.lambdaProps?.environment, }, Code of the Lambda Function was originally lifted from here: https://www.stackery.io/blog/failed-sqs-messages/
        """
        props = SqsRedriveProps(
            dead_letter_queue=dead_letter_queue,
            main_queue=main_queue,
            lambda_props=lambda_props,
        )

        jsii.create(SqsRedrive, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="redriveFunction")
    def redrive_function(self) -> aws_cdk.aws_lambda.IFunction:
        """The Lambda Function that will move messages from the DLQ to the main queue."""
        return jsii.get(self, "redriveFunction")

    @redrive_function.setter # type: ignore
    def redrive_function(self, value: aws_cdk.aws_lambda.IFunction) -> None:
        jsii.set(self, "redriveFunction", value)


@jsii.data_type(
    jsii_type="@matthewbonig/sqs-redrive.SqsRedriveProps",
    jsii_struct_bases=[],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "main_queue": "mainQueue",
        "lambda_props": "lambdaProps",
    },
)
class SqsRedriveProps:
    def __init__(
        self,
        *,
        dead_letter_queue: aws_cdk.aws_sqs.IQueue,
        main_queue: aws_cdk.aws_sqs.IQueue,
        lambda_props: typing.Optional[aws_cdk.aws_lambda_nodejs.NodejsFunctionProps] = None,
    ) -> None:
        """Props for the SqsRedrive construct creation.

        :param dead_letter_queue: The SQS Queue that holds dead-letters.
        :param main_queue: The SQS Queue that will re-process the DLQ messages.
        :param lambda_props: Props to hand to the underlying Lambda Function that does all the heavy lifting. These props are applied after the default functionName and entry file, but before the environment variables are setup:: functionName: id, entry: join(__dirname, 'sqs-redrive.queue-redrive.ts'), ...props.lambdaProps, environment: { QUEUE_URL: props.mainQueue.queueUrl, DLQ_URL: props.deadLetterQueue!.queueUrl, ...props?.lambdaProps?.environment, }, Code of the Lambda Function was originally lifted from here: https://www.stackery.io/blog/failed-sqs-messages/
        """
        if isinstance(lambda_props, dict):
            lambda_props = aws_cdk.aws_lambda_nodejs.NodejsFunctionProps(**lambda_props)
        self._values: typing.Dict[str, typing.Any] = {
            "dead_letter_queue": dead_letter_queue,
            "main_queue": main_queue,
        }
        if lambda_props is not None:
            self._values["lambda_props"] = lambda_props

    @builtins.property
    def dead_letter_queue(self) -> aws_cdk.aws_sqs.IQueue:
        """The SQS Queue that holds dead-letters."""
        result = self._values.get("dead_letter_queue")
        assert result is not None, "Required property 'dead_letter_queue' is missing"
        return result

    @builtins.property
    def main_queue(self) -> aws_cdk.aws_sqs.IQueue:
        """The SQS Queue that will re-process the DLQ messages."""
        result = self._values.get("main_queue")
        assert result is not None, "Required property 'main_queue' is missing"
        return result

    @builtins.property
    def lambda_props(
        self,
    ) -> typing.Optional[aws_cdk.aws_lambda_nodejs.NodejsFunctionProps]:
        """Props to hand to the underlying Lambda Function that does all the heavy lifting.

        These props are applied
        after the default functionName and entry file, but before the environment variables are setup::

           functionName: id,
           entry: join(__dirname, 'sqs-redrive.queue-redrive.ts'),
           ...props.lambdaProps,
           environment: {
                 QUEUE_URL: props.mainQueue.queueUrl,
                DLQ_URL: props.deadLetterQueue!.queueUrl,
                ...props?.lambdaProps?.environment,
              },

        Code of the Lambda Function was originally lifted from here: https://www.stackery.io/blog/failed-sqs-messages/
        """
        result = self._values.get("lambda_props")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsRedriveProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SqsRedrive",
    "SqsRedriveProps",
]

publication.publish()
