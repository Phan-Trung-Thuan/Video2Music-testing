'''
================================================================================================
This function is used to download Youtube video from video's id
Parameter:
    video_id: id of Youtube video
    save_path: path to save the video (default is current directory)
    new_filename: name of the downloaded video (default is the name that Youtube provide)
Return: None
'''
import os
from pytube import YouTube

def download_youtube_video(video_id, save_path=None, new_filename=None):
    try:
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()

        # Get current path if save path is not provided
        if not save_path:
            save_path = os.getcwd()

        # Download the video
        download_path = stream.download(output_path=save_path)
        print(f'Download {video_url} completed')
        
        # Rename if a new filename is provided
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


'''
================================================================================================
This function is used get the frame list of the video each time step
Parameter:
    video_filename: video file name to get the frame (include path)
    step: the time (second) step to get the frame (default is 1 second)
Return: Generator of frames
'''
import cv2

def get_frame_list(video_filepath, step=1):
    # Open the video file
    cap = cv2.VideoCapture(video_filepath)

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_count = 0

    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        
        # Check if the frame was read successfully
        if not ret:
            break

        frame_count += 1
        
        # Check if it's time to save the frame (e.g., every second)
        if frame_count % int(fps * step) == 0:
            yield frame
            
    # Release the video capture object
    cap.release()
'''
Example usage:
    video_path = './001.mp4'
    frames = get_frame_list(video_path, step=0.5)
    for frame in frames:
        cv2.imshow(frame)
================================================================================================
'''