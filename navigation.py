import cv2
import numpy as np
from collections import deque


class LaneDetector:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        # ================== CONFIG ==================
        self.DETECT_DARK_LINE = True  # BFMC tiles: dark tape on light floor

        # ================== PERSPECTIVE ==================
        self.src_points = np.float32([
            [80,  height],
            [150, int(height * 0.65)],
            [490, int(height * 0.65)],
            [560, height]
        ])

        self.dst_points = np.float32([
            [160, height],
            [160, 0],
            [width - 160, 0],
            [width - 160, height]
        ])

        self.M = cv2.getPerspectiveTransform(self.src_points, self.dst_points)

        # ================== MEMORY ==================
        self.prev_error = 0.0
        self.prev_curvature = 0.0
        self.error_history = deque(maxlen=10)

        self.alpha = 0.55
        self.max_delta = 0.05
        self.blind_decay = 0.995   # ⬅️ critical fix

        # Learned lane width (normalized)
        self.nominal_lane_width = 0.45

    # ------------------------------------------------
    def preprocess(self, frame):
        if frame is None:
            return None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ROI: bottom 50% (more forgiving)
        mask = np.zeros_like(gray)
        cv2.rectangle(
            mask,
            (0, int(self.height * 0.50)),
            (self.width, self.height),
            255,
            -1
        )
        gray = cv2.bitwise_and(gray, mask)

        # Blur stabilizes adaptive threshold
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        thresh_type = cv2.THRESH_BINARY_INV if self.DETECT_DARK_LINE else cv2.THRESH_BINARY

        binary = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresh_type,
            31,     # larger neighborhood
            15      # less aggressive subtraction
        )

      
        kernel = np.ones((7, 7), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=3)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

        return binary

    # ------------------------------------------------
    def warp(self, img):
        if img is None:
            return None
        return cv2.warpPerspective(img, self.M, (self.width, self.height))

    # ------------------------------------------------
    def _scan_slices(self, binary):
        """
        Multi-slice horizontal scan.
        BFMC lanes persist across slices.
        """
        h, w = binary.shape
        ys = np.linspace(h * 0.90, h * 0.40, 7).astype(int)

        left_pts, right_pts = [], []

        for y in ys:
            row = binary[y]
            xs = np.where(row > 0)[0]

           
            if len(xs) < 8:
                continue

            center = w // 2
            left = xs[xs < center]
            right = xs[xs > center]

            if len(left) > 5:
                left_pts.append(np.mean(left))
            if len(right) > 5:
                right_pts.append(np.mean(right))

        return left_pts, right_pts

    # ------------------------------------------------
    def compute_lane(self, binary):
        h, w = binary.shape
        center_x = w // 2

        left_pts, right_pts = self._scan_slices(binary)

        # ================= BLIND HANDLING =================
        if len(left_pts) < 2 and len(right_pts) < 2:
            # Predict forward (coast through gaps)
            self.prev_error = (
                self.prev_error * self.blind_decay +
                self.prev_curvature
            )
            return (
                float(np.clip(self.prev_error, -1.0, 1.0)),
                float(self.prev_curvature),
                0.0
            )

        # ================= CONFIDENCE =================
        num_slices = max(len(left_pts), len(right_pts))
        confidence = min(1.0, num_slices / 5.0)

        # ================= GEOMETRY =================
        if left_pts and right_pts:
            left_x = np.mean(left_pts)
            right_x = np.mean(right_pts)
            lane_width = right_x - left_x

            if w * 0.25 < lane_width < w * 0.9:
                target_x = (left_x + right_x) / 2
                self.nominal_lane_width = (
                    0.8 * self.nominal_lane_width +
                    0.2 * (lane_width / w)
                )
            else:
                target_x = center_x
                confidence *= 0.6

        elif left_pts:
            left_x = np.mean(left_pts)
            target_x = left_x + self.nominal_lane_width * w
            confidence *= 0.8

        else:
            right_x = np.mean(right_pts)
            target_x = right_x - self.nominal_lane_width * w
            confidence *= 0.8

        # ================= ERROR =================
        error = (target_x - center_x) / (w / 2)

        # ================= CURVATURE =================
        if len(self.error_history) >= 2:
            self.prev_curvature = error - self.error_history[-1]

        self.error_history.append(error)

        # ================= SMOOTHING =================
        smooth = self.alpha * self.prev_error + (1 - self.alpha) * error
        delta = np.clip(smooth - self.prev_error, -self.max_delta, self.max_delta)
        final_error = self.prev_error + delta

        self.prev_error = final_error

        return (
            float(np.clip(final_error, -1.0, 1.0)),
            float(self.prev_curvature),
            confidence
        )
