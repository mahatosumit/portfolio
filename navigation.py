# main.py — Autonomous Rover (Stable Version)
# Ultrasonic + Haar Vision + Picamera2 + Serial Reconnect

import time
import cv2
from motor import MotorController
from sensor import UltrasonicSensors
from camera import Camera
from vision import Vision


# ----------- CONFIGURATIONS -----------

TH_CENTER_STOP   = 25.0
TH_SIDE_CAUTION  = 45.0
FORWARD_STEP     = 0.20
STRAFE_STEP      = 0.35
LOOP_DELAY       = 0.10


# ----------- UTILITY FUNCTIONS -----------

def safe(v):
    return float('inf') if (v is None or v == float('inf')) else float(v)

def log(*a):
    print(*a, flush=True)


# ----------- WRAPPER CLASS FOR STABLE MOTOR USAGE -----------

class RoverMotor:
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.mc = MotorController("/dev/ttyACM0")
            log("[Motor] Connected")
        except Exception as e:
            log("[Motor ERROR] Failed to connect:", e)
            self.mc = None

    def ensure_connection(self):
        """Reconnect automatically if serial dropped."""
        if self.mc is None:
            log("[Motor] Serial missing → reconnecting")
            self.connect()
            return

        if not self.mc.ser.is_open:
            log("[Motor] Serial closed → reconnecting")
            self.connect()

    # Safe wrappers
    def forward(self):       self.ensure_connection(); self.mc.forward()
    def backward(self):      self.ensure_connection(); self.mc.backward()
    def strafe_left(self):   self.ensure_connection(); self.mc.strafe_left()
    def strafe_right(self):  self.ensure_connection(); self.mc.strafe_right()
    def rotate_left(self):   self.ensure_connection(); self.mc.rotate_left()
    def rotate_right(self):  self.ensure_connection(); self.mc.rotate_right()
    def stop(self):          
        try:
            self.ensure_connection()
            self.mc.stop()
        except:
            pass


# ----------- MAIN ROVER LOGIC -----------

def main():
    motor   = RoverMotor()
    sensors = UltrasonicSensors()
    cam     = Camera()
    vision  = Vision()

    log("TravaX Rover Ready (Picamera2 + Haar + Safe Serial)")

    try:
        while True:

            # ----- SENSOR READ -----
            dist = sensors.read_all()
            FL = safe(dist["FL"])
            FC = safe(dist["FC"])
            FR = safe(dist["FR"])
            RE = safe(dist["RE"])

            log(f"US: FL={FL:.1f} FC={FC:.1f} FR={FR:.1f} RE={RE:.1f}")

            # ----- CAMERA FRAME -----
            frame = cam.get_frame()
            if frame is None:
                log("[Camera] No frame → STOP")
                motor.stop()
                continue

            # ----- VISION -----
            bodies = vision.detect(frame)
            display = vision.annotate(frame, bodies)

            if len(bodies) > 0:
                log("[Vision] HUMAN DETECTED → STOP")
                motor.stop()
                cv2.imshow("Vision", display)
                cv2.waitKey(1)
                continue

            # ----- OBSTACLE AVOIDANCE -----

            # FRONT obstacle
            if FC < TH_CENTER_STOP:
                log("Obstacle FRONT → sidestep")
                motor.stop()
                time.sleep(0.1)

                if FR > FL:
                    motor.strafe_right()
                else:
                    motor.strafe_left()

                time.sleep(STRAFE_STEP)
                motor.stop()

            # LEFT obstacle
            elif FL < TH_SIDE_CAUTION:
                log("Obstacle LEFT → strafe right")
                motor.strafe_right()
                time.sleep(STRAFE_STEP)
                motor.stop()

            # RIGHT obstacle
            elif FR < TH_SIDE_CAUTION:
                log("Obstacle RIGHT → strafe left")
                motor.strafe_left()
                time.sleep(STRAFE_STEP)
                motor.stop()

            # REAR obstacle → move forward
            elif RE < TH_CENTER_STOP:
                log("Obstacle REAR → forward bump")
                motor.forward()
                time.sleep(FORWARD_STEP)
                motor.stop()

            # CLEAR → forward
            else:
                log("PATH CLEAR → forward step")
                motor.forward()
                time.sleep(FORWARD_STEP)
                motor.stop()

            # SHOW VISION WINDOW
            cv2.imshow("Vision", display)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(LOOP_DELAY)

    except KeyboardInterrupt:
        log("Manual STOP")

    except Exception as e:
        log("[FATAL ERROR]", e)
        motor.stop()

    finally:
        motor.stop()
        cam.release()
        cv2.destroyAllWindows()
        log("Rover shut down cleanly")


# ----------- ENTRY POINT -----------

if __name__ == "__main__":
    main()
