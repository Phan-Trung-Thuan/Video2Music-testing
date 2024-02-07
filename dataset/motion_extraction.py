from moviepy.editor import VideoFileClip
import os
from function import *

motion_feature_path = os.path.join(paths[7], f'{index}_motion.npy')
# If this video does not extract motion feature then extract it
if not os.path.exists(motion_feature_path):
    pass