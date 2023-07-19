import os
import json
from PIL import Image
import matchering as mg
import base64

metadata = []

if os.path.isfile("metadata.json") == False:
    print("no metadata.json file")
    exit(0)

if os.path.isfile("config.json") == False:
    print("no config.json file")
    exit(0)

# Read metadata for generating NFTs
with open('metadata.json') as metadata_file:
    metadata = json.load(metadata_file)

# Read visual_orders from config.json
with open('config.json') as config_file:
    config_data = json.load(config_file)
    visual_orders = config_data["visual_orders"]
    base_uri = config_data["baseURI"]

# Get an asset location
def getAssetLocation(trait, value, extension, wall = True):
    subpath = "Audio/"
    if extension != "wav":
        subpath = "Visual/" + str(visual_orders[trait]) + ". "
    if wall == True:
        return "'./Asset/" + subpath + trait + "/" + value + "." + extension + "'"
    return "./Asset/" + subpath + trait + "/" + value + "." + extension

# Get an NFT result location
def getNFTLocation(title, extension, wall = True):
    if wall == True:
        return "'./NFT/" + title + "." + extension + "'"
    return "./NFT/" + title + "." + extension
#
def generateNFTs():
    for i in range(len(metadata)):
        attributes = metadata[i]["attributes"]
        index = metadata[i]["name"].split("#")[1]
        # wav
        if len(attributes["wav"]) != 0:
            shell = "ffmpeg -y"
            for attr in attributes["wav"]:
                shell += " -i " + getAssetLocation(attr["trait_type"], attr["value"], "wav")
            shell += " -filter_complex amix=inputs=" + str(len(attributes["wav"])) + ":duration=first:dropout_transition=0,alimiter=level_out=2 "+ getNFTLocation(index + "_master", "wav")
            os.system(shell)
        # matchering
        mg.process(
            target=getNFTLocation(index + "_master", "wav", False),
            reference="reference.wav",
            results=[mg.pcm24(getNFTLocation(index, "wav", False))],
        )
        # png
        cut = 0
        length = len(attributes["png"])
        for cut in range(length):
            if visual_orders[attributes["png"][cut]["trait_type"]] > 6:
                break
        png_1 = attributes["png"][0:cut]
        png_2 = attributes["png"][cut:length]
        #png_1
        background = Image.open(getAssetLocation(png_1[0]["trait_type"], png_1[0]["value"], "png", False), 'r')
        for attr in png_1:
            img = Image.open(getAssetLocation(attr["trait_type"], attr["value"], "png", False), 'r')
            background = Image.alpha_composite(background, img)
        background.save(getNFTLocation(index + "_1", "png", False))
        #png_2
        background = Image.open(getAssetLocation(png_2[0]["trait_type"], png_2[0]["value"], "png", False), 'r')
        for attr in png_2:
            img = Image.open(getAssetLocation(attr["trait_type"], attr["value"], "png", False), 'r')
            background = Image.alpha_composite(background, img)
        background.save(getNFTLocation(index + "_2", "png", False))
        #
        if len(attributes["mp4"]) != 0:
            filemp4 = attributes["mp4"][0]
            # Overlay png_1 with mp4
            os.system("ffmpeg -y -i "
                        + getAssetLocation(filemp4["trait_type"], filemp4["value"], "mp4")
                        + " -i "
                        + getNFTLocation(index + "_1", "png")
                        + " -filter_complex '[0][1]overlay[v]' -map '[v]' -c:v libx264 -preset ultrafast -qp 0 "
                        + getNFTLocation(index + "_mp4_png", "mp4"))
            if len(attributes["mov"]) != 0:
                filemov = attributes["mov"][0]
                os.system("ffmpeg -y -i "
                    + getNFTLocation(index + "_mp4_png", "mp4")
                    + " -i " + getAssetLocation(filemov["trait_type"], filemov["value"], "mov")
                    + " -filter_complex '[1:v]setpts=PTS-STARTPTS+0/TB[ovr];[0:v][ovr]overlay=enable=gte(t\,0):eof_action=pass,format=yuv420p[vid]' -map '[vid]' -c:v libx264 -preset ultrafast -qp 0 "
                    + getNFTLocation(index + "_mp4_mov", "mp4"))
                # Overlay png_2 with mp4
                os.system("ffmpeg -y -i "
                    + getNFTLocation(index + "_mp4_mov", "mp4")
                    + " -i "
                    + getNFTLocation(index + "_2", "png")
                    + " -filter_complex '[0][1]overlay[v]' -map '[v]' -c:v libx264 -preset ultrafast -qp 0 "
                    + getNFTLocation(index + "_mp4_png_final", "mp4"))
                # Overlay alpha with mp4
                if len(attributes["mov"]) == 2:
                    filemov = attributes["mov"][1]
                    os.system("ffmpeg -y -i "
                        + getNFTLocation(index + "_mp4_png_final", "mp4")
                        + " -i " + getAssetLocation(filemov["trait_type"], filemov["value"], "mov")
                        + " -filter_complex '[1:v]setpts=PTS-STARTPTS+0/TB[ovr];[0:v][ovr]overlay=enable=gte(t\,0):eof_action=pass,format=yuv420p[vid]' -map '[vid]' -c:v libx264 -preset ultrafast -qp 0 "
                        + getNFTLocation(index + "_mp4_png_final_alpha", "mp4"))
                    # Merge mp4 with wav 
                    os.system("ffmpeg -y -i "
                            + getNFTLocation(index + "_mp4_png_final_alpha", "mp4")
                            +" -i "
                            + getNFTLocation(index, "wav")
                            + " -c:v libx264 -c:a aac -b:a 320k -movflags +faststart "
                            + getNFTLocation(index + "_mp4_wav", "mp4"))
                else:
                    # Merge mp4 with wav 
                    os.system("ffmpeg -y -i "
                            + getNFTLocation(index + "_mp4_png_final", "mp4")
                            +" -i "
                            + getNFTLocation(index, "wav")
                            + " -c:v libx264 -c:a aac -b:a 320k -movflags +faststart "
                            + getNFTLocation(index + "_mp4_wav", "mp4"))
                os.system("mv " + getNFTLocation(index + "_mp4_wav", "mp4") + " " + getNFTLocation(index + "_mp4", "mp4"))
                os.system("mv " + getNFTLocation(index + "_mp4", "mp4") + " " + getNFTLocation(index, "mp4"))
                # remove _mp4 & _mp4_mov & _mp4_wav
                os.system("rm -f " + getNFTLocation(index + "_1", "png"))
                os.system("rm -f " + getNFTLocation(index + "_2", "png"))
                os.system("rm -f " + getNFTLocation(index + "_mp4_mov", "mp4"))
                os.system("rm -f " + getNFTLocation(index + "_mp4_wav", "mp4"))
                os.system("rm -f " + getNFTLocation(index + "_mp4_png", "mp4"))
                os.system("rm -f " + getNFTLocation(index + "_mp4_png_final", "mp4"))
                if len(attributes["mov"]) == 2:
                    os.system("rm -f " + getNFTLocation(index + "_mp4_png_final_alpha", "mp4"))
            else:
                # remove _mp4_mov & rename _mp4_wav
                os.system("mv " + getNFTLocation(index + "_mp4_wav", "mp4") + " " + getNFTLocation(index, "mp4"))
                os.system("rm -f " + getNFTLocation(index + "_mp4_mov", "mp4"))
        else:
            # merge png & wav
            os.system("ffmpeg -y -loop 1 -i "
                        + getNFTLocation(index, "png")
                        + " -i "
                        + getNFTLocation(index, "wav")
                        + " -c:v libx264 -tune stillimage -c:a aac -b:a 320k -pix_fmt yuv420p -shortest "
                        + getNFTLocation(index + "_png_wav", "mp4"))
            # cut video by duration
            os.system("ffmpeg -ss 00:00:00 -to 00:01:00 -i "
                        + getNFTLocation(index + "_png_wav", "mp4")
                        + " -c copy "
                        + getNFTLocation(index, "mp4"))
            os.system("rm -f " + getNFTLocation(index + "_png_wav", "mp4"))
        # remove png & wav
        os.system("rm -f " + getNFTLocation(index, "png"))

        os.system("rm -f " + getNFTLocation(index, "wav"))
        # Do not remove Master WAV, we may need it, instead lets move it to index.wav
        os.system("mv " + getNFTLocation(index + "_master","wav") + " " + getNFTLocation(index, "wav"))
        # os.system("rm -f " + getNFTLocation(index + "_master", "wav"))
        
        # extract an image from video
        os.system("ffmpeg -i " + getNFTLocation(index, "mp4") + " -ss 00:00:00 -vframes 1 " + getNFTLocation(index, "png"))
        # generate metadata json
        temp_json = metadata[i]
        temp_json["image"] = base_uri + index + ".png"
        temp_json["animation_url"] = base_uri + index + ".mp4"
        temp_json["dna"] = ""

        temp_png = []
        tattoos_large= ""
        tattoos_small= ""
        alpha_animations= ""
        for attr in temp_json["attributes"]["png"]:
            if attr["trait_type"] == "Tattoos Large":
                tattoos_large = attr["value"]
            elif attr["trait_type"] == "Tattoos Small":
                tattoos_small = attr["value"]
            elif attr["trait_type"] in ["Under Nails", "Under Nails Normal", "Alpha Animations", "Over Stickers", "Under Hands", "Windows", "Details", "Tape Colors", "Nails", "Cassette Stickers", "Rings"]:
                # includes
                no = 0
            else:
                temp_png.append(attr)
            temp_json["dna"] += attr["trait_type"] + ":" + attr["value"] + ","

        temp_png.append({
            "trait_type": "Tattoos",
            "value": tattoos_large + " + " + tattoos_small
        })

        temp_mov = []
        for attr in temp_json["attributes"]["mov"]:
            if attr["trait_type"] == "Alpha Animations":
                alpha_animations = attr["value"]
            elif attr["trait_type"] != "Gears":
                temp_mov.append(attr)
            temp_json["dna"] += attr["trait_type"] + ":" + attr["value"] + ","
        temp_mov.append({
            "trait_type": "The Drip",
            "value": alpha_animations
        })
                    
        for attr in temp_json["attributes"]["wav"]:
            temp_json["dna"] += attr["trait_type"] + ":" + attr["value"] + ","

        for attr in temp_json["attributes"]["mp4"]:
            temp_json["dna"] += attr["trait_type"] + ":" + attr["value"] + ","

        temp_json["attributes"] = [
            *temp_png,
            *temp_json["attributes"]["wav"],
            *temp_mov
        ]

        temp_json["dna"] = (temp_json["dna"][0:(len(temp_json["dna"]) - 1)]).encode("ascii")
        temp_json["dna"] = (base64.b64encode(temp_json["dna"])).decode("ascii")

        with open(getNFTLocation(index, "json", False), 'w') as outfile:
            json.dump(temp_json, outfile, indent=4)

generateNFTs()
