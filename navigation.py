import cv2
import time
import serial
import numpy as np

# --- CONFIGURATION ---
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 115200

# Speeds
SPEED_NORMAL = 150
SPEED_CAUTION = 100
SPEED_STOP = 0

# Thresholds (The "Automatic" Decision Factors)
# If a sign covers more than this % of the screen height, act on it.
# 0.25 means the sign is 1/4th the height of the image (very close).
TRIGGER_SIZE_RATIO = 0.25 

class STM32Controller:
    def __init__(self, port, baud):
        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            time.sleep(2)
            print("✔ STM32 Connected")
        except:
            print("❌ STM32 Connection Failed")
            self.ser = None

    def send(self, speed, steer):
        if self.ser is None: return
        cmd = f"#steer:{int(steer)};;#speed:{int(speed)};;\r\n"
        self.ser.write(cmd.encode('utf-8'))

class TrafficManager:
    def __init__(self):
        self.state = "WAITING_FOR_START" # Initial State
        self.stop_start_time = 0
        self.min_stop_duration = 3.0 # Seconds to wait at STOP sign

    def check_rules(self, frame, current_speed):
        """
        Input: Camera Frame
        Output: Adjusted Speed (int), Status Message (str)
        """
        h_img, w_img, _ = frame.shape
        
        # --- 1. DETECT SIGNS (Placeholder for your NCNN Model) ---
        # Replace this block with your actual sign detection inference
        # It must return: label (str), box_height (int)
        
        label, box_h = self.dummy_detection(frame) 
        # ---------------------------------------------------------

        # Calculate how "big" the sign is relative to the screen
        ratio = box_h / h_img 

        # --- STATE MACHINE ---
        
        # STATE 1: WAITING AT START LINE
        if self.state == "WAITING_FOR_START":
            if label == "START" and ratio > 0.1: # If we see start sign
                self.state = "DRIVING"
                return SPEED_NORMAL, "🚀 GO!"
            return 0, "⏳ WAITING FOR START..."

        # STATE 2: STOP SIGN HANDLING
        elif self.state == "STOPPED_AT_SIGN":
            elapsed = time.time() - self.stop_start_time
            if elapsed > self.min_stop_duration:
                self.state = "COOLDOWN" # Prevent stopping again immediately
                return SPEED_NORMAL, "✅ RESUMING"
            else:
                return 0, f"🛑 STOPPING ({int(3-elapsed)}s)"

        # STATE 3: COOLDOWN (Ignore signs for 2 seconds after stopping)
        elif self.state == "COOLDOWN":
            if time.time() - self.stop_start_time > (self.min_stop_duration + 5):
                self.state = "DRIVING"
            return current_speed, "💨 DRIVING (Cooldown)"

        # STATE 4: NORMAL DRIVING (Looking for signs)
        elif self.state == "DRIVING":
            # Only react if the sign is CLOSE (Big enough)
            if ratio > TRIGGER_SIZE_RATIO:
                if label == "STOP":
                    self.state = "STOPPED_AT_SIGN"
                    self.stop_start_time = time.time()
                    return 0, "🛑 STOP SIGN TRIGGERED"
                
                elif label == "SLOW":
                    return SPEED_CAUTION, "⚠ SLOW DOWN"
                
                elif label == "END":
                    return 0, "🏁 END OF TRACK"

            return current_speed, "🚗 AUTOPILOT"

        return 0, "ERROR"

    def dummy_detection(self, frame):
        """
        Temporary color-based detector for testing without AI.
        Returns: Label, Height
        """
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Detect RED (Stop Sign)
        mask_red = cv2.inRange(hsv, np.array([0, 120, 70]), np.array([10, 255, 255]))
        contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            _, _, _, h = cv2.boundingRect(c)
            if h > 50: return "STOP", h

        # Detect GREEN (Start Sign)
        mask_green = cv2.inRange(hsv, np.array([40, 40, 40]), np.array([70, 255, 255]))
        contours_g, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours_g:
            _, _, _, h = cv2.boundingRect(c)
            if h > 50: return "START", h
            
        return None, 0

# --- LANE DETECTION (Keep your NCNN logic here) ---
class LaneDetector:
    # ... (Paste your NCNN LaneDetector class from previous step here) ...
    def get_lane_center(self, frame):
        # Placeholder logic
        return 320 # Returns center for now

def main():
    car = STM32Controller(SERIAL_PORT, BAUD_RATE)
    traffic = TrafficManager()
    lanes = LaneDetector()
    
    # Init Camera
    cap = cv2.VideoCapture(0) # or GStreamer pipeline
    cap.set(3, 640)
    cap.set(4, 480)

    try:
        while True:
            ret, frame = cap.read()
            if not ret: break
            
            # 1. TRAFFIC LOGIC (Speed Control)
            # This function automatically decides the speed based on signs
            target_speed, status_msg = traffic.check_rules(frame, SPEED_NORMAL)
            
            # 2. LANE LOGIC (Steering Control)
            steer_cmd = 0
            if target_speed > 0: # Only steer if we are moving
                lane_x = lanes.get_lane_center(frame)
                if lane_x:
                    error = lane_x - 320
                    steer_cmd = 0.8 * error
            
            # 3. EXECUTE
            car.send(target_speed, steer_cmd)
            
            # Visuals
            cv2.putText(frame, status_msg, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("BFMC AI", frame)
            
            if cv2.waitKey(1) == ord('q'): break
            
    finally:
        car.send(0,0) # Safety stop
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
