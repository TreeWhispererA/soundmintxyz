import csv
from distutils import extension
import json
import os

csvfile = open('traits.csv', 'r')
jsonfile = open('config.json', 'r+')
config = json.load(jsonfile)
extensions = config["extensions"]
visual_orders = config["visual_orders"]

fieldnames = ("audio type","audio index","audio trait","count","percentage","order","visual type","visual index","visual trait","old filename","half trait","half type","always order","always trait","always type","every","notes")
reader = csv.DictReader( csvfile, fieldnames)
rowIndex = 0
traitsDict = {}
traitsArray = []

def getAssetLocation(trait, value):
    subpath = "Audio/"
    if extensions[trait] != "wav":
        subpath = "Visual/" + str(visual_orders[trait]) + ". "
    return "./Asset/" + subpath + trait + "/" + value + "." + extensions[trait]

def percentageToNumber(percentage):
    return float(percentage.split('%')[0])

for row in reader:
    if rowIndex > 0:
        if len(row["audio type"]) > 0 and row["audio trait"] != "None (N/A)":
            type = row["audio type"].strip()
            trait = row["audio trait"].strip()
            if os.path.isfile(getAssetLocation(row["audio type"].strip(), row["audio trait"].strip())) == False:
                    print("No Exist: " + getAssetLocation(row["audio type"].strip(), row["audio trait"].strip()))
            tempByTraitType = traitsDict.get(type, [])
            if len(row["half type"]) > 0:
                tempByTraitType.append({
                    "value": trait,
                    "weight": row["count"],
                    "half": [
                        {
                            "name": row["visual type"].strip(),
                            "value": row["visual trait"].strip()
                        },
                        {
                            "name": row["half type"].strip(),
                            "value": row["half trait"].strip()
                        }
                    ]
                })
                if os.path.isfile(getAssetLocation(row["visual type"].strip(), row["visual trait"].strip())) == False:
                    print("No Exist: " + getAssetLocation(row["visual type"].strip(), row["visual trait"].strip()))
                if os.path.isfile(getAssetLocation(row["half type"].strip(), row["half trait"].strip())) == False:
                    print("No Exist: " + getAssetLocation(row["half type"].strip(), row["half trait"].strip()))
            elif len(row["always type"]) > 0:
                tempByTraitType.append({
                    "value": trait,
                    "weight": row["count"],
                    "together": [
                        {
                            "name": row["visual type"].strip(),
                            "value": row["visual trait"].strip()
                        },
                        {
                            "name": row["always type"].strip(),
                            "value": row["always trait"].strip()
                        }
                    ]
                })
                if os.path.isfile(getAssetLocation(row["visual type"].strip(), row["visual trait"].strip())) == False:
                    print("No Exist: " + getAssetLocation(row["visual type"].strip(), row["visual trait"].strip()))
                if os.path.isfile(getAssetLocation(row["always type"].strip(), row["always trait"].strip())) == False:
                    print("No Exist: " + getAssetLocation(row["always type"].strip(), row["always trait"].strip()))
            else:
                tempByTraitType.append({
                    "value": trait,
                    "weight": row["count"],
                    "together": [
                        {
                            "name": row["visual type"].strip(),
                            "value": row["visual trait"].strip()
                        }
                    ]
                })
                if os.path.isfile(getAssetLocation(row["visual type"].strip(), row["visual trait"].strip())) == False:
                    print("No Exist: " + getAssetLocation(row["visual type"].strip(), row["visual trait"].strip()))
            traitsDict[type] = tempByTraitType
        elif len(row["visual type"]) > 0 and row["visual trait"] != "None (N/A)":
            type = row["visual type"]
            trait = row["visual trait"]
            if os.path.isfile(getAssetLocation(row["visual type"].strip(), row["visual trait"].strip())) == False:
                    print("No Exist: " + getAssetLocation(row["visual type"].strip(), row["visual trait"].strip()))
            tempByTraitType = traitsDict.get(type, [])
            if len(row["always type"]) > 0:
                tempByTraitType.append({
                    "value": trait,
                    "weight": row["count"],
                    "together": [
                        {
                            "name": row["always type"].strip(),
                            "value": row["always trait"].strip()
                        }
                    ]
                })
                if os.path.isfile(getAssetLocation(row["always type"].strip(), row["always trait"].strip())) == False:
                    print("No Exist: " + getAssetLocation(row["always type"].strip(), row["always trait"].strip()))
            else:
                tempByTraitType.append({
                    "value": trait,
                    "weight": row["count"],
                })
            traitsDict[type] = tempByTraitType  
    rowIndex += 1

for key in traitsDict:
    traitsArray.append({
        "name": key,
        "values": traitsDict[key]
    })

config["traits"] = traitsArray
jsonfile.seek(0)
jsonfile.write(json.dumps(config, indent=4))
jsonfile.truncate()
