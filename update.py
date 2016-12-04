import boto3
import json

def lambda_handler(params, context):
    """
    Update endpoint. Creates/Updates an item in a table and returns its updated
    form.

    Example input:
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
    