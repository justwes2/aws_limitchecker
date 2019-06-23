import sys
import boto3
from time import time

from connections import Connections
from current_usage import AccountUsage
from email_creation import EmailGenerator
from report_generation import ReportGenerator

def lambda_handler(event, context, **kwargs):
    print('Starting function\n-------------------------------------------------')
    start_time = time()
    print('Loading account credentials')
    accounts = Connections()


    print('Gathering Usage and Limit Data')
    comparisons = {}
    for count, account in enumerate(accounts.env_names):
        comparisons[account] = AccountUsage(accounts.env_names[count], accounts.connection_list[count])
        comparisons[account].get_limits()
        comparisons[account].compare()

    print('Generationg Email')
    email = EmailGenerator(comparisons)
    email.create_html
    email.send_email

    print('Creating Report')
    report = ReportGenerator(email.utilization)
    json = report.write_json()
    csv = report.write_csv

    print('Uplaoding Report to S3')
    push_json = report.push_to_s3(report.metadata)
    push_csv = report.push_to_s3(report.report)

    end_time = time() - start_time
    print('Time required: {0:.2f} s'.format(end_time))
    
    
    
if __name__ == '__main__':
    # Map command line arguments to function arguments.
    get_instance_limits(*sys.argv[1:])