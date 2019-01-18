import sys
import time
import boto3
from pprint import pprint

from current_usage import AccountUsage


# !!!! Added region check/sort
def get_instance_limits():
    print 'Starting function'
    start_time = time.time()
    current = AccountUsage()

    pprint(current)

    end_time = time.time() - start_time
    print 'Time required: {0:.2f} s'.format(end_time)
    
    
    
if __name__ == '__main__':
    # Map command line arguments to function arguments.
    get_instance_limits(*sys.argv[1:])