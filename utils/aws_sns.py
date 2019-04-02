
import boto3

# Create an SNS client
client = boto3.client(
    "sns",
    aws_access_key_id="AKIAVSQMCGUCAXZPZEGY",
    aws_secret_access_key="cRET2j8jn7CssqkccpvyArksvSswBElI5NsksgjK",
    region_name="us-east-1"
)

# Send your sms message.
client.publish(
    PhoneNumber="+9447020535",
    Message="Hey,\nSms Test. \n\nTeam Wokidz"
)