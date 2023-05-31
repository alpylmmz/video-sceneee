from re import A
from typing import Iterable
from scenedetect import VideoManager, SceneManager, StatsManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images, write_scene_list_html
from scenedetect.video_splitter import split_video_ffmpeg
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import sys


# import cv2

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


root = Tk()
root.title('Videosplit')

# File_DIR set
root.filename = filedialog.askopenfilename(initialdir='./mp4', title='Src_path', filetypes=(
('all files', '*.*'), ('mov files', '*.mov'), ('mp4 files', '*.mp4')))
dir_path = filedialog.askdirectory(initialdir="/", title='Set Project to....')

folder_Thumbnail = "Thumbnail"
os.makedirs(str(dir_path) + "/" + "Thumbnail")
tm = (dir_path + "/" + "Thumbnail")

folder_Video = "Video"
os.makedirs(str(dir_path) + "/" + "Video")
vd = (dir_path + "/" + "Video")

folder_Data = "Data"
os.makedirs(str(dir_path) + "/" + "Data")
DT = (dir_path + "/" + "Data")

video_path = ([root.filename])
stats_path = 'result.csv'

video_manager = VideoManager([root.filename])
stats_manager = StatsManager()
scene_manager = SceneManager(stats_manager)
input_video_path = ([root.filename])

scene_manager.add_detector(ContentDetector(threshold=30))
video_manager.set_downscale_factor()

video_manager.start()
scene_manager.detect_scenes(frame_source=video_manager)

# results
with open(stats_path, 'w') as f:
    stats_manager.save_to_csv(f, video_manager.get_base_timecode())

scene_list = scene_manager.get_scene_list()
print(f'{len(scene_list)} Scenes Found!')

save_images(
    scene_list,
    video_manager,
    num_images=1,
    image_name_template='$FRAME_NUMBER',
    output_dir=str(tm))

split_video_ffmpeg(
    input_video_path,
    scene_list,
    output_file_template=str(vd + "/" + '$FRAME_NUMBER-$SCENE_NUMBER.mp4'),
    video_name=None,
    arg_override='-c:v libx264 -preset veryfast -crf 21 -c:a aac',
    hide_progress=False,
    suppress_output=False)

write_scene_list_html(f"{DT}/result.html", scene_list)
for scene in scene_list:
    start, end = scene

    # your code
    print(f'{start.get_seconds()} - {end.get_seconds()}')

