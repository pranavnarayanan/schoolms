from boto3.s3.transfer import S3Transfer
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = 'myshishya'
FILEPATH = 'D:/pics/a.jpg'
UPLOADED_FILENAME = 'bike.jpg' # how file name should be created in s3


client = boto3.client(
    's3',
    aws_access_key_id="AKIAVSQMCGUCAXZPZEGY",
    aws_secret_access_key="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",
    region_name="us-east-1"
)

##Upload
transfer = S3Transfer(client)
transfer.upload_file(FILEPATH, BUCKET_NAME, "marks/"+UPLOADED_FILENAME) #marks folder will be auto created

#Download
client.download_file(BUCKET_NAME,"marks/"+UPLOADED_FILENAME,'D:/k.jpg')

#delete
client.delete_object(Bucket=BUCKET_NAME, Key="marks/"+UPLOADED_FILENAME)

def checkFileExists():
    try:
        client.head_object(Bucket=BUCKET_NAME, Key=UPLOADED_FILENAME)
        print("File Exists")
    except ClientError:
        print("File Not Found")