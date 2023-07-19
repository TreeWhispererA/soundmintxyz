import os
from PIL import Image

def main():

    for path, subdirs, files in os.walk("./Asset"):
        for i in range(len(files)):
            name = files[i]
            if name.find(".png") != -1:
                file = os.path.join(path, name)
                temp = os.path.join(path, str(i) + ".png")
                os.system("ffmpeg -y -i '" + file + "' -vf scale=2500:2500 '" + temp + "'")
                os.system("rm -f '" + file + "'")
                os.system("mv '" + temp + "' '" + file + "'")

# Check the image size as 2500* 2500
def check():

    result = True
    for path, subdirs, files in os.walk("./Asset"):
        for name in files:
            if name.find(".png") != -1:
                im = Image.open(os.path.join(path, name))
                width, height = im.size
                if width != 2500 or height != 2500:
                    result = False
                    break
    return result

main()

# print(check())
