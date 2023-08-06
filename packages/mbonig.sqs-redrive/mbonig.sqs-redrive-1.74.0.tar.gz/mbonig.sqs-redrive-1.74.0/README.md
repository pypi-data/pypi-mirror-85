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
