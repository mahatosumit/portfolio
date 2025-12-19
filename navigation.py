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
            print("✔ Model Loaded Successfully")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
        
        self.class_map = {
            0: "STOP", 1: "CROSSWALK", 2: "PRIORITY",
            3: "PARKING", 4: "ROUNDABOUT", 5: "ONEWAY"
        }

    def detect_sign(self, frame):
        if self.model is None: return None
        results = self.model(frame, imgsz=320, conf=0.4, verbose=False)
        best_label = None
        max_h = 0
        for r in results:
            for box in r.boxes:
                h = int(box.xyxy[0][3] - box.xyxy[0][1])
                if h > config.SIGN_TRIGGER_HEIGHT:
                    label = self.class_map.get(int(box.cls[0]), "UNKNOWN")
                    if h > max_h:
                        max_h = h
                        best_label = label
        return best_label

    def detect_lane(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape
        roi = gray[int(height * 0.75):, :] 
        _, thresh = cv2.threshold(roi, config.LANE_THRESHOLD, 255, cv2.THRESH_BINARY)
        M = cv2.moments(thresh)
        if M["m00"] > 0:
            return int(M["m10"] / M["m00"]) 
        return None

# ================= MAIN LOOP =================
def main():
    # 1. Hardware Init
    car = STM32Controller(config.SERIAL_PORT, config.BAUD_RATE)
    cam = BFMCamera()
    cam.open()
    
    # 2. AI Init
    vision = VisionSystem(config.MODEL_PATH)
    
    print("--- BFMC AUTONOMOUS PILOT ENGAGED ---")

    state = "DRIVING"
    state_timer = 0
    last_time = time.time()
    
    # Heartbeat Timer
    last_heartbeat = time.time()
    frame_count = 0

    try:
        while True:
            frame = cam.read()
            if frame is None: continue
            
            frame_count += 1
            height, width, _ = frame.shape

            # --- 1. HEARTBEAT SAFETY (Crucial Fix) ---
            # Send 'alive' signal every 1 second
            if time.time() - last_heartbeat > 1.0:
                car.send_heartbeat()
                last_heartbeat = time.time()
                # print("♥ Heartbeat Sent") 

            # --- 2. PERCEPTION ---
            sign = None
            if frame_count % 3 == 0:
                sign = vision.detect_sign(frame)
                if sign: print(f"👀 SIGN SEEN: {sign}")

            # --- 3. DECISION ---
            current_speed = config.SPEED_NORMAL
            
            if state == "DRIVING":
                if sign == "STOP":
                    state = "STOPPING"
                    state_timer = time.time()
                    print("🛑 STOPPING")
                elif sign == "CROSSWALK" or sign == "ROUNDABOUT":
                    current_speed = config.SPEED_CAUTION
            
            elif state == "STOPPING":
                current_speed = 0
                if time.time() - state_timer > config.STOP_WAIT_TIME:
                    state = "COOLDOWN"
                    state_timer = time.time()
                    print("✅ RESUMING")
            
            elif state == "COOLDOWN":
                current_speed = config.SPEED_NORMAL
                if time.time() - state_timer > config.INTERSECTION_COOLDOWN:
                    state = "DRIVING"

            # --- 4. CONTROL ---
            lane_x = vision.detect_lane(frame)
            steer_cmd = 0
            
            if lane_x is not None:
                error = (lane_x - (width // 2)) / (width // 2)
                steer_cmd = config.KP * error * config.MAX_STEER
                if abs(steer_cmd) < config.STEER_DEADZONE: steer_cmd = 0
                cv2.circle(frame, (lane_x, height-50), 10, (0, 255, 0), -1)

            # Debug: Force print speed command to terminal to verify
            # print(f"CMD -> Speed: {current_speed}, Steer: {int(steer_cmd)}")

            car.send(current_speed, steer_cmd)

            # --- 5. DISPLAY ---
            cv2.putText(frame, f"STATE: {state}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("BFMC Pilot", frame)
            
            if cv2.waitKey(1) == 27: break
            
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
