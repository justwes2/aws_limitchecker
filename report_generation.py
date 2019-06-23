import boto3
import json
import csv
from datetime import datetime

class ReportGenerator:
    utilization = None
    now = ''
    metadata = None
    report = None

    def __init__(self, utilization):
        self.utilization = utilization
        self.now = str(datetime.now())

    def write_json(self):
        # This is a json object that holds information about the report. Fee free to omit

        # This is the path for prod
        fh = open("/tmp/ec2_utilization.json", "w")
        # This is the path for local testing
        # fh = open("ec2_utilization.json", "w")
        content = {
            "name" : "EC2 Usage Limits"
            "description" : "A report showing number of EC2 instances by class"
            "author" : "Barbara Gorden"
        }
        fh.write(json.dumps(content))
        fh.close()
        self.metadata = 'ec2_utilizatization.json'

    def write_csv(self):
        # This is the path for prod
        with open('/tmp/ec2_utilization.csv', 'wb') as csvfile:
        # This is the path for local testing
        # with open('ec2_utilization.csv', 'wb') as csvfile:
            f = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            f.writerow(['Report gerneated at {}'.format(self.now)])
            f.writerow([
                'Account',
                'Instance Type',
                'Number in Use',
                'Current Limit',
                'Percent Capacity'
                ])
            for row in self.utilization:
                f.writerow(row)
        self.report = 'ec2_utiization.csv'

    def push_to_s3(self, file):
        s3 = boto3.client('s3')
        bucket_name = '<Bucket Name Here'>

        # for prod
        filepath = "/tmp/{}".format(file)
        # for local testing
        # filepath = "{}".format(file)

        upload = s3.upload_file(filepath, bucket_name, file)