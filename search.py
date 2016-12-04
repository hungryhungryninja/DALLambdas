import boto3
import json
from boto3.dynamodb.conditions import Attr

def get_by_id(table, id_keys):
    """
    Retrieve the single item from the table whose id matches the key-value
    pairs specified in the id_keys map.abs
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table)

    response = table.get_item(Key=id_keys)

    if response.get('Item') is not None:
        return response['Item']
    else:
        return None

def get_all_matches(table, match_attributes={}, page_size=100, page_num=0):
    """
    Retrieve all of the elements from the table whose attributes match
    those specified in the match_attributes mapping
    """
    client = boto3.client('dynamodb')

    filter_expressions = None

    for key in match_attributes:
        filter_expression = Attr(key).contains(match_attributes[key])
        if filter_expressions is None:
            filter_expressions = filter_expression
        else:
            filter_expressions = filter_expressions | filter_expression


    paginator = client.get_paginator('scan')
    paginator_iterator = paginator.paginate(
        TableName=table,
        Select='ALL_ATTRIBUTES',
        PaginationConfig={
            'MaxItems': 1000,
            'PageSize': 100
        }
    )

    for page_idx, page in enumerate(paginator_iterator):
        if page_idx == page_num:
            return page['Items']

    return None

def lambda_handler(params, context):
    """
    Used to grab either a specific item or search for items in a table whose
    attributes contain certain values.

    If you are searching for a specific item, use a type of "get_id" and pass
    in the id keys in "id_keys".

    If you are searching for any values whose attributes match a specified
    attribute, use a type of "query" and pass in the attributes into
    "match_attributes".

    See parameter example below.

    Valid Parameters:
    {
        "table_name": "TableName",
        "type": "get_id" | "query",
        "id_keys": {
            "idkey1": "idvalue1"
        },
        "match_attributes": {
            "attribute_key": "attribute_value"
        }
    }
    """

    # Parse parameters to see what kind of search we need to do
    table_name = params["table_name"]

    if params["type"] == "get_id":
        return get_by_id(table_name, params["id_keys"])
    elif params["type"] == "query":
        return get_all_matches(table_name, params["match_attributes"])
