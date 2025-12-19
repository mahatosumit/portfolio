import cv2
import time
import serial
import numpy as np

# ==============================================================================
# CONFIGURATION & TUNING PARAMETERS
# ==============================================================================

# Hardware Settings
SERIAL_PORT = '/dev/ttyACM0'  # Verify if using /dev/ttyUSB0 or /dev/ttyAMA0
BAUD_RATE = 115200
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Speed Control (PWM Values)
SPEED_NORMAL = 150       # Standard cruising speed
SPEED_SLOW = 100         # For curves or caution zones
SPEED_STOP = 0           # Complete stop

# Steering Control (P-Controller)
MAX_STEER_ANGLE = 250    # Servo limit (-250 to 250)
KP = 0.8                 # Proportional Gain (Sensitivity)
CENTER_IMAGE_X = CAMERA_WIDTH // 2

# Traffic Rule Logic
MIN_SIGN_SIZE_RATIO = 0.20  # Sign must cover 20% of screen height to be valid
STOP_WAIT_TIME = 3.0        # Seconds to wait at a stop sign

# ==============================================================================
# 1. DRIVER INTERFACE (HARDWARE ABSTRACTION)
# ==============================================================================

class STM32Controller:
    def __init__(self, port, baud):
        self.ser = None
        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            time.sleep(2) # Allow handshake time
            print("[HARDWARE] Connected to STM32 Microcontroller.")
        except Exception as e:
            print(f"[ERROR] Serial Connection Failed: {e}")

    def send_command(self, speed, steer):
        if self.ser is None:
            return

        # Clamp values for safety
        steer = max(-MAX_STEER_ANGLE, min(MAX_STEER_ANGLE, int(steer)))
        speed = int(speed)

        # Format strictly: #steer:value;;#speed:value;;
        command = f"#steer:{steer};;#speed:{speed};;\r\n"
        try:
            self.ser.write(command.encode('utf-8'))
        except Exception as e:
            print(f"[ERROR] Serial Write Failed: {e}")

    def emergency_stop(self):
        self.send_command(0, 0)
        if self.ser:
            try:
                self.ser.write(b"#brake:1;;\r\n")
            except:
                pass

# ==============================================================================
# 2. TRAFFIC BRAIN (STATE MACHINE)
# ==============================================================================

class TrafficBrain:
    def __init__(self):
        # States: WAITING_START, DRIVING, STOPPING, INTERSECTION_COOLDOWN
        self.state = "WAITING_START"
        self.timer_start = 0
        self.last_sign_time = 0

    def process_rules(self, frame_height, detected_sign_label, sign_height):
        """
        Decides the target speed based on traffic rules and current state.
        Returns: (target_speed, status_message)
        """
        
        # Calculate sign relevance (how close is it?)
        sign_ratio = 0
        if sign_height > 0:
            sign_ratio = sign_height / frame_height

        # STATE 1: WAITING FOR START SIGNAL
        if self.state == "WAITING_START":
            # If we see a START sign close enough, begin mission
            if detected_sign_label == "START" and sign_ratio > 0.1:
                self.state = "DRIVING"
                return SPEED_NORMAL, "STATUS: MISSION STARTED"
            
            return 0, "STATUS: WAITING FOR SIGNAL"

        # STATE 2: STOPPING AT INTERSECTION
        elif self.state == "STOPPING":
            elapsed_time = time.time() - self.timer_start
            if elapsed_time >= STOP_WAIT_TIME:
                self.state = "INTERSECTION_COOLDOWN"
                self.timer_start = time.time()
                return SPEED_NORMAL, "STATUS: RESUMING MOTION"
            else:
                remaining = int(STOP_WAIT_TIME - elapsed_time) + 1
                return 0, f"STATUS: STOPPED ({remaining}s)"

        # STATE 3: COOLDOWN (Ignoring signs just after an intersection)
        elif self.state == "INTERSECTION_COOLDOWN":
            # Drive blindly for 4 seconds to clear the intersection so we don't stop twice
            if time.time() - self.timer_start > 4.0:
                self.state = "DRIVING"
            return SPEED_NORMAL, "STATUS: CLEARING INTERSECTION"

        # STATE 4: NORMAL DRIVING
        elif self.state == "DRIVING":
            # Check for signs only if they are close enough (Relevant)
            if sign_ratio > MIN_SIGN_SIZE_RATIO:
                
                if detected_sign_label == "STOP":
                    self.state = "STOPPING"
                    self.timer_start = time.time()
                    return 0, "STATUS: STOP SIGN DETECTED"
                
                elif detected_sign_label == "SLOW":
                    return SPEED_SLOW, "STATUS: CAUTION ZONE"
                
                elif detected_sign_label == "LIMIT_50":
                    return SPEED_SLOW, "STATUS: SPEED LIMIT 50"

            return SPEED_NORMAL, "STATUS: AUTOPILOT ACTIVE"

        return 0, "STATUS: UNKNOWN STATE"

