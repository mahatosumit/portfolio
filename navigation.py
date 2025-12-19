import cv2
import time
import sys
import config  # Imports your settings

# Ensure we can import from local folders
sys.path.append('.')

from drivers.camera import BFMCamera
from drivers.motor import STM32Controller 
from ultralytics import YOLO

# ================= VISION SYSTEM =================
class VisionSystem:
    def __init__(self, model_path):
        print(f"Loading AI Model from: {model_path}...")
        try:
            self.model = YOLO(model_path, task="detect")
            print("Model Loaded Successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
        
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
        if self.model is None: return None

        # Use 320px for speed, 640px for accuracy
        results = self.model(frame, imgsz=320, conf=0.4, verbose=False)
        
        best_label = None
        max_h = 0
        
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                h = int(y2 - y1)
                cls_id = int(box.cls[0])
                
                if h > config.SIGN_TRIGGER_HEIGHT:
                    label = self.class_map.get(cls_id, "UNKNOWN")
                    if h > max_h:
                        max_h = h
                        best_label = label
        
        return best_label

    def detect_lane(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape
        
        # Look at the bottom 25% of the road
        roi = gray[int(height * 0.75):, :] 
        
        # Use threshold from config
        _, thresh = cv2.threshold(roi, config.LANE_THRESHOLD, 255, cv2.THRESH_BINARY)
        M = cv2.moments(thresh)
        
        if M["m00"] > 0:
            return int(M["m10"] / M["m00"]) # Returns Center X
        return None

# ================= MAIN LOOP =================
def main():
    # 1. Hardware Init
    car = STM32Controller(config.SERIAL_PORT, config.BAUD_RATE)
    cam = BFMCamera()
    
    # 2. AI Init
    vision = VisionSystem(config.MODEL_PATH)
    
    cam.open()
    print("--- BFMC AUTONOMOUS PILOT ENGAGED ---")

    # State Variables
    state = "DRIVING"
    state_timer = 0
    last_time = time.time()
    frame_count = 0

    try:
        while True:
            # A. Get Frame
            frame = cam.read()
            if frame is None: continue
            
            frame_count += 1
            height, width, _ = frame.shape

            # B. AI Detection (Run every 3rd frame to save CPU)
            sign = None
            if frame_count % 3 == 0:
                sign = vision.detect_sign(frame)
                if sign: print(f"SIGN SEEN: {sign}")

            # C. Driving Logic
            current_speed = config.SPEED_NORMAL
            
            if state == "DRIVING":
                if sign == "STOP":
                    state = "STOPPING"
                    state_timer = time.time()
                    print("STOPPING")
                elif sign == "CROSSWALK" or sign == "ROUNDABOUT":
                    current_speed = config.SPEED_CAUTION
            
            elif state == "STOPPING":
                current_speed = 0
                if time.time() - state_timer > config.STOP_WAIT_TIME:
                    state = "COOLDOWN"
                    state_timer = time.time()
                    print("RESUMING")
            
            elif state == "COOLDOWN":
                current_speed = config.SPEED_NORMAL
                if time.time() - state_timer > config.INTERSECTION_COOLDOWN:
                    state = "DRIVING"

            # D. Lane Following (P-Controller)
            lane_x = vision.detect_lane(frame)
            steer_cmd = 0
            
            if lane_x is not None:
                error = (lane_x - (width // 2)) / (width // 2)
                # Calculate steering using Config values
                steer_cmd = config.KP * error * config.MAX_STEER
                
                # Apply Deadzone
                if abs(steer_cmd) < config.STEER_DEADZONE:
                    steer_cmd = 0
                
                # Visual Debug
                cv2.circle(frame, (lane_x, height-50), 10, (0, 255, 0), -1)

            # E. Execute
            car.send(current_speed, steer_cmd)

            # F. Display
            cv2.putText(frame, f"STATE: {state}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("BFMC Pilot", frame)
            
            if cv2.waitKey(1) == 27: # ESC key
                break
            
            # Loop Timing (Keep consistent Hz)
            elapsed = time.time() - last_time
            if elapsed < config.CONTROL_DT:
                time.sleep(config.CONTROL_DT - elapsed)
            last_time = time.time()

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        car.stop()
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
