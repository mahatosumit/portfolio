# main.py – Autonomous Rover with Ultrasonic + Haar Vision + Picamera2
import time
import cv2
from motor import MotorController
from sensor import UltrasonicSensors
from camera import Camera       # Picamera2 version
from vision import Vision       # Haar detector

TH_CENTER_STOP     = 25.0
TH_SIDE_CAUTION    = 45.0
FORWARD_STEP       = 0.20
STRAFE_STEP        = 0.35
LOOP_DELAY         = 0.10


def safe(v):
    return float('inf') if v is None else float(v)


def log(*a): print(*a, flush=True)


class RoverMotor:
    def __init__(self):
        self.mc = MotorController("/dev/ttyACM0")
        log("MotorController ready")

    def forward(self): self.mc.forward()
    def backward(self): self.mc.backward()
    def strafe_left(self): self.mc.strafe_left()
    def strafe_right(self): self.mc.strafe_right()
    def rotate_left(self): self.mc.rotate_left()
    def rotate_right(self): self.mc.rotate_right()
    def stop(self): self.mc.stop()


def main():
    motor = RoverMotor()
    sensors = UltrasonicSensors()
    cam = Camera()
    vision = Vision()

    log("TravaX Rover Ready (Picamera2 + Haar)")

    try:
        while True:
            # ---- Get ultrasonic values ----
            dist = sensors.read_all()
            FL = safe(dist["FL"])
            FC = safe(dist["FC"])
            FR = safe(dist["FR"])
            RE = safe(dist["RE"])

            log(f"US: FL={FL:.1f} FC={FC:.1f} FR={FR:.1f} RE={RE:.1f}")

            # ---- Get camera frame ----
            frame = cam.get_frame()
            if frame is None:
                log("No camera frame → STOP")
                motor.stop()
                continue

            # ---- Vision detection ----
            bodies = vision.detect(frame)
            display = vision.annotate(frame, bodies)

            if len(bodies) > 0:
                log("HUMAN DETECTED → STOP")
                motor.stop()
                cv2.imshow("TravaX Vision", display)
                cv2.waitKey(1)
                time.sleep(0.2)
                continue

            # ---- Obstacle Logic ----
            if FC < TH_CENTER_STOP:
                log("Obstacle FRONT → sidestep")
                motor.stop()
                if FR > FL:
                    motor.strafe_right()
                else:
                    motor.strafe_left()
                time.sleep(STRAFE_STEP)
                motor.stop()

            elif FL < TH_SIDE_CAUTION:
                log("Obstacle LEFT → strafe right")
                motor.strafe_right()
                time.sleep(STRAFE_STEP)
                motor.stop()

            elif FR < TH_SIDE_CAUTION:
                log("Obstacle RIGHT → strafe left")
                motor.strafe_left()
                time.sleep(STRAFE_STEP)
                motor.stop()

            elif RE < TH_CENTER_STOP:
                log("Obstacle REAR → forward bump")
                motor.forward()
                time.sleep(FORWARD_STEP)
                motor.stop()

            else:
                log("PATH CLEAR → forward step")
                motor.forward()
                time.sleep(FORWARD_STEP)
                motor.stop()

            # Display for debugging
            cv2.imshow("TravaX Vision", display)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(LOOP_DELAY)

    except KeyboardInterrupt:
        log("Manual STOP")

    finally:
        motor.stop()
        cam.release()
        cv2.destroyAllWindows()
        log("Rover shut down cleanly")


if __name__ == "__main__":
    main()
