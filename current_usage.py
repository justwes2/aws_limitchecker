import boto3
from boto3.dynamodb.conditions import Key, Attr
from pprint import pprint

class AccountUsage:
    account = ''
    current = {}
    limit = {}
    comparison = []

    def __init__(self, account, connection):
        current = {}
        credentials = connection['Credentials']

        ec2_client =  boto3.client(
            'ec2',
            aws_access_key_id = credentials['AccessKeyId'],
            aws_secret_access_key = credentials['SecretAccessKey'],
            aws_session_token = credentials['SessionToken'],
            )
        filer = [
            {
                'Name' : 'instance-state-name',
                'Values' : [
                    'running'
                ]
            }
        ]
        response = ec2_client.describe_instances(
            Filters = filer
        )
        instances = response['Reservations']
        
        for instance in instances:
            if instance['Instances'][0]['InstanceType'] in current:
                current[instance['Instances'][0]['InstanceType']] += 1
            else:
                current[instance['Instances'][0]['InstanceType']] = 1
        self.current = current
        self.account = account

    def get_limits(self):
        table_name = 'ec2_limits'
        table_key = 'Account'
        table_value = self.account
        dynamodb_client = boto3.resource('dynamodb')
        table = dynamodb_client.Table(table_name)
        response = table.query(
            KeyConditionExpression = Key(table_key).eq(table_value)
        )
        
        limit = response['Items'][0]
        self.limit = limit

    def compare(self):
        comparison = []
        region = 'us-east-1'
        for instance_type in self.current:
            comparison.append([
                self.account, 
                instance_type, 
                self.current[instance_type], 
                int(self.limit[region][instance_type], 
                "{}".format(int(self.current[instance_type]/self.limit[region][instance_type]*100))
                ])
            self.comparison = comparison