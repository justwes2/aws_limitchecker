import boto3
import json
from pprint import pprint

table_name = 'ec2_limits'

with open('account_limits.json') as f:
    data = json.load(f)

pprint(data)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

table.put_item(
   Item = data
)
