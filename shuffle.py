import boto3
from botocore.client import Config
from os.path import join
from random import randrange

ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
BUCKET_NAME = ''
COUNT = 2500    
ROUND = 10

# S3 Connect
s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)
def exchange_object(index1, index2, extension):
    s3.Object(BUCKET_NAME,join("shhunrevealed", "BACKINTIME", index1 + "_temp" + "." + extension)).copy_from(CopySource=join(BUCKET_NAME, "shhunrevealed", "BACKINTIME", index1 + "." + extension))
    s3.Object(BUCKET_NAME,join("shhunrevealed", "BACKINTIME", index2 + "_temp" + "." + extension)).copy_from(CopySource=join(BUCKET_NAME, "shhunrevealed", "BACKINTIME", index2 + "." + extension))
    s3.Object(BUCKET_NAME,join("shhunrevealed", "BACKINTIME", index1 + "." + extension)).delete()
    s3.Object(BUCKET_NAME,join("shhunrevealed", "BACKINTIME", index2 + "." + extension)).delete()
    s3.Object(BUCKET_NAME,join("shhunrevealed", "BACKINTIME", index2 + "." + extension)).copy_from(CopySource=join(BUCKET_NAME, "shhunrevealed", "BACKINTIME", index1 + "_temp" + "." + extension))
    s3.Object(BUCKET_NAME,join("shhunrevealed", "BACKINTIME", index1 + "." + extension)).copy_from(CopySource=join(BUCKET_NAME, "shhunrevealed", "BACKINTIME", index2 + "_temp" + "." + extension))
    s3.Object(BUCKET_NAME,join("shhunrevealed", "BACKINTIME", index1 + "_temp" + "." + extension)).delete()
    s3.Object(BUCKET_NAME,join("shhunrevealed", "BACKINTIME", index2 + "_temp" + "." + extension)).delete()

i = 1
while i <= ROUND:
    index1 = randrange(COUNT)
    index2 = randrange(COUNT)
    if index1 != index2:
        for extension in ["png", "mp4", "wav", "json"]:
            exchange_object(str(index1), str(index2), extension)
        print("(", i, ")", "index1:", index1, "index2:", index2)
        i = i + 1
