import os
import boto3
from ConfigParser import SafeConfigParser

# Create SQS client
path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'config.ini'
parser = SafeConfigParser()
parser.read(path)
AWSID = parser.get('aws_connection', 'access_key')
AWSKEY = parser.get('aws_connection', 'secret_key')
REGIONNAME = parser.get('sqs_connection', 'region_name')
QUEUEURL = parser.get('sqs_connection', 'queue_url')
FILENAME = parser.get('file', 'file_path')
sqs = boto3.resource('sqs', aws_access_key_id=AWSID,
                     aws_secret_access_key=AWSKEY,
                     region_name=REGIONNAME
                     )

queue_url = QUEUEURL

client = boto3.client('sqs', aws_access_key_id=AWSID,
                      aws_secret_access_key=AWSKEY,
                      region_name=REGIONNAME
                      )
response = client.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=[
        'ApproximateNumberOfMessages'
    ]
)

count = response.get('Attributes').get('ApproximateNumberOfMessages')

print count

for i in range(1, int(count)+1):
    message = client.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=1
    )
    print '#############################################'
    print 'Message number :' + str(i) + ' :' + str(message)
    print '#############################################'
    with open(FILENAME, 'a') as file:
         file.write(str(message))
         file.write('\n')
         file.write('-------------------------EOM-------------------------')
         file.write('\n')

