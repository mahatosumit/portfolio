import sys
import os
import time
import cv2
import numpy as np
import threading
import serial
import math

# ==================================================
# ADD SRC TO PYTHON PATH
# ==================================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
sys.path.append(SRC_PATH)

# ==================================================
# IMPORTS
# ==================================================
from perception.camera import Camera
from perception.lane_detection import LaneDetector
# Phase 2: YOLO disabled to match report
# from perception.yolo_detector import YOLODetector 
from planning.fsm import FSM, State

# ==================================================
# CONFIG
# ==================================================
SERIAL_PORT = "/dev/ttyACM0"
# MODEL_PATH  = os.path.join(SRC_PATH, "models/best.pt") # Disabled for Phase 2

FRAME_W = 640
FRAME_H = 480

BASE_SPEED = 25.0
MIN_SPEED  = 18.0
MAX_STEER  = 25.0

# ==================================================
# SERIAL HANDLER
# ==================================================
class SerialHandler:
    def __init__(self, port):
        self.port = port
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, 115200, timeout=1)
            print(f"[Serial] Connected to {self.port}")
        except Exception as e:
            print(f"[Serial] Connection failed: {e}")

    def send_command(self, speed, steer):
        if self.ser and self.ser.is_open:
            cmd = f"#S:{speed:.2f};#T:{steer:.2f};;\r\n"
            self.ser.write(cmd.encode())

    def stop(self):
        self.send_command(0.0, 0.0)

# ==================================================
# SHARED STATE (THREAD SAFE)
# ==================================================
current_speed = 0.0
current_steer = 0.0
# current_sign_intensity = 0.0 # Disabled
system_running = True
# sign_lock = threading.Lock() # Disabled

# ==================================================
# THREAD: SERIAL HEARTBEAT
# ==================================================
def serial_heartbeat(stm32):
    global current_speed, current_steer, system_running
    while system_running:
        stm32.send_command(current_speed, current_steer)
        time.sleep(0.05)

# ==================================================
# THREAD: YOLO WORKER (DISABLED FOR PHASE 2)
# ==================================================
# def yolo_worker(detector, camera):
#     global current_sign_intensity, system_running
#
#     YOLO_INTERVAL = 0.25  # 4 Hz
#
#     while system_running:
#         start = time.time()
#
#         ok, frame, _ = camera.read()
#         if ok:
#             intensity = detector.detect_sign_intensity(frame)
#             with sign_lock:
#                 current_sign_intensity = intensity
#
#         elapsed = time.time() - start
#         if elapsed < YOLO_INTERVAL:
#             time.sleep(YOLO_INTERVAL - elapsed)

# ==================================================
# STEERING: COSINE LAW
# ==================================================
def cosine_steering(error):
    error = np.clip(error, -1.0, 1.0)
    steer = MAX_STEER * math.sin(error * math.pi / 2.0)
    return float(np.clip(steer, -MAX_STEER, MAX_STEER))

# ==================================================
# MAIN
# ==================================================
def main():
    global current_speed, current_steer, system_running

    cam = Camera(width=FRAME_W, height=FRAME_H, fps=60)
    lane_detector = LaneDetector(width=FRAME_W, height=FRAME_H)
    fsm = FSM()
    stm32 = SerialHandler(SERIAL_PORT)

    # YOLO init - DISABLED
    # yolo = YOLODetector(MODEL_PATH, FRAME_W, FRAME_H, device="cpu")

    cam.open()
    stm32.connect()
    time.sleep(1.0)

    # Threads
    threading.Thread(target=serial_heartbeat, args=(stm32,), daemon=True).start()
    
    # YOLO Thread - DISABLED
    # threading.Thread(target=yolo_worker, args=(yolo, cam), daemon=True).start()

    print("=== BFMC AUTONOMOUS MODE STARTED (PHASE 2) ===")

    try:
        while True:
            ok, frame, ts = cam.read()
            if not ok:
                continue

            # Lane perception
            binary = lane_detector.preprocess(frame)
            warped = lane_detector.warp(binary)
            error, _, lane_conf = lane_detector.compute_lane(warped)

            # Read YOLO signal - DISABLED (Force 0)
            # with sign_lock:
            #     sign_intensity = current_sign_intensity
            sign_intensity = 0.0

            # FSM
            state = fsm.update({
                "lane_confidence": lane_conf,
                "obstacle": False,
                "sign_intensity": sign_intensity
            })

            # Speed logic
            if state == State.LANE_FOLLOW:
                speed_cmd = BASE_SPEED
            elif state == State.CAUTION:
                speed_cmd = BASE_SPEED * 0.6
            elif state == State.BLIND:
                speed_cmd = BASE_SPEED * 0.3
            else:
                speed_cmd = 0.0

            if speed_cmd > 0:
                speed_cmd = max(speed_cmd, MIN_SPEED)

            steer_cmd = cosine_steering(error)

            current_speed = speed_cmd
            current_steer = steer_cmd

            # Debug Display
            if int(time.time() * 10) % 5 == 0:
                # Visualize on warped image to check lane fit
                dbg = cv2.cvtColor(warped, cv2.COLOR_GRAY2BGR)
                
                # HUD info
                cv2.putText(dbg, f"STATE: {state.name}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(dbg, f"LaneConf: {lane_conf:.2f}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(dbg, f"Steer: {steer_cmd:.1f}", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 100, 100), 2)
                
                cv2.imshow("BFMC View", dbg)

                if cv2.waitKey(1) == ord('q'):
                    break

    finally:
        system_running = False
        stm32.stop()
        time.sleep(0.1)
        if stm32.ser:
            stm32.ser.close()
        cam.release()
        cv2.destroyAllWindows()

# ==================================================
# ENTRY
# ==================================================
if __name__ == "__main__":
    main()
