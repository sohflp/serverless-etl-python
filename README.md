# Simple ETL on AWS powered by Serverless, Lambda and Python

This repository contains a simple ETL process delivered for the DNX mentoring program. The following topics are contained in this project:

- AWS
    - Lambda
    - CloudFormation
    - DynamoDB
    - S3
    - CloudWatch
- Serverless framework
- Python
    - Python OO
    - Boto3 (AWS SDK)

## Architecture

![Simple ETL Architecture](images/simple-etl-architecture.png)

## Serverless Quick Start Guide

Tutorial available on `https://www.serverless.com/framework/docs/providers/aws/guide/quick-start/`.

## Authentication

Serverless uses the authentication configured in your AWS CLI, make sure you have access to your account configured in at least one profile before executing the deploy.

It's also possible to configure the credentials directly through Serverless, the following link provides details about this option `https://www.serverless.com/framework/docs/providers/aws/cli-reference/config-credentials/`.

## Serverless plugin installation and Python dependencies fix

To make use of Python common libs, install the plugin `serverless-python-requirements`. The command below is used for Serverless plugin installation.

```
serverless plugin install --name <pluginName>
```

To install `serverless-python-requirements`:

```
serverless plugin install --name serverless-python-requirements
```

Additional details about plugins installation in `https://www.serverless.com/framework/docs/providers/aws/cli-reference/plugin-install/`.

## Tests

To perform tests, Serverless use the command `serverless invoke` or `sls invoke`. 

Important notes:
- For local tests include the statement `local` after the command `invoke`.
- Specify the function name with `-f <functionName>`.
- If your function expect parameters create a file and specify with `-p <parameters.json>`.

Example:

```
sls invoke [local] -f <myFunction> -p <myEventData.json>
```

### AWS Python SDK

Boto3 is the AWS Python SDK that is already deployed in the Lambda runtimes, if you want to perform local tests you need to install this package before running the tests.

For `Python 2.x`:

```
pip install boto3
```

For `Python 3.x`:

```
pip3 install boto3
```

### Serverless tests (local and remote)

Use the following commands for local tests of the ETL Functions:

#### Ingestor

`Remote`

```
sls invoke -f ingestor -p test/lambda/s3-raw-stub.json
```

`Local`

```
sls invoke local -f ingestor -p test/lambda/s3-raw-stub.json
```

#### Transformer

`Remote`

```
sls invoke -f transformer -p test/lambda/dynamo-stub.json
```

`Local`

```
sls invoke local -f transformer -p test/lambda/dynamo-stub.json
```

### ! Bug note regarding local tests !

Since this application uses a plugin to assume the folder `src` as the main folder for Lambda deployments, there is a pending bug that impacts local tests with `sls invoke local`.

Before running local tests we need to update 2 pieces of code inside the project:

1. Include `src/` before the handler name in the file `sls/function.yml`.

Example:

```
ingestor:
  handler: src/lambda_ingestor.handler
  ...
```

2. Adjust Python import from `util.common` to `.util.common` inside the files `src/lambda_ingestor.py` and `src/lambda_transformer.py`.

Example:

```
from .util.common import IngestorUtils
```