import logging
from unittest import result 
import boto3
from botocore.exceptions import ClientError

from decimal import Decimal
import json

""" Initializing our localstack to use dynamodb """
dynamodb = boto3.client('dynamodb',endpoint_url='http://localhost:4566')


""" An entry point of the application """
def _init():

    table_name = 'Customers'

    existing_tables = dynamodb.list_tables()['TableNames']

    if table_name not in existing_tables:
        create_customers_table()
        with open("customerdata.json") as json_file:
            customer_list = json.load(json_file,parse_float=Decimal)
            register_customers(customer_list)
    else:
        with open("customerdata.json") as json_file:
            customer_list = json.load(json_file,parse_float=Decimal)
            register_customers(customer_list)
    

""" A function to create customers table in dynamodb"""
def create_customers_table():
    table = dynamodb.create_table(
    TableName='Customers',
    KeySchema=[
        {
            'AttributeName': 'customer_id',
            'KeyType': 'HASH' #Partition key
        },
        {
            'AttributeName': 'smart_meter_msn',
            'KeyType': 'RANGE' #Sort key
        },
    ],
    AttributeDefinitions = [
        {
            'AttributeName': "customer_id",
            'AttributeType': "N"
        },
        {
            'AttributeName': "smart_meter_msn",
            'AttributeType': "S"
        }
    ],
    ProvisionedThroughput = 
    { 
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

def register_customers(customers):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    table = dynamodb.Table('Customers')

    for customer in customers:
        last_name = customer["last_name"]
        customer_id = customer["customer_id"]
        print("Adding customer:", last_name,customer_id)
        table.put_item(Item=customer)


_init()






