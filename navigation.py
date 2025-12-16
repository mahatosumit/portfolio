python - <<EOF
import cv2
for i in range(4):
    cap = cv2.VideoCapture(i)
    print(i, cap.isOpened())
    if cap.isOpened():
        ret, frame = cap.read()
        print("  frame:", ret, None if not ret else frame.shape)
    cap.release()
EOF
