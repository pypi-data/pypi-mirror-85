import cv2 # type: ignore

class VideoLoader:
    @property
    def framerate(self):
        return self.cap.get(cv2.CAP_PROP_FPS)

    @property
    def width(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def size(self):
        return self.width, self.height

    @property
    def framenum(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_COUNT)

    def release(self):
        self.cap.release()

    def iter(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            yield frame
