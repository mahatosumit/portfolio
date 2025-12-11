import cv2
import numpy as np
import serial
import time
from gpiozero import DistanceSensor

# =====================================================
# SERIAL → Arduino
# =====================================================
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)

def send(cmd):
    ser.write((cmd + "\n").encode())
    print("[CMD]", cmd)


# =====================================================
# ULTRASONIC SENSORS
# =====================================================
front_left  = DistanceSensor(echo=27, trigger=17, max_distance=4)
front_right = DistanceSensor(echo=23, trigger=22, max_distance=4)
back        = DistanceSensor(echo=25, trigger=24, max_distance=4)

OBSTACLE = 25  # cm threshold


# =====================================================
# LOAD MobileNet SSD MODEL (VISION LOGIC)
# =====================================================
net = cv2.dnn.readNetFromCaffe(
    "deploy.prototxt",
    "MobileNetSSD_deploy.caffemodel"
)

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]


# =====================================================
# FIXED CAMERA INITIALIZATION FOR PI3 + BOOKWORM
# =====================================================
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# MUST SET LOWER RESOLUTION (otherwise Pi3 will fail allocation)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

time.sleep(2)  # camera warmup

if not cap.isOpened():
    print("ERROR: Camera failed to open. Exiting.")
    exit()


# =====================================================
# MOVEMENT TUNING
# =====================================================
FORWARD_SPEED = 150
STRAFE_SPEED  = 140
TURN_SPEED    = 140

STRAFE_TIME = 0.60
TURN_TIME   = 0.70
BACKUP_TIME = 0.50


# =====================================================
# AUTO-RECOVERY FUNCTION
# =====================================================
def auto_recover():
    print("AUTO-RECOVERY TRIGGERED")

    send("<STOP>")
    time.sleep(0.2)

    send(f"<MOVE|B|{FORWARD_SPEED}>")
    time.sleep(BACKUP_TIME)
    send("<STOP>")
    time.sleep(0.2)

    send(f"<MOVE|CW|{TURN_SPEED}>")
    time.sleep(TURN_TIME)
    send("<STOP>")
    time.sleep(0.2)


# =====================================================
# MAIN LOOP (VISION + ULTRASONIC)
# =====================================================
while True:

    # ----------- ULTRASONIC VALUES -----------
    fl = front_left.distance * 100
    fr = front_right.distance * 100
    bk = back.distance * 100

    print(f"FL:{fl:.1f}  FR:{fr:.1f}  BK:{bk:.1f}")

    # ----------- CAMERA FRAME -----------
    ret, frame = cap.read()

    if not ret:
        print("WARN: Camera frame read failed")
        time.sleep(0.1)
        continue

    # ----------- PERSON DETECTION -----------
    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)),
        0.007843, (300, 300), 127.5
    )
    net.setInput(blob)
    detections = net.forward()

    person_detected = False

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.50:
            idx = int(detections[0, 0, i, 1])
            label = CLASSES[idx]

            if label == "person":
                person_detected = True

                box = detections[0, 0, i, 3:7] * np.array(
                    [frame.shape[1], frame.shape[0],
                     frame.shape[1], frame.shape[0]]
                )
                (x1, y1, x2, y2) = box.astype("int")

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "PERSON", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 2)

    # ----------- SAFETY: PERSON STOP -----------
    if person_detected:
        print("PERSON DETECTED → STOP")
        send("<STOP>")
        time.sleep(3)
        continue


    # ----------- ULTRASONIC OBSTACLE AVOIDANCE -----------

    # Front completely blocked → stuck
    if fl < OBSTACLE and fr < OBSTACLE:
        print("FRONT BLOCKED → AUTO RECOVERY")
        auto_recover()
        continue

    # Left wall → strafe right
    if fl < OBSTACLE:
        print("LEFT BLOCK → STRAFE RIGHT")
        send(f"<MOVE|R|{STRAFE_SPEED}>")
        time.sleep(STRAFE_TIME)
        send("<STOP>")
        continue

    # Right wall → strafe left
    if fr < OBSTACLE:
        print("RIGHT BLOCK → STRAFE LEFT")
        send(f"<MOVE|L|{STRAFE_SPEED}>")
        time.sleep(STRAFE_TIME)
        send("<STOP>")
        continue

    # Back obstacle
    if bk < OBSTACLE:
        print("BACK BLOCKED → HOLD")
        send("<STOP>")
        continue

    # ----------- DEFAULT MOVEMENT: FORWARD -----------
    print("CLEAR PATH → MOVE FORWARD")
    send(f"<MOVE|F|{FORWARD_SPEED}>")

    # ----------- OPTIONAL PREVIEW -----------
    cv2.imshow("Rover Navigation Preview", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.1)
