# main.py
# Final reliable autonomous rover: ultrasonic obstacle avoidance + Haar human-stop
# Uses motor.py, sensor.py, camera.py, vision.py in same folder.

import time
import cv2
from motor import MotorController
from sensor import UltrasonicSensors
from camera import Camera
from vision import Vision

# ---------- Config (tune if needed) ----------
TH_CENTER_STOP = 25.0     # cm, immediate stop threshold
TH_SIDE_CAUTION = 45.0    # cm, side caution threshold
FORWARD_STEP = 0.20       # seconds of forward motion for small advance
STRAFE_STEP = 0.35        # seconds to perform a strafe
LOOP_DELAY = 0.10         # main loop base delay

# ---------- Helpers ----------
def safe_float(v):
    return float('inf') if v is None else float(v)

def log(*args):
    print(*args, flush=True)

# ---------- Motor wrapper ----------
class RoverMotor:
    def __init__(self, port="/dev/ttyACM0"):
        try:
            self.mc = MotorController(port=port)
            log("MotorController connected")
        except Exception as e:
            log("Motor init error:", e)
            raise

    def forward(self): self.mc.forward()
    def backward(self): self.mc.backward()
    def rotate_left(self): self.mc.rotate_left()
    def rotate_right(self): self.mc.rotate_right()
    def strafe_left(self): self.mc.strafe_left()
    def strafe_right(self): self.mc.strafe_right()
    def stop(self): self.mc.stop()

# ---------- Main logic ----------
def main():
    motor = None
    sensors = None
    cam = None
    vision = None

    try:
        motor = RoverMotor()
        sensors = UltrasonicSensors()
        cam = Camera()
        vision = Vision()
    except Exception as e:
        log("Initialization failed:", e)
        # Ensure safe stop if motors were initialized
        if motor:
            try: motor.stop()
            except: pass
        return

    log("System ready. Ctrl+C to stop.")

    try:
        while True:
            # Read ultrasonics
            try:
                us = sensors.read_all()
            except Exception as e:
                log("Ultrasonic read error:", e)
                us = {'FL': None, 'FC': None, 'FR': None, 'RE': None}

            FL = safe_float(us.get('FL'))
            FC = safe_float(us.get('FC'))
            FR = safe_float(us.get('FR'))
            RE = safe_float(us.get('RE'))

            log(f"US -> FL:{FL:.1f} FC:{FC:.1f} FR:{FR:.1f} RE:{RE:.1f}")

            # Read camera
            frame = cam.get_frame()
            if frame is None:
                log("No camera frame - stopping for safety")
                motor.stop()
                time.sleep(0.2)
                continue

            # Vision detection
            bodies = vision.detect(frame)
            display = vision.annotate(frame, bodies)

            # Vision priority: if human present -> stop immediately
            if len(bodies) > 0:
                log("Human detected -> STOP")
                motor.stop()
                cv2.imshow("TravaX Vision", display)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # wait short so human can move away; then continue sensing
                time.sleep(0.2)
                continue

            # Ultrasonic obstacle avoidance (highest priority next)
            if FC < TH_CENTER_STOP:
                log("FRONT OBSTACLE -> STOP then sidestep")
                motor.stop()
                # choose safer side by comparing FL/FR; treat None as far
                if FR >= FL:
                    motor.strafe_right()
                    log("Strafing right")
                else:
                    motor.strafe_left()
                    log("Strafing left")
                time.sleep(STRAFE_STEP)
                motor.stop()
                time.sleep(0.1)
                continue

            # side avoidance
            if FL < TH_SIDE_CAUTION:
                log("Left too close -> strafe right")
                motor.strafe_right()
                time.sleep(STRAFE_STEP)
                motor.stop()
                continue

            if FR < TH_SIDE_CAUTION:
                log("Right too close -> strafe left")
                motor.strafe_left()
                time.sleep(STRAFE_STEP)
                motor.stop()
                continue

            # rear avoidance
            if RE < TH_CENTER_STOP:
                log("Rear close -> small forward bump")
                motor.forward()
                time.sleep(FORWARD_STEP)
                motor.stop()
                continue

            # default: forward small bursts, repeatedly re-evaluate
            log("Path clear -> forward step")
            motor.forward()
            time.sleep(FORWARD_STEP)
            motor.stop()

            # show camera window (non-blocking)
            cv2.imshow("TravaX Vision", display)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(LOOP_DELAY)

    except KeyboardInterrupt:
        log("User interrupted - stopping")

    except Exception as e:
        log("Runtime error:", e)

    finally:
        try:
            motor.stop()
        except Exception:
            pass
        try:
            cam.release()
        except Exception:
            pass
        cv2.destroyAllWindows()
        log("Shutdown complete.")

if __name__ == "__main__":
    main()
