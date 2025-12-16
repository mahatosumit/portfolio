import subprocess
import numpy as np
import onnxruntime as ort
import serial
import time

# ================= CONFIG =================
CAM_W, CAM_H = 640, 480
MODEL_W, MODEL_H = 640, 640
FRAME_SIZE = CAM_W * CAM_H * 3  # RGB24

# ================= SERIAL =================
ser = serial.Serial("/dev/ttyACM0", 115200, timeout=0.1)
time.sleep(2)

def send(cmd):
    ser.write((cmd + "\n").encode())

# ================= LETTERBOX (NO OPENCV) =================
def letterbox(img, new_shape=(640, 640), color=114):
    h, w, _ = img.shape
    new_h, new_w = new_shape

    scale = min(new_w / w, new_h / h)
    rw, rh = int(w * scale), int(h * scale)

    # Resize (nearest neighbor, fast & acceptable here)
    resized = np.zeros((rh, rw, 3), dtype=np.uint8)
    for c in range(3):
        resized[:, :, c] = np.resize(img[:, :, c], (rh, rw))

    padded = np.full((new_h, new_w, 3), color, dtype=np.uint8)
    top = (new_h - rh) // 2
    left = (new_w - rw) // 2

    padded[top:top + rh, left:left + rw] = resized
    return padded, scale, top, left

# ================= ONNX =================
session = ort.InferenceSession(
    "models/yolov8n.onnx",
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
try:
    while True:
        raw = proc.stdout.read(FRAME_SIZE)
        if len(raw) != FRAME_SIZE:
            break

        frame = np.frombuffer(raw, dtype=np.uint8)
        frame = frame.reshape((CAM_H, CAM_W, 3))

        # ---- LETTERBOX TO 640x640 ----
        img640, scale, pad_top, pad_left = letterbox(frame)

        # ---- YOLO PREPROCESS ----
        img = img640.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))  # CHW
        img = np.expand_dims(img, axis=0)   # NCHW

        outputs = session.run(None, {input_name: img})

        # ---- BASIC DECISION LOGIC (PLACEHOLDER) ----
        detections = outputs[0]
        cmd_out = "STOP" if detections.shape[1] > 0 else "FWD"

        send(cmd_out)

finally:
    proc.terminate()
    ser.close()
