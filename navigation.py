# vision.py
import cv2
from picamera2 import Picamera2

class Vision:
    """
    Haar-based full-body detection + Picamera2 capture.
    """

    def __init__(self, width=640, height=480):
        # ----- Load Haar Cascade -----
        self.cascade_path = cv2.data.haarcascades + "haarcascade_fullbody.xml"
        self.detector = cv2.CascadeClassifier(self.cascade_path)
        if self.detector.empty():
            raise RuntimeError("Failed to load Haar cascade")

        # ----- Initialize Camera -----
        self.picam = Picamera2()
        config = self.picam.create_video_configuration(
            main={"format": "XRGB8888", "size": (width, height)}
        )
        self.picam.configure(config)
        self.picam.start()

        print("[Vision] Picamera2 initialized.")

    def capture(self):
        """
        Capture one frame from the Pi Camera.
        Returns a BGR frame usable by OpenCV.
        """
        frame = self.picam.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        return frame

    def detect(self, frame, scaleFactor=1.08, minNeighbors=4, minSize=(64, 64)):
        """
        Returns list of (x, y, w, h) detected humans.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bodies = self.detector.detectMultiScale(
            gray,
            scaleFactor=scaleFactor,
            minNeighbors=minNeighbors,
            minSize=minSize
        )
        return bodies

    def annotate(self, frame, bodies):
        """
        Draw bounding boxes on detected bodies.
        """
        for (x, y, w, h) in bodies:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 2)
            cv2.putText(frame, "Human", (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        return frame
