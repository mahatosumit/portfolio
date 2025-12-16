python - <<EOF
from picamera2 import Picamera2
import cv2
import time

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"}
))
picam2.start()

time.sleep(1)

frame = picam2.capture_array()
print(frame.shape)  # should be (480, 640, 3)

cv2.imshow("Frame", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

picam2.stop()
EOF
