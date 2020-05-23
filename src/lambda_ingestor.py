from util.common import IngestorUtils

def handler(event, context):

    # Instantiate Data Utilities
    dataUtils = IngestorUtils()

    # Start logger
    dataUtils.log("INFO", "Starting")

    for idx, record in enumerate(event['Records']):
        try:
            # Transfer S3 trigger details to an object
            metadataItem  = dataUtils.extractMetadata(record)
            dataUtils.log("INFO", "Record[{}] => DynamoDB => Metadata => {}".format(idx, metadataItem))

            # Check if file format is valid
            if metadataItem['format'] != 'json':
                dataUtils.log("ERROR", "Record[{}] => Invalid file format".format(idx))
                continue

            # Input metadata in DynamoDB Table
            httpStatusCode = dataUtils.updateMetadata(metadataItem)
            dataUtils.log("INFO", "Record[{}] => DynamoDB update => HTTP {}".format(idx, httpStatusCode))
        
        except (Exception) as error:
            dataUtils.log("ERROR", "Record[{}] => Exception => {}".format(idx, error))

    dataUtils.log("INFO", "Finishing")

    return {
        "statusCode": 200,
        "body": {
            "message": "Ingestion concluded"
        }
    }