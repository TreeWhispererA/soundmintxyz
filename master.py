from distutils.log import error
import os
import json
from math import radians
from math import ceil, floor
from random import shuffle

metadata = []

errors = []

# Read config file
with open('config.json') as config_file:
    data = json.load(config_file)
    name = data['name']
    description = data['description']
    count = data['count']
    traits = data['traits']
    visual_orders = data["visual_orders"]
    extensions = data["extensions"]

def getAssetLocation(trait, value):
    subpath = "Audio/"
    if extensions[trait] != "wav":
        subpath = "Visual/" + str(visual_orders[trait]) + ". "
    return "./Asset/" + subpath + trait + "/" + value + "." + extensions[trait]

# Initilize metadata array
for i in range(count):
    metadata.append({
        "name": name + " #" + str(i),
        "description": description,
        "image": "",
        "animation_url": "",
        "attributes": [],
    })

# Make metadata for generating nfts

def makeMetadataForGeneratingNFTs():
    for trait in traits:
        trait_name = trait["name"]
        values = trait["values"]
        visual_order = visual_orders[trait["name"]]
        # Random Value Array for each trait_type with trait value weight
        # Each index describes each trait value
        # For example, (0, 0, 1, 1, 1, 2, .... , 2498, 2499, 2499, 2499)
        randomValues = []
        for i in range(len(values)):
            for j in range(int(values[i]["weight"])):
                randomValues.append(i)
        # Shuffle Random Values
        # For example, (5, 8, 9, 5, 2498, 1034, .... , 10)
        shuffle(randomValues)
        for i in range(len(values)):
            for j in range(len(randomValues)):
                # Find the correct trait value with index
                if randomValues[j] == i:
                    # Add trait attribute
                    metadata[j]["attributes"].append(
                        {
                            "trait_type": trait_name,
                            "value": values[i]["value"],
                            "extension": extensions[trait_name],
                            "visual_order": visual_order,
                        })
                    if os.path.isfile(getAssetLocation(trait_name, values[i]["value"])) == False and (getAssetLocation(trait_name, values[i]["value"]) in errors) == False:
                        errors.append(getAssetLocation(trait_name, values[i]["value"]))
        for i in range(len(values)):
            value = values[i]
            # Trait Value List for "Swappable 50% (opensea name)" 
            neighbour_half = value.get("half", [])
            # Trait Value List for "Always Attached With (No Opensea Trait Name)"
            neighbour_together = value.get("together", [])
            attributes_count = int(value["weight"])
            # Handle the "Swappable 50%" trait value list
            if len(neighbour_half) != 0:
                j = 0
                for k in range(len(randomValues)):
                    if randomValues[k] == i:
                        if j < ceil(attributes_count / 2):
                            metadata[k]["attributes"].append(
                                {
                                    "trait_type": neighbour_half[0]["name"],
                                    "value": neighbour_half[0]["value"],
                                    "extension": extensions[neighbour_half[0]["name"]],
                                    "visual_order": visual_orders[neighbour_half[0]["name"]],
                                })
                            if os.path.isfile(getAssetLocation(neighbour_half[0]["name"], neighbour_half[0]["value"])) == False and (getAssetLocation(neighbour_half[0]["name"], neighbour_half[0]["value"]) in errors) == False:
                    	        errors.append(getAssetLocation(neighbour_half[0]["name"], neighbour_half[0]["value"]))
                        else:
                            metadata[k]["attributes"].append(
                                {
                                    "trait_type": neighbour_half[1]["name"],
                                    "value": neighbour_half[1]["value"],
                                    "extension": extensions[neighbour_half[1]["name"]],
                                    "visual_order": visual_orders[neighbour_half[1]["name"]],
                                })
                            if os.path.isfile(getAssetLocation(neighbour_half[1]["name"], neighbour_half[1]["value"])) == False and (getAssetLocation(neighbour_half[0]["name"], neighbour_half[0]["value"]) in errors) == False:
                                errors.append(getAssetLocation(neighbour_half[0]["name"], neighbour_half[0]["value"]))
                        j += 1
            # Handle the "Always Attached With" trait value list
            elif len(neighbour_together) != 0:
                for j in range(len(neighbour_together)):
                    for k in range(len(randomValues)):
                        if randomValues[k] == i:
                            metadata[k]["attributes"].append(
                                {
                                    "trait_type": neighbour_together[j]["name"],
                                    "value": neighbour_together[j]["value"],
                                    "extension": extensions[neighbour_together[j]["name"]],
                                    "visual_order": visual_orders[neighbour_together[j]["name"]],
                                })
                            if os.path.isfile(getAssetLocation(neighbour_together[j]["name"], neighbour_together[j]["value"])) == False and (getAssetLocation(neighbour_together[j]["name"], neighbour_together[j]["value"]) in errors) == False:
                                errors.append(getAssetLocation(neighbour_together[j]["name"], neighbour_together[j]["value"]))

# arrage attributes by extension and visual order

def arrageAttrByExtensionAndVisualOrder():
    def sortByVisualOrder(e):
        return e["visual_order"]
    for i in range(count):
        # sort by visual order
        metadata[i]["attributes"].sort(key=sortByVisualOrder)
        # arrage by extension
        temp = {"png": [], "wav": [], "mp4": [], "mov": []}
        for j in range(len(metadata[i]["attributes"])):
            attribute = metadata[i]["attributes"][j]
            temp[attribute["extension"]].append({
                "trait_type": attribute["trait_type"],
                "value": attribute["value"]}
            )
        metadata[i]["attributes"] = temp

# save metadata for generating nfts to a json file

def saveMetadataForGeneratingNFTs():

    with open('master.json', 'w') as outfile:
        json.dump(metadata, outfile)


# show non-existed files

def showErrors():
    for error in errors:
        print(error)
        
# main

makeMetadataForGeneratingNFTs()
showErrors()
arrageAttrByExtensionAndVisualOrder()
saveMetadataForGeneratingNFTs()
