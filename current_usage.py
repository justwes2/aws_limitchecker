import boto3


class AccountUsage:
    current = {}

    def __init__(self):
        ec2_client =  boto3.client('ec2')
        response = ec2_client.describe_instances()
        instances = response['Reservations']
        current = {}
        for instance in instances:
            print instance['Instances'][0]['InstanceType'] 
            if instance['Instances'][0]['InstanceType'] in current:
                current[instance['Instances'][0]['InstanceType']] += 1
            else:
                current[instance['Instances'][0]['InstanceType']] = 1
        self.current = current
