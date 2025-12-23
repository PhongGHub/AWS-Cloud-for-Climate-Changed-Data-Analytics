import json
import boto3
import base64
import os
import datetime

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    output = []
    
    print(f"Received {len(event['Records'])} records.")

    for record in event['Records']:
        # Kinesis data is base64 encoded
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        data = json.loads(payload)
        
        # Simple Transformation: Add 'processed_at' timestamp and 'status'
        data['processed_at'] = datetime.datetime.now().isoformat()
        
        # Alert Logic (Example)
        if data['temperature'] > 35.0:
            data['alert'] = 'HIGH_TEMP'
        else:
            data['alert'] = 'NORMAL'

        # Log for CloudWatch (Real-time monitoring potential)
        print(f"Processed Record: {json.dumps(data)}")
        
        # Write individual record to S3 (For a real Data Lake, utilize Kinesis Firehose for batching)
        # Here we do it per batch to keep it simple for a demo Project
        file_name = f"climate_data/{data['city']}/{data['timestamp']}.json"
        
        try:
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=file_name,
                Body=json.dumps(data)
            )
        except Exception as e:
            print(f"Error writing to S3: {e}")
            raise e

    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully processed {len(event["Records"])} records.')
    }
