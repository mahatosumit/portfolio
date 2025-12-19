import cv2
import time
import serial
import numpy as np
from ultralytics import YOLO
from camera import BFMCamera  # Imports your FIXED camera class

# ================= CONFIGURATION =================
SERIAL_PORT = '/dev/ttyACM0' 
BAUD_RATE = 115200

# Speed Constants
SPEED_NORMAL = 150
SPEED_CAUTION = 80
SPEED_STOP = 0

# Steering Constants
MAX_STEER = 250
KP = 0.4
STEER_DEADZONE = 10

# Traffic Rules
SIGN_TRIGGER_HEIGHT = 50   # Sign must be this tall (pixels) to react
STOP_WAIT_TIME = 3.0       # Time to wait at Stop sign
INTERSECTION_COOLDOWN = 5.0

CONTROL_DT = 0.05          # 20Hz Control Loop

# ================= STM32 CONTROLLER =================
class STM32Controller:
    def __init__(self, port, baud):
        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            time.sleep(2)
            print("✔ STM32 Connected")
        except:
            print("❌ STM32 Connection Failed. Check USB/Pins.")
            self.ser = None

    def send(self, speed, steer):
        if self.ser is None: return
        steer = int(max(-MAX_STEER, min(MAX_STEER, steer)))
        speed = int(speed)
        # BFMC Protocol: #steer:val;;#speed:val;;
        cmd = f"#steer:{steer};;#speed:{speed};;\r\n"
        self.ser.write(cmd.encode())

    def stop(self):
        self.send(0, 0)

# ================= VISION SYSTEM =================
class VisionSystem:
    def __init__(self, model_path="best_ncnn_model"):
        print(f"Loading AI Model: {model_path}...")
        # Load YOLO model (supports .pt or _ncnn_model folder)
        self.model = YOLO(model_path, task="detect")
        
        # MAP YOUR CLASS IDs HERE (Check your data.yaml!)
        self.class_map = {
            0: "STOP",
            1: "CROSSWALK",
            2: "PRIORITY",
            3: "PARKING",
            4: "ROUNDABOUT", 
            5: "ONEWAY"
        }

    def detect_sign(self, frame):
        # Run inference on the frame
        results = self.model(frame, imgsz=320, conf=0.4, verbose=False)
        
        best_label = None
        max_h = 0
        
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                h = int(y2 - y1)
                cls_id = int(box.cls[0])
                
                if h > SIGN_TRIGGER_HEIGHT:
                    # Found a close sign
                    label = self.class_map.get(cls_id, "UNKNOWN")
                    if h > max_h:
                        max_h = h
                        best_label = label
        
        return best_label

    def detect_lane(self, frame):
        # Simple grayscale centroid logic for lane following
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape
        roi = gray[int(height * 0.75):, :] # Bottom 25%
        _, thresh = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY)
        M = cv2.moments(thresh)
        
        if M["m00"] > 0:
            return int(M["m10"] / M["m00"]) # Center X
        return None

# ================= MAIN AUTONOMOUS LOOP =================
def main():
    # 1. Initialize Hardware
    car = STM32Controller(SERIAL_PORT, BAUD_RATE)
    vision = VisionSystem("best_ncnn_model") # Or "best.pt"
    
    # 2. Initialize Camera (Uses your fixed camera.py)
    cam = BFMCamera()
    cam.open()

    # 3. State Variables
    state = "DRIVING" # Start immediately for testing
    state_timer = 0
    last_time = time.time()
    frame_count = 0
    
    print("--- BFMC AUTONOMOUS PILOT ENGAGED ---")

    try:
        while True:
            # A. Read Frame
            frame = cam.read()
            if frame is None:
                print("⚠ Frame dropped")
                continue
            
            frame_count += 1
            height, width, _ = frame.shape

            # B. AI Detection (Every 3rd frame to save CPU)
            sign = None
            if frame_count % 3 == 0:
                sign = vision.detect_sign(frame)
                if sign: print(f"👀 SIGN SEEN: {sign}")

            # C. State Machine Logic
            current_speed = SPEED_NORMAL
            
            if state == "DRIVING":
                if sign == "STOP":
                    state = "STOPPING"
                    state_timer = time.time()
                    print("🛑 STOPPING")
                elif sign == "CROSSWALK" or sign == "ROUNDABOUT":
                    current_speed = SPEED_CAUTION
            
            elif state == "STOPPING":
                current_speed = 0
                if time.time() - state_timer > STOP_WAIT_TIME:
                    state = "COOLDOWN"
                    state_timer = time.time()
                    print("✅ RESUMING")
            
            elif state == "COOLDOWN":
                # Ignore signs for a few seconds after an intersection
                current_speed = SPEED_NORMAL
                if time.time() - state_timer > INTERSECTION_COOLDOWN:
                    state = "DRIVING"

            # D. Lane Following (Steering)
            lane_x = vision.detect_lane(frame)
            steer_cmd = 0
            
            if lane_x is not None:
                # P-Control
                error = (lane_x - (width // 2)) / (width // 2)
                steer_cmd = KP * error * MAX_STEER
                
                # Visuals
                cv2.circle(frame, (lane_x, height-50), 10, (0, 255, 0), -1)

            # E. Execute Control
            car.send(current_speed, steer_cmd)

            # F. Debug Display
            cv2.putText(frame, f"STATE: {state}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("BFMC Pilot", frame)
            
            if cv2.waitKey(1) == 27: # ESC to quit
                break
            
            # loop timing
            elapsed = time.time() - last_time
            if elapsed < CONTROL_DT: time.sleep(CONTROL_DT - elapsed)
            last_time = time.time()

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        car.stop()
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
