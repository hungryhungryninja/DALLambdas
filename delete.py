import boto3
import json

def lambda_handler(params, context):
    """
    Data deletion endpoint. Takes in a table name to delete from and a
    key map for the document that we want to delete.

    Example:
    {
        "table_name": "Ingredients",
        "key": {
            "name": "garlic"
        }
    }
    """
    dynamodb = boto3.resource('dynamodb')
    table_name = params['table_name']
    table = dynamodb.Table(table_name)

    response = table.delete_item(Key=params['key'])

    return response
