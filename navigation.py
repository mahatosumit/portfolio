import cv2
import time
import serial
import numpy as np
# import ncnn # Uncomment when real model is ready

# --- CONFIGURATION ---
SERIAL_PORT = '/dev/ttyACM0'  # Check your port!
BAUD_RATE = 115200

# Camera
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Control Constants
NORMAL_SPEED = 150
SLOW_SPEED = 80
STOP_SPEED = 0
MAX_STEER = 250
KP = 0.8  # Steering sensitivity

# Sign Detection Thresholds (Pixels)
# How big must the sign be in the image to trigger a reaction?
SIGN_TRIGGER_HEIGHT = 80  # If sign is taller than 80px, we are "close"
STOP_DURATION = 3         # Seconds to wait at a stop sign

# ---------------------------------------------------------
# 1. HARDWARE INTERFACE (STM32)
# ---------------------------------------------------------
class STM32Controller:
    def __init__(self, port, baud):
        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            time.sleep(2)
            print(f"✔ Connected to STM32")
        except:
            print(f"❌ ERROR: STM32 Connection Failed")
            self.ser = None

    def send(self, speed, steer):
        if self.ser is None: return
        steer = max(-MAX_STEER, min(MAX_STEER, int(steer)))
        speed = int(speed)
        cmd = f"#steer:{steer};;#speed:{speed};;\r\n"
        self.ser.write(cmd.encode('utf-8'))

    def stop(self):
        self.send(0, 0)
        if self.ser: self.ser.write(b"#brake:1;;\r\n")

# ---------------------------------------------------------
# 2. PERCEPTION: TRAFFIC SIGNS
# ---------------------------------------------------------
class SignDetector:
    def __init__(self):
        # TODO: Load your Object Detection Model here (e.g., NanoDet / YOLO)
        # self.net = ncnn.Net()
        # self.net.load_param("signs.param")
        # self.net.load_model("signs.bin")
        print("✔ Sign Detector initialized")

    def detect(self, frame):
        """
        Returns: (label, box_height)
        label: "STOP", "SLOW", "LEFT", "RIGHT", "START"
        box_height: Height of the bounding box in pixels
        """
        
        # --- PLACEHOLDER LOGIC FOR TESTING ---
        # (This allows you to test the logic without a trained model yet)
        # Logic: If we see a LOT of RED color, assume STOP sign.
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Red Color Range (Stop Sign)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red1, upper_red1)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        best_label = None
        max_h = 0
        
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if h > max_h:
                max_h = h
                # Basic color-based guessing (Replace with AI model later!)
                if h > 30: best_label = "STOP" 

        # Return the biggest sign found
        if best_label and max_h > 0:
            return best_label, max_h
            
        return None, 0

# ---------------------------------------------------------
# 3. PERCEPTION: LANE FOLLOWING
# ---------------------------------------------------------
class LaneDetector:
    def __init__(self):
        # Load your Lane NCNN model here
        pass

    def get_lane_center(self, frame):
        # --- PASTE YOUR PREVIOUS NCNN LANE LOGIC HERE ---
        # For now, using simple image processing as placeholder
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        roi = gray[int(FRAME_HEIGHT*0.8):, :] 
        _, thresh = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY)
        M = cv2.moments(thresh)
        if M["m00"] > 0:
            return int(M["m10"] / M["m00"])
        return None

# ---------------------------------------------------------
# 4. MAIN AUTONOMOUS LOOP
# ---------------------------------------------------------
def main():
    car = STM32Controller(SERIAL_PORT, BAUD_RATE)
    signs = SignDetector()
    lanes = LaneDetector()
    
    # Camera Setup (GStreamer for Pi 5)
    pipeline = f"libcamerasrc ! video/x-raw, width={FRAME_WIDTH}, height={FRAME_HEIGHT}, framerate=30/1 ! videoconvert ! appsink"
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    # State Variables
    current_speed = NORMAL_SPEED
    stop_timer = 0
    is_stopped = False
    
    print("--- STARTING MISSION ---")

    try:
        while True:
            ret, frame = cap.read()
            if not ret: break

            # --- A. CHECK FOR SIGNS ---
            sign_label, sign_height = signs.detect(frame)
            
            # Logic: Only react if the sign is CLOSE (big enough)
            if sign_height > SIGN_TRIGGER_HEIGHT:
                cv2.rectangle(frame, (10,10), (200,50), (0,0,0), -1)
                cv2.putText(frame, f"SIGN: {sign_label}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
                
                if sign_label == "STOP":
                    if not is_stopped:
                        print("🛑 STOP SIGN DETECTED -> STOPPING")
                        current_speed = 0
                        is_stopped = True
                        stop_timer = time.time()
                
                elif sign_label == "SLOW":
                    current_speed = SLOW_SPEED
                    print("⚠ SLOW ZONE")

                elif sign_label == "START":
                    current_speed = NORMAL_SPEED
                    is_stopped = False # Force resume
                    print("🚀 START / RESUME")

            # --- B. HANDLE STOP TIMER ---
            if is_stopped:
                # Check if we waited long enough (e.g., 3 seconds)
                if time.time() - stop_timer > STOP_DURATION:
                    print("✅ STOP COMPLETE -> RESUMING")
                    is_stopped = False
                    current_speed = NORMAL_SPEED
                else:
                    # Force Stop
                    car.stop()
                    # Skip steering logic while stopped
                    cv2.imshow("BFMC Pilot", frame)
                    if cv2.waitKey(1) == ord('q'): break
                    continue 

            # --- C. LANE FOLLOWING (STEERING) ---
            lane_x = lanes.get_lane_center(frame)
            
            if lane_x is not None:
                error = lane_x - (FRAME_WIDTH // 2)
                steer_cmd = KP * error
                
                # Apply specific steering logic for turns if needed
                if sign_label == "LEFT" and sign_height > SIGN_TRIGGER_HEIGHT:
                     # Bias steering to the left to take the turn
                     steer_cmd -= 50 
                elif sign_label == "RIGHT" and sign_height > SIGN_TRIGGER_HEIGHT:
                     steer_cmd += 50

                car.send(current_speed, steer_cmd)
            else:
                car.send(0, 0) # Safety stop if no lane

            # Debug Display
            cv2.imshow("BFMC Pilot", frame)
            if cv2.waitKey(1) == ord('q'): break

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        car.stop()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
