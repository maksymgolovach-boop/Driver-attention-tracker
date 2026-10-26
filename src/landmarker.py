import mediapipe as mp
import os.path
from urllib.request import urlretrieve
from pathlib import Path

url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

res_dir = PROJECT_ROOT / "res"
model_path = res_dir / "face_landmarker.task"


if not os.path.exists(model_path):
    urlretrieve(url, model_path)


BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(str(model_path)),
    running_mode=VisionRunningMode.VIDEO,
    num_faces=10
)

landmarker = FaceLandmarker.create_from_options(options)