import logging
from unittest import result 
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3',endpoint_url="http://localhost:4566")

print(s3_client)

try:
    s3_client.create_bucket(Bucket = "mysecondbucket")
except ClientError as e:
    logging.error(e)

buckets_list = s3_client.list_buckets()

print('Existing buckets:')

for bucket in buckets_list['Buckets']:
    print(f'{bucket["Name"]}')

try:
    result= s3_client.upload_file("secondtest.txt","mysecondbucket","secondtest.txt")
except ClientError as e:
    logging.error(e)

stored_objects = s3_client.list_objects_v2(Bucket="mysecondbucket")
print('Bucket "mysecondbucket" contains:',)
for stored in stored_objects['Contents']:
    print(f'{stored["Key"]}')