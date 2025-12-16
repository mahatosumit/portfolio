python - <<EOF
import cv2
print("cv2 OK:", cv2.__version__)
print("GStreamer:", "YES" if "GStreamer:                   YES" in cv2.getBuildInformation() else "NO")
EOF


pip install --upgrade pip
pip install ultralytics pyserial numpy pillow
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
