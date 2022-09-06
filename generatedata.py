import random
import json
from datetime import date,datetime
import time
starttime = time.time()
import os
import logging
from zipfile import ZipFile
import boto3

AWS_REGION = 'us-east-2'
AWS_PROFILE = 'test'
ENDPOINT_URL = 'http://localhost:4566'
LAMBDA_ZIP = './function.zip'
function_name = 'lambda'

#boto3.setup_default_session(profile_name=AWS_PROFILE)

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


def get_boto3_client(service):
    """
    Initialize Boto3 Lambda client.
    """
    try:
        lambda_client = boto3.client(
            service,
            region_name=AWS_REGION,
            endpoint_url=ENDPOINT_URL
        )
    except Exception as e:
        logger.exception('Error while connecting to LocalStack.')
        raise e
    else:
        return lambda_client



def invoke_function(filename):
    """
    Invokes the specified function and returns the result.
    """
    # Opening JSON file

    f = open(filename)
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    f.close()
    
    # returns JSON object as 
    # a dictionary
    print("dattttttt")
    print(data)
    print("dataaaa")

    try:
        lambda_client = get_boto3_client('lambda')
        response =  lambda_client.invoke(
            FunctionName=function_name,                
            Payload=json.dumps(data),
        )

        return json.loads(
            response['Payload']
            .read()
            .decode('utf-8')
        )
    except Exception as e:
        logger.exception('Error while invoking function')
        raise e

while True:
    meters = [{"smart_meter_msn": "ke16k59775", "customer_id":123},{"smart_meter_msn": "ke16k59708","customer_id":124
}]

    for meter in meters:
        meter["energy"] = random.randint(0, 9)
        meter["date"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        

    # Serializing json
    json_object = json.dumps(meters, indent=4)


    myobj = json_object

    #x = requests.post(url, data = "myobj")
    # Writing to sample.json
    print(meters)
    filename=str(str(datetime.now().strftime("%Y%m%d%I%M%S%p"))+".json")
    #with open(str(datetime.now().strftime("%Y%m%d%I%M%S%p"))+".json", "w") as outfile:
    with open(filename, "w") as outfile:    
        outfile.write(json_object)
    invoke_function(filename)
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))

