pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

python - <<EOF
import serial
import cv2
from ultralytics import YOLO
import torch

print("pyserial OK")
print("OpenCV:", cv2.__version__)
print("YOLO OK")
print("Torch:", torch.__version__)
EOF
