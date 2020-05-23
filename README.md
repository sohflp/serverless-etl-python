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

## Plugin installation

To make use of common libs from Python we are using the plugin `serverless-python-requirements`. To install the plugin execute the command:

```
serverless plugin install --name <pluginName>
```

Additional details about plugins installation in `https://www.serverless.com/framework/docs/providers/aws/cli-reference/plugin-install/`.

## Test your functions locally / remotely  with Serverless

To perform tests via Serverless use the command `serverless invoke` or `sls invoke`.

Example:
```
sls invoke [local] -f <myFunction> -p <myEventData.json>
```

1. `Ingestor`
```
sls invoke local -f ingestor -p test/lambda/s3-raw-stub.json
```

2. `Transformer`

```
sls invoke local -f transformer -p test/lambda/dynamo-stub.json
```