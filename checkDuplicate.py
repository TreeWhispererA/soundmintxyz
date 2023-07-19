import os
import json

# Read metadata for generating NFTs
with open('metadata.json') as metadata_file:
    metadata = json.load(metadata_file)

for i in range(len(metadata) - 1):
    for j in range(i + 1, len(metadata)):
        iattributes = metadata[i]["attributes"]
        jattributes = metadata[j]["attributes"]

        ipngs = iattributes["png"]
        jpngs = jattributes["png"]
        isDiff = False
        if len(ipngs) == len(jpngs):
            for k in range(len(ipngs)):
                if ipngs[k]["trait_type"] != jpngs[k]["trait_type"] or ipngs[k]["value"] != jpngs[k]["value"]:
                    isDiff = True
                    break
        else:
            isDiff = True

        iwavs = iattributes["wav"]
        jwavs = jattributes["wav"]
        if isDiff == False and len(iwavs) == len(jwavs):
            for k in range(len(iwavs)):
                if iwavs[k]["trait_type"] != jwavs[k]["trait_type"] or iwavs[k]["value"] != jwavs[k]["value"]:
                    isDiff = True
                    break
        else:
            isDiff = True

        imp4s = iattributes["mp4"]
        jmp4s = jattributes["mp4"]
        if isDiff == False and len(imp4s) == len(jmp4s):
            for k in range(len(imp4s)):
                if imp4s[k]["trait_type"] != jmp4s[k]["trait_type"] or imp4s[k]["value"] != jmp4s[k]["value"]:
                    isDiff = True
                    break
        else:
            isDiff = True

        imovs = iattributes["mov"]
        jmovs = jattributes["mov"]
        if isDiff == False and len(imovs) == len(jmovs):
            for k in range(len(imovs)):
                if imovs[k]["trait_type"] != jmovs[k]["trait_type"] or imovs[k]["value"] != jmovs[k]["value"]:
                    isDiff = True
                    break
        else:
            isDiff = True
        
        if isDiff == False:
            print("Same NFTs exist: ", i, " ", j)
        