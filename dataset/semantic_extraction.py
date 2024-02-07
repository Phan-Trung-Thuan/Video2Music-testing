from moviepy.editor import VideoFileClip
import torch
import clip
from PIL import Image
import numpy as np
import os
from function import *

video_dir_path = './dataset/video'
semantic_feature_dir_path = './dataset/vevo_semantic'

# If the directory is not exist then create it
if not os.path.exists(semantic_feature_dir_path):
    os.makedirs(semantic_feature_dir_path)

idList = get_id_list(idlist_path='./dataset/vevo_meta/idlist.txt')

# Load CLIP model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model, preprocess = clip.load('ViT-L/14', device=device)

# Extract semantic feature for each video downloaded
for index, _ in idList[:1]:
    video_file_path = os.path.join(video_dir_path, f'{index}.mp4')
    semantic_feature_file_path = os.path.join(semantic_feature_dir_path, f'{index}_semantic.npy')

    # If the video is downloaded and have not extract motion feature then extract it
    if os.path.exists(video_file_path) and not os.path.exists(semantic_feature_file_path):
        # Get video no sound
        video_no_sound, _ = get_video_audio(video_file_path)
        
        # Get frame list step by 1 second
        frames = get_frame_list(video_no_sound)
        num_frames = len(frames)

        semantic_values = np.zeros((num_frames, 768), dtype=np.float32)
        for i in range(num_frames):
            image = preprocess(Image.fromarray(frames[i])).unsqueeze(0).to(device)
            img_encode = model.encode_image(image)
            semantic_values[i] = img_encode.detach().numpy()

        # Save motion values
        np.save(semantic_feature_file_path, semantic_values)
