import cv2
from ultralytics import YOLO
from serial_link import RoverSerial

# ================= SERIAL =================
rover = RoverSerial("/dev/ttyACM0")

# ================= YOLO =================
model = YOLO("yolov8n.pt")

# ================= CAMERA (USB via GStreamer) =================
gst = (
    "v4l2src device=/dev/video8 ! "
    "video/x-raw,width=640,height=480,framerate=30/1 ! "
    "videoconvert ! appsink drop=true"
)

cap = cv2.VideoCapture(gst, cv2.CAP_GSTREAMER)
if not cap.isOpened():
    raise RuntimeError("Camera not opened")

# ================= MAIN LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        rover.send("STOP")
        continue

    results = model(frame, imgsz=640, conf=0.5, verbose=False)

    cmd = "FWD"

    for box in results[0].boxes:
        cls = int(box.cls[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cx = (x1 + x2) // 2

        # person / vehicle avoidance
        if cls in [0, 2, 3]:
            if cx < 213:
                cmd = "RIGHT"
            elif cx > 426:
                cmd = "LEFT"
            else:
                cmd = "STOP"

    rover.send(cmd)

    cv2.imshow("Rover Vision", results[0].plot())
    if cv2.waitKey(1) & 0xFF == 27:
        break

rover.close()
cap.release()
cv2.destroyAllWindows()
