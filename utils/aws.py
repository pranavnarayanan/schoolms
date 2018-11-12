import boto.s3
import boto3
from boto.s3.connection import S3Connection, Bucket, Key
from botocore.errorfactory import ClientError

#Configuration can be removed if using boto3 (credentials will be stored via cmd)
AWS_ACCESS_KEY_ID = "AKIAIRWJP4ZDTHVK7PJQ"
AWS_SECRET_ACCESS_KEY = "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"
END_POINT = 'ap-south-1'
S3_HOST = 's3-ap-south-1.amazonaws.com'
BUCKET_NAME = 'myshishya'
FILENAME = 'D:/aws/img2.jpg' 
UPLOADED_FILENAME = 'ehan.png' # how file name should be created in s3

def upload():
    s3 = boto.s3.connect_to_region(END_POINT,aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY,host=S3_HOST)
    bucket = s3.get_bucket(BUCKET_NAME)
    k = Key(bucket)
    k.key = UPLOADED_FILENAME
    k.set_contents_from_filename(FILENAME)

def upload_using_boto3():
    s3 = boto3.client('s3')
    s3.upload_file(FILENAME, BUCKET_NAME, UPLOADED_FILENAME)

def download_using_boto3():
    s3 = boto3.resource('s3')
    s3.Bucket(BUCKET_NAME).download_file(UPLOADED_FILENAME, "D:/aws/dwnld2.jpg")

def download():
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3.download_file(BUCKET_NAME, UPLOADED_FILENAME, 'D:/aws/dwnld.jpg')

def delete():
    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, host=S3_HOST)
    bucket = Bucket(conn, BUCKET_NAME)
    k = Key(bucket=bucket, name=UPLOADED_FILENAME)
    k.delete()

def checkFileExists():
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        s3.head_object(Bucket=BUCKET_NAME, Key=UPLOADED_FILENAME)
        print("File Exists")
    except ClientError:
        print("File Not Found")

checkFileExists()
#upload()
#upload_using_boto3()
#download_using_boto3()
#download()
#delete()