import boto3
import os

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])


def handler(event, context):
    id = event['body']['id']
    response = table.query(
        KeyConditionExpression=Key('id').eq(id)
    )
    return response.get('Items')