# ==============================================================================
# 3. VISION SYSTEM (PERCEPTION)
# ==============================================================================

class PerceptionSystem:
    def __init__(self):
        # Initialize NCNN or Models here
        print("[VISION] System Initialized.")

    def detect_signs(self, frame):
        """
        REPLACE THIS with your actual Object Detection Model (YOLO/NanoDet).
        Currently uses Color Thresholding for testing without a model.
        Returns: (label_string, box_height_pixels)
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # 1. Detect STOP (Red)
        # Range for red is tricky because it wraps around 0-180
        mask1 = cv2.inRange(hsv, np.array([0, 70, 50]), np.array([10, 255, 255]))
        mask2 = cv2.inRange(hsv, np.array([170, 70, 50]), np.array([180, 255, 255]))
        mask_red = mask1 | mask2
        
        contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            # Filter noise
            if h > 40: 
                return "STOP", h

        # 2. Detect START (Green)
        mask_green = cv2.inRange(hsv, np.array([40, 40, 40]), np.array([80, 255, 255]))
        contours_g, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours_g:
            x, y, w, h = cv2.boundingRect(c)
            if h > 40:
                return "START", h

        return None, 0

    def detect_lane_center(self, frame):
        """
        REPLACE THIS with your Lane Segmentation Model (NCNN).
        Currently uses a simple brightness centroid for testing.
        Returns: x_coordinate (int) or None
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Focus on the bottom half of the image
        roi = gray[int(CAMERA_HEIGHT/2):, :]
        
        # Threshold to find white lines
        _, thresh = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY)
        
        # Find center of white pixels
        M = cv2.moments(thresh)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            return cx
        
        return None

# ==============================================================================
# 4. MAIN EXECUTION LOOP
# ==============================================================================

def main():
    # Initialize Modules
    car = STM32Controller(SERIAL_PORT, BAUD_RATE)
    brain = TrafficBrain()
    eyes = PerceptionSystem()

    # Initialize Camera (GStreamer for Pi 5)
    pipeline = (
        "libcamerasrc ! "
        "video/x-raw, width=(int)640, height=(int)480, framerate=(fraction)30/1 ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
    )
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("[ERROR] Could not open camera.")
        return

    print("---------------------------------------")
    print(" SYSTEM READY. SHOW 'START' SIGNAL. ")
    print("---------------------------------------")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Camera frame dropped.")
                break

            # --- STEP 1: PERCEPTION ---
            sign_label, sign_height = eyes.detect_signs(frame)
            lane_center_x = eyes.detect_lane_center(frame)

            # --- STEP 2: DECISION MAKING (SPEED) ---
            target_speed, status_text = brain.process_rules(CAMERA_HEIGHT, sign_label, sign_height)

            # --- STEP 3: CONTROL (STEERING) ---
            steer_command = 0
            
            # Only calculate steering if we are moving or about to move
            if lane_center_x is not None:
                # Calculate Error: How far is the lane from the center of the image?
                error = lane_center_x - CENTER_IMAGE_X
                
                # P-Controller
                steer_command = error * KP
            
            # If stopped, force steering to zero to prevent servo jitter
            if target_speed == 0:
                steer_command = 0

            # --- STEP 4: ACTUATION ---
            car.send_command(target_speed, steer_command)

            # --- VISUALIZATION (For Debugging) ---
            # Draw Lane Center
            if lane_center_x:
                cv2.circle(frame, (lane_center_x, CAMERA_HEIGHT-50), 10, (255, 0, 0), -1)
            
            # Draw Status Text
            cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # Draw Steering Bar
            cv2.line(frame, (CENTER_IMAGE_X, CAMERA_HEIGHT-20), (CENTER_IMAGE_X + int(steer_command), CAMERA_HEIGHT-20), (0, 0, 255), 5)

            cv2.imshow("BFMC Autonomous View", frame)

            # Exit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\n[USER] Manual Interruption.")

    finally:
        print("[SYSTEM] Shutting down...")
        car.emergency_stop()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
