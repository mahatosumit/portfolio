python - <<EOF
import cv2

cap = cv2.VideoCapture("/dev/video8", cv2.CAP_V4L2)

# DO NOT set MJPG (unsupported)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Opened:", cap.isOpened())

for i in range(5):
    ret, frame = cap.read()
    print(i, ret, None if not ret else frame.shape)

cap.release()
EOF
