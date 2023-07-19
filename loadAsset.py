import boto3
from botocore.client import Config
from pathlib import Path

ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
BUCKET_NAME = 'soundmint-curated-assets'

# Make folders

Visuals = ["Background Color", "Under Nails", "Under Nails Normal", "Under Hands", "Tape Colors", "Gears", "Cassette", "Windows", "Details", "Cassette Stickers", "Stickers", "Over Stickers", "Hands", "Nails", "Tattoos Large", "Tattoos Small", "Rings", "Alpha Animations"]
Audios = ["Bass + Chords", "Drums", "Percussion", "Vox"]

Path("Asset").mkdir(parents=True, exist_ok=True)
Path("Asset/Visual").mkdir(parents=True, exist_ok=True)
Path("Asset/Audio").mkdir(parents=True, exist_ok=True)

for i in range(1, len(Visuals) + 1):
    Path("Asset/Visual/" + str(i) + ". " + Visuals[i - 1]).mkdir(parents=True, exist_ok=True)
    
for audio in Audios:
    Path("Asset/Audio/" + audio).mkdir(parents=True, exist_ok=True)

Path("NFT").mkdir(parents=True, exist_ok=True)

# S3 Connect
s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)

listObjSummary = s3.Bucket(BUCKET_NAME).objects.all()
assets = []
for objSum in listObjSummary:
    assets.append(objSum.key)

length = len(assets)

for i in range(1, length + 1):
    s3.Bucket(BUCKET_NAME).download_file(assets[i - 1], "./Asset/" + assets[i - 1]);
    print("(" + str(i) + "/" + str(length)+")", assets[i - 1])
    
