'''
================================================================================================
This function is used to download Youtube video from video's id
Parameter:
    video_id: id of Youtube video
    save_path: path to save the video (default is current directory)
    new_filename: name of the downloaded video (default is the name that Youtube provide)
'''
import os
from pytube import YouTube

def download_youtube_video(video_id, save_path=None, new_filename=None):
    try:
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()

        if not save_path:
            save_path = os.getcwd()

        download_path = stream.download(output_path=save_path)
        print(f'Download {video_url} completed')
        
        # Rename the downloaded file if a new filename is provided
        if new_filename:
            new_file_path = os.path.join(save_path, new_filename)
            os.rename(download_path, new_file_path)

    except Exception as e:
        print(f'An error occurred: {e}, video url: {video_url}')
'''
Example usage:
    video_id = 'kJQP7kiw5Fk'
    save_path = '' # Save at current directory
    new_filename = '001.mp4'  # New filename of the downloaded video
    download_youtube_video(video_id, save_path, new_filename)
================================================================================================
'''