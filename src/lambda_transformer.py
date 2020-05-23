from util.common import TransformerUtils

def handler(event, context):

    # Instantiate Data Utilities
    dataUtils = TransformerUtils()

    # Start logger
    dataUtils.log("INFO", "Starting")

    for idx, record in enumerate(event['Records']):
        try:
            # Retrieve file key from DynamoDB Streams
            fileKey = dataUtils.getFileKey(record)
            dataUtils.log("INFO", "Record[{}] => Processing file => {}".format(idx, fileKey))

            # Get metadata from DynamoDB
            metadata = dataUtils.getMetadata(fileKey)
            dataUtils.log("INFO", "Record[{}] => DynamoDB => Read File Metadata => {}".format(idx, metadata))

            # Verify if metadata is in the catalog
            if not metadata:
                dataUtils.log("ERROR", "Record[{}] => DynamoDB => Metadata not found".format(idx))
                continue
            
            # Get the content of the file in S3
            json = dataUtils.readFile(metadata["bucket"], metadata["fileKey"])
            dataUtils.log("INFO", "Record[{}] => S3 => Read File Content".format(idx))

            # Transform your data before the transfer to the next bucket
            json = dataUtils.transform(json)
            dataUtils.log("INFO", "Record[{}] => S3 => Transform JSON content".format(idx))

            # Transfer single file to the next bucket
            dataUtils.transfer(self.getVariable('bucketDataStaging'), fileKey, json)
            dataUtils.log("INFO", "Record[{}] => File transferred to staging bucket".format(idx))
        
        except (Exception) as error:
            dataUtils.log("ERROR", "Record[{}] => Exception => {}".format(idx, error))

    dataUtils.log("INFO", "Finishing")

    return {
        "statusCode": 200,
        "body": {
            "message": "Ingestion concluded"
        }
    }