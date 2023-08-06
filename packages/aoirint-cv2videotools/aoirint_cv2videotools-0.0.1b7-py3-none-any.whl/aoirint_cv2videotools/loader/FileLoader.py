import cv2 # type: ignore

from .VideoLoader import VideoLoader

class FileLoader(VideoLoader):
    def __init__(self, video_path):
        cap = cv2.VideoCapture(video_path)
        self.cap = cap
