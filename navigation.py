import cv2
import numpy as np

def nothing(x):
    pass

# Initialize Camera
cap = cv2.VideoCapture(0) # Change to 0 or 1 depending on your camera index

# Create a Window for Trackbars
cv2.namedWindow("Tuning")
cv2.createTrackbar("Top Width", "Tuning", 100, 320, nothing)    # Top spread
cv2.createTrackbar("Bottom Width", "Tuning", 300, 320, nothing) # Bottom spread
cv2.createTrackbar("Height Top", "Tuning", 240, 480, nothing)   # How far up to look
cv2.createTrackbar("Height Bottom", "Tuning", 480, 480, nothing)# How close to look
cv2.createTrackbar("Threshold", "Tuning", 150, 255, nothing)    # Binary cutoff

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Resize for consistency (optional, helps with FPS)
    frame = cv2.resize(frame, (640, 480))
    h, w = frame.shape[:2]

    # 1. Get Values from Trackbars
    w_top = cv2.getTrackbarPos("Top Width", "Tuning")
    w_bot = cv2.getTrackbarPos("Bottom Width", "Tuning")
    h_top = cv2.getTrackbarPos("Height Top", "Tuning")
    h_bot = cv2.getTrackbarPos("Height Bottom", "Tuning")
    thresh_val = cv2.getTrackbarPos("Threshold", "Tuning")

    # 2. Define Source Points (The Trapezoid)
    # We assume the camera is centered, so we calculate offsets from the center (w // 2)
    center_x = w // 2
    
    # Top Left, Top Right, Bottom Left, Bottom Right
    tl = (center_x - w_top, h_top)
    tr = (center_x + w_top, h_top)
    bl = (center_x - w_bot, h_bot)
    br = (center_x + w_bot, h_bot)
    
    src_points = np.float32([tl, tr, bl, br])

    # 3. Define Destination Points (The Square/Rectangle output)
    # We want the output to be a 400x400 top-down view
    dst_size = 400
    dst_points = np.float32([
        [0, 0],           # Top Left
        [dst_size, 0],    # Top Right
        [0, dst_size],    # Bottom Left
        [dst_size, dst_size] # Bottom Right
    ])

    # 4. Compute Perspective Transform
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    warped = cv2.warpPerspective(frame, matrix, (dst_size, dst_size))

    # 5. Apply Thresholding (To see if lines are clear)
    gray_warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    # If black tape on white floor, use cv2.THRESH_BINARY_INV
    # If white tape on black floor, use cv2.THRESH_BINARY
    _, binary = cv2.threshold(gray_warped, thresh_val, 255, cv2.THRESH_BINARY_INV)

    # Visualization: Draw the points on the original frame so you can see them
    cv2.circle(frame, tl, 5, (0, 0, 255), -1) # Red dots
    cv2.circle(frame, tr, 5, (0, 0, 255), -1)
    cv2.circle(frame, bl, 5, (0, 0, 255), -1)
    cv2.circle(frame, br, 5, (0, 0, 255), -1)
    cv2.line(frame, tl, tr, (0, 255, 0), 2)   # Green box
    cv2.line(frame, tr, br, (0, 255, 0), 2)
    cv2.line(frame, br, bl, (0, 255, 0), 2)
    cv2.line(frame, bl, tl, (0, 255, 0), 2)

    # Show windows
    cv2.imshow("Original with ROI", frame)
    cv2.imshow("Bird's Eye View (Warped)", binary)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('s'):
        print("\n--- SAVE THESE NUMBERS ---")
        print(f"Top Width: {w_top}")
        print(f"Bottom Width: {w_bot}")
        print(f"Height Top: {h_top}")
        print(f"Height Bottom: {h_bot}")
        print(f"Threshold: {thresh_val}")
        print("--------------------------\n")

cap.release()
cv2.destroyAllWindows()
