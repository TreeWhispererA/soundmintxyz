# 🌜 Soundmint Curated NFT Generator 🌛

## Environment

- Ubuntu
- Python 3.6 or higher

## Install Packages

```
sudo apt update
```

### install pip module

```
sudo apt install python3-pip

```

### install matchering module

```
sudo apt -y install libsndfile1
```

```
python3 -m pip install -U matchering
```

### install ffmpeg module

```
sudo apt -y install ffmpeg
```

### install PIL module

```
python3 -m pip install --upgrade Pillow
```

### install boto3 module for aws s3

```
python3 -m pip install -U boto3
```

## Structure

- **config.json**

  - name
  - description
  - baseURI
  - visual_orders
  - extensions
  - traits (It will be inserted when run makeTraitsOnConfig.py)

- **master.json**
  metadata file for 2500 NFTs
- **metadata.json**
  metadata file for generation
- **makeTraitsOnConfig.py**
  Extract data from csv and import to config.json
- **master.py**
  Generate metadata for 2500 NFTs
- **metadata.py**
  Input Format: start end
  Generate metadata
- **nft.py**
  Generate NFTs and metadata
- **resizePNG.py**
  Resize all PNG files to 2500 \* 2500
- **loadAsset.py**
  Create "Asset" and "NFT" folders & Download all assets from aws s3 bucket
- **NFT**
  Save all created NFTs in this folder
- **Asset**
  assets folder(wav, png, mp4, mov) for generation

## How to work

### First Step(run at only one time)

```
python3 makeTraitsOnConfig.py
```

```
python3 master.py
```

### Second Step

![png](https://github.com/CaCaBlocker/Gifs/blob/main/2022-04-28_20-55-43.png)

```
python3 metadata.py
```

```
python3 loadAsset.py
```

```
python3 nft.py
```
