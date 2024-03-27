import os
from function import *

def main():
    video_dir_path = './dataset/video'
    audio_feature_dir_path = './dataset/audio'

    # If the directory is not exist then create it
    if not os.path.exists(audio_feature_dir_path):
        os.makedirs(audio_feature_dir_path)

    idList = get_id_list(idlist_path='./dataset/vevo_meta/idlist.txt')

    # Extract note density feature for each video downloaded
    for index, _ in idList:
        video_file_path = os.path.join(video_dir_path, f'{index}.mp4')
        audio_file_path = os.path.join(audio_feature_dir_path, f'{index}.wav')

        # If the video is downloaded and have not extract audio then extract it
        if os.path.exists(video_file_path) and not os.path.exists(audio_file_path):
            # NOTIFICATION
            print(f'Processing video {video_file_path}')

            # NOTIFICATION
            print(f'Extracting audio from video {video_file_path}')

            # Extract and save audio from video
            _, audio_object = get_video_audio(video_file_path)
            audio_object.write_audiofile(audio_file_path, 44100, 2, 2000,"pcm_s32le")

            # NOTIFICAITON
            print(f'Finish extract motion feature and saved into {audio_file_path} from video {video_file_path}', end=' ')

if __name__ == '__main__':
    main()