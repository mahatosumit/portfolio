import subprocess
import numpy as np
import onnxruntime as ort
import serial
import time

# ===== CONFIG =====
WIDTH, HEIGHT = 640, 480
FRAME_SIZE = WIDTH * HEIGHT * 3  # RGB24

# ===== SERIAL =====
ser = serial.Serial("/dev/ttyACM0", 115200, timeout=0.1)
time.sleep(2)

def send(cmd):
    ser.write((cmd + "\n").encode())

# ===== ONNX =====
session = ort.InferenceSession(
    "models/yolov8n.onnx",
    providers=["CPUExecutionProvider"]
)
input_name = session.get_inputs()[0].name

# ===== CAMERA PIPE =====
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

while True:
    raw = proc.stdout.read(FRAME_SIZE)
    if len(raw) != FRAME_SIZE:
        break

    frame = np.frombuffer(raw, dtype=np.uint8)
    frame = frame.reshape((HEIGHT, WIDTH, 3))

    # ===== YOLO PREPROCESS =====
    img = frame.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)

    outputs = session.run(None, {input_name: img})

    # ===== BASIC DECISION LOGIC =====
    detections = outputs[0]
    cmd_out = "STOP" if detections.shape[1] > 0 else "FWD"

    send(cmd_out)

proc.terminate()
ser.close()
