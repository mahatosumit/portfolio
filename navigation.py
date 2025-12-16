echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc


source ~/.bashrc

pyenv --version

pyenv install 3.11.9

cd ~/rover
pyenv local 3.11.9


python --version

python -m venv rover_env
source rover_env/bin/activate

python --version

pip install --upgrade pip setuptools wheel
pip install ultralytics opencv-python numpy pillow
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

python - <<EOF
import cv2, torch
print("Python OK")
print("OpenCV:", cv2.__version__)
print("Torch:", torch.__version__)
EOF

python - <<EOF
import cv2, torch
from ultralytics import YOLO

print("OpenCV:", cv2.__version__)
print("Torch:", torch.__version__)

model = YOLO("yolov8n.pt")
print("YOLO model loaded")
EOF



python - <<EOF
import cv2
cap = cv2.VideoCapture(0)
print("Camera opened:", cap.isOpened())
ret, frame = cap.read()
print("Frame:", ret, frame.shape if ret else None)
cap.release()
EOF
