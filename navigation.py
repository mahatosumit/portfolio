import subprocess
import numpy as np
import onnxruntime as ort
import serial
import time
import signal
import sys

# ================= CONFIG =================
CAM_W, CAM_H = 640, 480
MODEL_W, MODEL_H = 640, 640
FRAME_SIZE = CAM_W * CAM_H * 3  # RGB24

SERIAL_PORT = "/dev/ttyACM0"
BAUDRATE = 115200

CONF_THRESH = 0.45
CMD_COOLDOWN = 0.15     # command rate limit
HEARTBEAT_INTERVAL = 0.3

# YOLO classes of interest (COCO)
# 0: person, 2: car, 3: motorcycle, 5: bus, 7: truck
VALID_CLASSES = {0, 2, 3, 5, 7}

# ================= SERIAL =================
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.1)
time.sleep(2)

last_cmd = None
last_cmd_time = 0
last_heartbeat = 0

def send(cmd):
    global last_cmd, last_cmd_time
    now = time.time()
    if cmd != last_cmd and (now - last_cmd_time) > CMD_COOLDOWN:
        ser.write((cmd + "\n").encode())
        last_cmd = cmd
        last_cmd_time = now

def heartbeat():
    global last_heartbeat
    now = time.time()
    if now - last_heartbeat > HEARTBEAT_INTERVAL:
        ser.write(b"PING\n")
        last_heartbeat = now

# ================= SAFE EXIT =================
def cleanup(sig=None, frame=None):
    try:
        ser.write(b"STOP\n")
    except:
        pass
    try:
        proc.terminate()
    except:
        pass
    try:
        ser.close()
    except:
        pass
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

# ================= LETTERBOX =================
def letterbox(img, new_shape=(640, 640), color=114):
    h, w, _ = img.shape
    new_h, new_w = new_shape

    scale = min(new_w / w, new_h / h)
    rw, rh = int(w * scale), int(h * scale)

    resized = np.zeros((rh, rw, 3), dtype=np.uint8)
    for c in range(3):
        resized[:, :, c] = np.resize(img[:, :, c], (rh, rw))

    padded = np.full((new_h, new_w, 3), color, dtype=np.uint8)
    top = (new_h - rh) // 2
    left = (new_w - rw) // 2
    padded[top:top + rh, left:left + rw] = resized

    return padded

# ================= ONNX =================
session = ort.InferenceSession(
    "yolov8n.onnx",
    providers=["CPUExecutionProvider"]
)
input_name = session.get_inputs()[0].name

# ================= CAMERA PIPE =================
cmd = [
    "ffmpeg",
    "-f", "v4l2",
    "-input_format", "yuyv422",
    "-video_size", "640x480",
    "-i", "/dev/video8",
    "-f", "rawvideo",
    "-pix_fmt", "rgb24",
    "-"
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)

# ================= MAIN LOOP =================
while True:
    raw = proc.stdout.read(FRAME_SIZE)
    if len(raw) != FRAME_SIZE:
        break

    heartbeat()  # ---- WATCHDOG HEARTBEAT ----

    frame = np.frombuffer(raw, dtype=np.uint8)
    frame = frame.reshape((CAM_H, CAM_W, 3))

    img640 = letterbox(frame)
    img = img640.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)

    outputs = session.run(None, {input_name: img})
    preds = outputs[0][0]   # shape: Nx6 or Nx7 depending on export

    cmd_out = "FWD"
    best_conf = 0
    best_x = None

    # ===== DECODE YOLO OUTPUT =====
    for det in preds:
        conf = det[4]
        if conf < CONF_THRESH:
            continue

        cls = int(det[5])
        if cls not in VALID_CLASSES:
            continue

        if conf > best_conf:
            best_conf = conf
            x_center = (det[0] + det[2]) / 2
            best_x = x_center

    # ===== DECISION LOGIC =====
    if best_x is not None:
        if best_x < MODEL_W * 0.4:
            cmd_out = "RIGHT"
        elif best_x > MODEL_W * 0.6:
            cmd_out = "LEFT"
        else:
            cmd_out = "STOP"
    else:
        cmd_out = "FWD"

    send(cmd_out)

cleanup()
