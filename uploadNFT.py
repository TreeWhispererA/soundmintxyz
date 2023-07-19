import boto3
from botocore.client import Config
from os import listdir
from os.path import isfile, join

ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
BUCKET_NAME = 'collections.soundmint.xyz'

# S3 Connect
s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)

# check NFT folder
files = [f for f in listdir("./NFT") if isfile(join("./NFT", f))]
length = len(files)

if length == 0:
    print("Error: No Files")
    exit()
elif length % 4 != 0:
    print("Error: Exist not right pair(4)")
else:
    for filename in files:
        s3.Bucket(BUCKET_NAME).upload_file(join("./NFT", filename), "shhunrevealed/BACKINTIME/" + filename)
        print("Upload: ", filename)

