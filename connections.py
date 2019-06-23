import boto3

class Connections():
    sts_client = boto3.client('sts')
    connection_list = []
    # Add a connection for each account you want to check
    connection_list.append(sts_client.assume_role(
        RoleArn = "arn:aws(-us-gov):iam:<ACCOUNT NUMBER>:role/<ROLE NAME>",
        RoleSessionName = "AssumeRoleSession1")
    )
    # Add the account names in the same order as the connections
    # TODO: this should be expressed as a dict, not parallel lists
    env_names = ['<ACCOUNT NAME']