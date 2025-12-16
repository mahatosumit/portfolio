import cv2

gst = (
    "v4l2src device=/dev/video8 ! "
    "videoconvert ! "
    "video/x-raw,width=640,height=480,framerate=30/1 ! "
    "appsink drop=true"
)

cap = cv2.VideoCapture(gst, cv2.CAP_GSTREAMER)
print("Opened:", cap.isOpened())

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Frame failed")
        break
    cv2.imshow("USB Cam", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

