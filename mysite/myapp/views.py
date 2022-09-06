from django.shortcuts import render
from django.http import HttpResponse

import logging
from unittest import result 
import boto3
from botocore.exceptions import ClientError

from decimal import Decimal
import json
from django.views.decorators.csrf import csrf_exempt


import os


# Create your views here.

def index(request):
    """ Initializing our localstack to use dynamodb """
    
    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.INFO)
    dynamodb = boto3.resource('dynamodb',endpoint_url='http://localhost:4566')
    table = dynamodb.Table('Customers')
    response = table.scan()
    data = response['Items']

    return render(request,"index.html",{'customers':data})

@csrf_exempt
def energy(request,customer_id,smart_meter_msn):    
    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.INFO)
    dynamodb = boto3.client('dynamodb',endpoint_url='http://localhost:4566')

    # Use the DynamoDB client get item method to get a single item
    response = dynamodb.get_item(
    TableName="Customers",
    Key={
        'customer_id': {'N': str(customer_id)},
        'smart_meter_msn': {'S': str(smart_meter_msn)}
    }
    )
    energy_consumption_list = []

    for item in (response["Item"]["readings"]["L"]):
        energy_consumption_list.append(json.loads(item["S"]))
    return render(request,"energy.html",{'customers':response["Item"],'energy_consumption_list':energy_consumption_list})

def analytics(request,customer_id,smart_meter_msn):
    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.INFO)
    dynamodb = boto3.client('dynamodb',endpoint_url='http://localhost:4566')

    # Use the DynamoDB client get item method to get a single item
    response = dynamodb.get_item(
    TableName="Customers",
    Key={
        'customer_id': {'N': str(customer_id)},
        'smart_meter_msn': {'S': str(smart_meter_msn)}
    }
    )
    energy_consumption_list = []
    energy_consumption_list_graph = []
    dates_list=[]
    for item in (response["Item"]["readings"]["L"]):
        energy_consumption_list.append(json.loads(item["S"]))
    for item in energy_consumption_list:
        print(item["energy"])
        energy_consumption_list_graph.append(item["energy"])
        dates_list.append(item["date"])

    
    return render(request,"analytics.html",{'customers':response["Item"],'energy_consumption_list':energy_consumption_list,'energy_list':energy_consumption_list_graph,'dates_list':dates_list})
