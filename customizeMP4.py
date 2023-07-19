import os
import subprocess
import cv2

mp4_path = "./Asset/Visual/1. Background Color"

def get_length(input_video):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

def loop():
  for file in os.listdir(mp4_path):
    if file.endswith(".mov"):
        filepath = os.path.join(mp4_path, file)
        outpath = os.path.join(mp4_path, "_"+file)
        os.system("ffmpeg -stream_loop 1 -i '" + filepath + "' -c copy '" + outpath + "'")

# Check mp4 & loop 1 min
def checkMov():
  for file in os.listdir(mp4_path):
    if file.endswith(".mov"):
      filepath = os.path.join(mp4_path, file)
      print(file, get_length(filepath))

def checkMp4():
  for file in os.listdir(mp4_path):
    if file.endswith(".mp4"):
      filepath = os.path.join(mp4_path, file)
      vid = cv2.VideoCapture(filepath)
      height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
      width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
      if height != 2500 or width != 2500:
        print(file, width, height)
# loop()
# checkMov()
checkMp4()