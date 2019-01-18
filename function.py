import sys
import boto3
from pprint import pprint

ec2 = boto3.client('ec2')
# !!!! Added region check/sort
def get_instance_limits():
    response = ec2.describe_instances()
    instances = response['Reservations']
    # pprint(instances)
    for instance in instances:
        pprint(instance['Instances'][0]['InstanceType'])
    
    
    
if __name__ == '__main__':
    # Map command line arguments to function arguments.
    get_instance_limits(*sys.argv[1:])