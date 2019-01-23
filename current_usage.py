import boto3
from boto3.dynamodb.conditions import Key, Attr
from pprint import pprint

class AccountUsage:
    current = {}
    limit = {}
    def __init__(self):
        ec2_client =  boto3.client('ec2')
        response = ec2_client.describe_instances()
        instances = response['Reservations']
        current = {}
        for instance in instances:
            # print instance['Instances'][0]['InstanceType'] 
            if instance['Instances'][0]['InstanceType'] in current:
                current[instance['Instances'][0]['InstanceType']] += 1
            else:
                current[instance['Instances'][0]['InstanceType']] = 1
        self.current = current

    def get_limits(self):
        table_name = 'ec2_limits'
        table_key = 'Account'
        table_value = 'coffayhouse'
        dynamodb_client = boto3.resource('dynamodb')
        table = dynamodb_client.Table(table_name)
        response = table.query(
            KeyConditionExpression = Key(table_key).eq(table_value)
        )
        pprint(response['Items'][0])
        limit = response['Items'][0]
        self.limit = limit

    def compare(self):
        comparison = [['Instance Type', 'Number in use', 'Current Limit', 'Percent Capacity']]
        region = 'us-east-1'
        for instance_type in self.current:
            comparison.append([instance_type, self.current[instance_type] , self.limit[region][instance_type], self.current[instance_type]/self.limit[region][instance_type]])
            print instance_type, self.current[instance_type] , self.limit[region][instance_type], self.current[instance_type]/self.limit[region][instance_type]