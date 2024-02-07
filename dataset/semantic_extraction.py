from moviepy.editor import VideoFileClip
import clip
from PIL import Image
import numpy as np
import os
from function import *

def main():
    video_dir_path = './dataset/video'
    semantic_feature_dir_path = './dataset/vevo_semantic'

    # If the directory is not exist then create it
    if not os.path.exists(semantic_feature_dir_path):
        os.makedirs(semantic_feature_dir_path)

    idList = get_id_list(idlist_path='./dataset/vevo_meta/idlist.txt')

    # Load CLIP model
    model, preprocess = clip.load('ViT-L/14', device=DEVICE)

    # Extract semantic feature for each video downloaded
    for index, _ in idList:
        video_file_path = os.path.join(video_dir_path, f'{index}.mp4')
        semantic_feature_file_path = os.path.join(semantic_feature_dir_path, f'{index}_semantic.npy')

        # If the video is downloaded and have not extract motion feature then extract it
        if os.path.exists(video_file_path) and not os.path.exists(semantic_feature_file_path):
            # NOTIFICATION
            print(f'Processing video {video_file_path}')

            # Get video no sound
            video_no_sound, _ = get_video_audio(video_file_path)
            
            # Get frame list step by 1 second
            frames = get_frame_list(video_no_sound)
            num_frames = len(frames)

            # NOTIFICATION
            print(f'Extracting semantic feature from video {video_file_path}')

            semantic_values = np.zeros((num_frames, 768), dtype=np.float32)
            for i in range(num_frames):
                # Preprocess image
                image = preprocess(Image.fromarray(frames[i])).unsqueeze(0).to(DEVICE)
                # Encode image
                img_encode = model.encode_image(image)
                semantic_values[i] = img_encode.detach().numpy()
            
            # NOTIFICAITON
            print(f'Finish extract semantic feature from video {video_file_path}', end=' ')

            # Save semantic values
            np.save(semantic_feature_file_path, semantic_values)
            
            # NOTIFICATION
            print(f'Saved into {semantic_feature_file_path}')

if __name__ == '__main__':
    main()