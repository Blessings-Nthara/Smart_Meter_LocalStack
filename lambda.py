from ast import Expression
import logging
from unicodedata import decimal

from unittest import result
from xml.etree.ElementTree import tostring 
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
import json

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb',endpoint_url='http://localhost:4566')
table = dynamodb.Table('Customers')
#response = table.scan()
#data = response['Items']

def handler(event, context):
    data= json.dumps(event)
    data =  json.loads(data)
    charge = 2.00
   
    for i in data:
        x = json.dumps(i)
        y = json.loads(x)
        #response = table.get_item(Key={'smart_meter_msn':i["smart_meter_msn"]})
                

        table.update_item(
            Key = {'customer_id':i["customer_id"],'smart_meter_msn':i["smart_meter_msn"]},
            UpdateExpression = "SET readings = list_append(readings, :vals)",
            #UpdateExpression = 'SET last_name = :value1',
            ExpressionAttributeValues={
                #':vals': [json.dumps(i)],
                ':vals': [x],

            },
            
             ReturnValues="UPDATED_NEW"
            )
        
        response = table.get_item(Key={'customer_id':i["customer_id"],'smart_meter_msn':i["smart_meter_msn"]})
        total = 0.00
        #f=json.loads(response["Item"]["readings"][0])
        #return f["customer_id"]

        #d=json.load(f)

        for bill in response["Item"]["readings"]:
            total = Decimal(json.loads(bill)["energy"]) + Decimal(total)
            balance = Decimal(response["Item"]["balance"]) - (Decimal(json.loads(bill)["energy"])*Decimal(charge))
            table.update_item(
            Key = {'customer_id':i["customer_id"],'smart_meter_msn':i["smart_meter_msn"]},
            UpdateExpression = "SET balance = :r",
            ExpressionAttributeValues={
                ':r': balance,

            },
            
             ReturnValues="UPDATED_NEW"
            )  
        
        table.update_item(
            Key = {'customer_id':i["customer_id"],'smart_meter_msn':i["smart_meter_msn"]},
            UpdateExpression = "SET total_energy = :r",
            ExpressionAttributeValues={
                ':r': total,

            },
            
             ReturnValues="UPDATED_NEW"
            )   


        

    #response = table.get_item(Key={'customer_id':123, 'last_name':'Joe'})

    logging.info('Hands-on-cloud')
    return {
        "message": "response"
    }