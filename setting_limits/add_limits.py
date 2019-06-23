import boto3
import json

table_name = 'ec2_limits'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Talbe(table_name)

with open('account_limits.json') as f:
    data_mgmt = json.load(f)

table.put_item(
    Item = data_mgmt
)