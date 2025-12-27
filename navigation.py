import cv2
import numpy as np

# --- CONFIGURATION SWITCH ---
# Set to TRUE if you are testing on your White Floor with Black Tape.
# Set to FALSE when you are on the actual BFMC Track (Dark Floor, White Lines).
TEST_MODE_BLACK_TAPE = True 
# ----------------------------

class LaneDetector:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        
        # --- APPROXIMATE CALIBRATION (Adjust these later) ---
        # A trapezoid that usually works for 20cm camera height
        # Order: Bottom-Left, Top-Left, Top-Right, Bottom-Right
        self.src_points = np.float32([
            [0, height],           # Bottom-Left
            [220, 280],            # Top-Left (Horizon line approx)
            [420, 280],            # Top-Right
            [width, height]        # Bottom-Right
        ])
        
        self.dst_points = np.float32([
            [0, height],           # Bottom-Left
            [0, 0],                # Top-Left
            [width, 0],            # Top-Right
            [width, height]        # Bottom-Right
        ])
        
        self.M = cv2.getPerspectiveTransform(self.src_points, self.dst_points)
        self.Minv = cv2.getPerspectiveTransform(self.dst_points, self.src_points)

    def preprocess(self, frame):
        """
        Handles both Test Mode (Black Tape) and Competition Mode (White Lines).
        Switch is controlled by 'TEST_MODE_BLACK_TAPE' at the top.
        """
        # 1. Convert to HLS
        hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

        if TEST_MODE_BLACK_TAPE:
            # --- MODE: BLACK TAPE ON WHITE FLOOR ---
            # We want to detect DARK pixels.
            # L: 0-80 (Darkness). If your room is bright, you might need 0-100.
            lower = np.array([0, 0, 0])
            upper = np.array([180, 80, 255])
        else:
            # --- MODE: WHITE LINES ON DARK FLOOR (BFMC) ---
            # We want to detect BRIGHT pixels.
            # L: 150-255 (Brightness).
            lower = np.array([0, 150, 0])
            upper = np.array([255, 255, 255])

        # Create binary mask
        mask = cv2.inRange(hls, lower, upper)

        # Remove noise (small dots)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        return mask

    def warp(self, img):
        """Applies Bird's Eye View Transform"""
        return cv2.warpPerspective(img, self.M, (self.width, self.height))

    def get_lane_center(self, binary_warped):
        """
        THE SLIDING WINDOW ALGORITHM
        Finds the center of the lane using a Histogram.
        """
        # 1. Take a histogram of the bottom half of the image
        # This sums up the white pixels in each column.
        histogram = np.sum(binary_warped[binary_warped.shape[0]//2:, :], axis=0)
        
        # 2. Find the peak of the left and right halves
        midpoint = int(histogram.shape[0] / 2)
        
        left_base = np.argmax(histogram[:midpoint])
        right_base = np.argmax(histogram[midpoint:]) + midpoint
        
        # Check if peaks are strong enough (avoid noise)
        left_detected = histogram[left_base] > 1000
        right_detected = histogram[right_base] > 1000
        
        lane_center = self.width // 2  # Default to straight if nothing found
        
        # LOGIC:
        # If we see BOTH lines -> Drive in the middle
        # If we see ONLY LEFT -> Drive right of it
        # If we see ONLY RIGHT -> Drive left of it
        
        OFFSET = 250 # Pixels from lane line to car center (Tune this!)

        if left_detected and right_detected:
            lane_center = int((left_base + right_base) / 2)
        elif left_detected:
            lane_center = left_base + OFFSET 
        elif right_detected:
            lane_center = right_base - OFFSET
            
        # Error = How far is the lane center from the image center?
        # range: -320 (Left) to +320 (Right)
        error = lane_center - (self.width // 2)
        
        # Normalize to -1.0 to 1.0 for the PID controller
        normalized_error = error / (self.width // 2)
        
        return normalized_error, lane_center, histogram
