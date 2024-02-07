from moviepy.editor import VideoFileClip
import os
from function import *

idList = get_id_list(idlist_path='./dataset/vevo_meta/idlist.txt')

video_download_path = './dataset/video'
         
# If the directory is not exist then create it
if not os.path.exists(video_download_path):
    os.makedirs(video_download_path)

# Extract feature for each VIDEO - AUDIO pair
for index, id in idList:
    video_path = os.path.join(video_download_path, f'{index}.mp4')

    # If the video is not downloaded then download it
    if not os.path.exists(video_path):
        download_youtube_video(id, video_download_path, f'{index}.mp4')

    video = VideoFileClip(video_path)
    video_no_sound = video.without_audio()
    audio = video.audio()