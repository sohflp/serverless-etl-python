import os
import json
import logging
import boto3
import psycopg2
import pytz

from boto3.dynamodb.conditions import Key
from datetime import datetime

class DataUtils:

    def __init__(self):
        # Start logger
        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, 'INFO'))

        # Environment Variables (Serverless / Lambda)
        self.env = {}
        self.env['bucketDataRaw']     = os.environ.get('bucketDataRaw')
        self.env['bucketDataStaging'] = os.environ.get('bucketDataStaging')
        self.env['tableMetadata']     = os.environ.get('tableMetadata')

        # AWS Resources
        self.session = boto3.session.Session()
        self.s3 = boto3.resource('s3')
        self.dynamoDB = boto3.resource('dynamodb', region_name=self.session.region_name)
    
    def getAllVariables(self):
        return self.env

    def getVariable(self, key):
        return self.env[key]
    
    def log(self, type, message):
        if type == "INFO":
            self.logger.info(message)
        elif type == "WARNING":
            self.logger.warning(message)
        elif type == "ERROR":
            self.logger.error(message)
        else:
            self.logger.info(message)

    def putItemDynamoDB(self, table, item):
        dynamoTable = self.dynamoDB.Table(table)
        queryResponse = dynamoTable.put_item(Item=item)
        
        return queryResponse

    def queryItemDynamoDB(self, table, key, value):
        dynamoTable = self.dynamoDB.Table(table)
        queryResponse = dynamoTable.query(
            KeyConditionExpression = Key(key).eq(value)
        )
        items = queryResponse['Items']
        
        if items:
            return items[0]
        else:
            return []

    def readS3File(self, bucket, fileKey):
        # Open the S3 file based on bucket + file
        s3Object = self.s3.Object(bucket, fileKey)
        
        # Read the file content and return a JSON
        fileContent = s3Object.get()['Body'].read().decode('utf-8')
        
        return fileContent

class IngestorUtils(DataUtils):

    def __init__(self):
        # Parent class constructur
        DataUtils.__init__(self)

    def extractMetadata(self, record):
        # Auxiliar variables
        s3path = "s3://{}/{}"
        eventName = record["eventName"].split(':')[-1]

        # Populate file metadata
        metadata = {}
        metadata["bucket"]      = record["s3"]["bucket"]["name"]
        metadata["fileKey"]     = record["s3"]["object"]["key"]
        metadata["format"]      = record["s3"]["object"]["key"].split(".")[-1].lower()
        metadata["size"]        = record["s3"]["object"]["size"]
        metadata["s3Path"]      = s3path.format(metadata.get("bucket"),metadata.get("fileKey"))
        metadata["createdAt"]   = datetime.now().isoformat() # DynamoDB hack for datetime
        metadata["event"]       = eventName.upper()

        return metadata

    def getMetadata(self, fileKey):
        metadataTable = self.getVariable("tableMetadata")

        return self.queryItemDynamoDB(metadataTable, 'fileKey', fileKey)

    def updateMetadata(self, metadataItem):
        metadataTable = self.getVariable("tableMetadata")
        response = self.putItemDynamoDB(metadataTable, metadataItem)
        
        if response:
            return response["ResponseMetadata"]["HTTPStatusCode"]
        else:
            return []

class TransformerUtils(IngestorUtils):

    def __init__(self):
        # Parent class constructur
        IngestorUtils.__init__(self)
    
    def getFileKey(self, record):
        return record["dynamodb"]["Keys"]["fileKey"]["S"]

    def readS3File(self, bucket, fileKey):
        # Open file via parent method
        fileContent = IngestorUtils.readFile(self, bucket, fileKey)
        return json.loads(fileContent)

    def transform(self, content):
        # TODO: Implement your transformation logic here
        return content

    def transfer(self, bucket, fileKey, data):
        # Input the data in the new file
        s3object = self.s3.Object(bucket, fileKey)
        s3object.put(
            Body=(bytes(json.dumps(data).encode('UTF-8')))
        )