import boto3
import json

def lambda_handler(params, context):
    """
    Used to get a new id for a table.
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Ids')

    response = table.get_item(Key=params)

    if response is None:
        response = {
            'name': params['name'],
            'id': 0
        }
    else:
        response['value'] = response['value'] + 1

    table.put_item(Item=response)

    return response
