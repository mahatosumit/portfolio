import cv2
import time
import serial
import numpy as np
from ultralytics import YOLO  # Import the AI Library

# ================= CONFIGURATION =================
SERIAL_PORT = '/dev/ttyACM0' 
BAUD_RATE = 115200

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Speed Settings
SPEED_NORMAL = 150
SPEED_CAUTION = 80       # Speed for Crosswalks/Roundabouts
SPEED_STOP = 0

# Steering Settings
MAX_STEER = 250
KP = 0.4
STEER_DEADZONE = 10

# Traffic Rules
SIGN_TRIGGER_HEIGHT = 50    # Sign must be at least 50px tall to react
STOP_WAIT_TIME = 3.0        # Seconds to wait at Stop sign
INTERSECTION_COOLDOWN = 5.0 # Seconds to ignore signs after reacting

CONTROL_DT = 0.05
# =================================================

# ================= STM32 INTERFACE =================
class STM32Controller:
    def __init__(self, port, baud):
        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            time.sleep(2)
            print("STM32 connected")
        except:
            print("STM32 connection failed")
            self.ser = None

    def send(self, speed, steer):
        if self.ser is None: return
        steer = int(max(-MAX_STEER, min(MAX_STEER, steer)))
        speed = int(speed)
        cmd = f"#steer:{steer};;#speed:{speed};;\r\n"
        self.ser.write(cmd.encode())

    def stop(self):
        self.send(0, 0)
        if self.ser: self.ser.write(b"#brake:1;;\r\n")

# ================= AI SIGN DETECTOR (UPDATED) =================
class SignDetector:
    def __init__(self, model_path="best.pt"):
        print(f"Loading AI Model from {model_path}...")
        try:
            self.model = YOLO(model_path, task='detect')
            print("AI Model Loaded Successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

        # MAP YOUR DATASET CLASSES HERE
        # Check your 'data.yaml' from Roboflow to confirm these ID numbers!
        self.class_map = {
            0: "STOP",
            1: "CROSSWALK",  # Pedestrian
            2: "PRIORITY",
            3: "PARKING",
            4: "ROUNDABOUT",
            5: "ONEWAY"
        }

    def detect(self, frame):
        if self.model is None: return None

        # Run Inference
        results = self.model(frame, verbose=False, conf=0.4, imgsz=320)
        
        # Process Results
        best_label = None
        max_height = 0

        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Get Box Coordinates
                x1, y1, x2, y2 = box.xyxy[0]
                h = int(y2 - y1)
                cls_id = int(box.cls[0])
                
                # Check if it's big enough to be relevant
                if h > SIGN_TRIGGER_HEIGHT:
                    # Look up the name in our map
                    label_name = self.class_map.get(cls_id, "UNKNOWN")
                    
                    # Prioritize the biggest/closest sign
                    if h > max_height:
                        max_height = h
                        best_label = label_name

        return best_label

# ================= LANE DETECTOR =================
class LaneDetector:
    def get_lane_center(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        roi = gray[int(FRAME_HEIGHT * 0.75):, :]
        _, thresh = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY)
        M = cv2.moments(thresh)
        if M["m00"] > 0:
            return int(M["m10"] / M["m00"])
        return None

# ================= MAIN LOOP =================
def main():
    car = STM32Controller(SERIAL_PORT, BAUD_RATE)
    
    # 1. LOAD THE TRAINED MODEL
    # Ensure 'best.pt' is in the folder
    signs = SignDetector("best.pt") 
    lanes = LaneDetector()

    cap = cv2.VideoCapture(f"libcamerasrc ! video/x-raw, width={FRAME_WIDTH}, height={FRAME_HEIGHT}, framerate=30/1 ! videoconvert ! appsink", cv2.CAP_GSTREAMER)

    # Traffic States
    state = 'DRIVING'
    current_speed = SPEED_NORMAL
    state_timer = 0
    
    last_time = time.time()
    frame_count = 0

    print("SYSTEM READY: AI DRIVER ENGAGED")

    try:
        while True:
            ret, frame = cap.read()
            if not ret: break
            frame_count += 1

            # ---- 1. PERCEPTION (AI Check every 3 frames) ----
            # We skip frames to keep FPS high on the Pi
            detected_sign = None
            if frame_count % 3 == 0:
                detected_sign = signs.detect(frame)
                if detected_sign: print(f"AI SAW: {detected_sign}")

            # ---- 2. DECISION MAKING (TRAFFIC RULES) ----
            
            # NORMAL DRIVING
            if state == 'DRIVING':
                current_speed = SPEED_NORMAL
                
                if detected_sign == "STOP":
                    state = 'STOPPED'
                    state_timer = time.time()
                    print("STOPPING FOR SIGN")

                elif detected_sign == "CROSSWALK":
                    state = 'CAUTION_ZONE'
                    state_timer = time.time()
                    print("PEDESTRIAN CROSSING")

                elif detected_sign == "ROUNDABOUT":
                    current_speed = SPEED_CAUTION
                    print("ROUNDABOUT AHEAD")
            
            # STOP SIGN LOGIC
            elif state == 'STOPPED':
                current_speed = 0
                if time.time() - state_timer > STOP_WAIT_TIME:
                    state = 'COOLDOWN'
                    state_timer = time.time()
                    print("GOING")

            # CROSSWALK LOGIC
            elif state == 'CAUTION_ZONE':
                current_speed = SPEED_CAUTION
                # Drive slow for 3 seconds then resume
                if time.time() - state_timer > 3.0:
                    state = 'COOLDOWN'
                    state_timer = time.time()
                    print("CROSSING CLEARED")

            # COOLDOWN
            elif state == 'COOLDOWN':
                current_speed = SPEED_NORMAL
                if time.time() - state_timer > INTERSECTION_COOLDOWN:
                    state = 'DRIVING'

            # ---- 3. CONTROL ----
            lane_x = lanes.get_lane_center(frame)
            steer_cmd = 0

            if current_speed > 0 and lane_x is not None:
                error = (lane_x - (FRAME_WIDTH // 2)) / (FRAME_WIDTH // 2)
                steer_cmd = KP * error * MAX_STEER
                if abs(steer_cmd) < STEER_DEADZONE: steer_cmd = 0
            
            car.send(current_speed, steer_cmd)

            # ---- 4. DISPLAY ----
            cv2.putText(frame, f"MODE: {state}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            if detected_sign:
                 cv2.putText(frame, f"SIGN: {detected_sign}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.imshow("BFMC AI Driver", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'): break

            # Loop Timing
            elapsed = time.time() - last_time
            if elapsed < CONTROL_DT: time.sleep(CONTROL_DT - elapsed)
            last_time = time.time()

    except KeyboardInterrupt:
        pass
    finally:
        car.stop()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
