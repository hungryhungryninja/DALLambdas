import boto3
import json

def lambda_handler(params, context):
    """
    Data creation endpoint. Takes in a table name to insert into and an
    item that we want to insert.

    Example:
    {
        "table_name": "Ingredients",
        "item": {
            "name": "garlic"
        }
    }
    """
    dynamodb = boto3.resource('dynamodb')
    table_name = params['table_name']
    table = dynamodb.Table(table_name)

    response = table.put_item(Item=params['item'])

    return response
