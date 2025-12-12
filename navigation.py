# main.py
# TravaX Autonomous Rover – Ultrasonic + Vision + Motor Control

import time
import cv2
from motor import MotorController
from sensor import UltrasonicSensors
from camera import Camera
from vision import Vision   # Haar-based human detector

# ------------------ PARAMETERS ------------------
TH_CENTER_STOP = 25.0      # Stop immediately if obstacle < 25 cm
TH_SIDE_CAUTION = 45.0     # Avoid walls/sides < 45 cm
FORWARD_STEP = 0.20        # Forward burst in seconds
STRAFE_STEP = 0.35         # Side step duration
ROTATE_STEP = 0.35         # Rotation duration
LOOP_DELAY = 0.10          # Delay between loop cycles

# ------------------ HELPERS ------------------
def d(v):
    return float('inf') if v is None else float(v)

def log(*args):
    print(*args, flush=True)

# Motor wrapper
class RoverMotor:
    def __init__(self):
        self.mc = MotorController("/dev/ttyACM0")
        log("Motor controller connected")

    def send(self, cmd):
        try:
            ack = self.mc.send(cmd)
            log(ack)
        except Exception as e:
            log("Motor command error:", e)

    def forward(self): self.send("FWD")
    def backward(self): self.send("BACK")
    def left(self): self.send("LEFT")
    def right(self): self.send("RIGHT")
    def strafe_left(self): self.send("SL")
    def strafe_right(self): self.send("SR")
    def stop(self): self.send("STOP")

# ------------------ MAIN CONTROL LOGIC ------------------
def main():
    motor = RoverMotor()
    sensor = UltrasonicSensors()
    cam = Camera()
    vision = Vision()

    log("System ready. Press CTRL+C to stop.")

    try:
        while True:

            # ----------- SENSOR READINGS -----------
            dist = sensor.read_all()
            FL, FC, FR, RE = d(dist["FL"]), d(dist["FC"]), d(dist["FR"]), d(dist["RE"])
            log(f"US: FL={FL}  FC={FC}  FR={FR}  RE={RE}")

            # ----------- CAMERA FRAME ----------
            frame = cam.get_frame()
            if frame is None:
                motor.stop()
                continue

            # ----------- HUMAN DETECTION ----------
            humans = vision.detect(frame)
            display = vision.annotate(frame, humans)

            if len(humans) > 0:
                log("HUMAN DETECTED → STOP")
                motor.stop()
                cv2.imshow("TravaX Vision", display)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                time.sleep(0.1)
                continue

            # ----------- OBSTACLE AVOIDANCE ----------
            # Close obstacle directly in front
            if FC < TH_CENTER_STOP:
                log("Obstacle front → STOP + sidestep")
                motor.stop()

                # Choose safer side based on left/right distance
                if FR > FL:
                    motor.strafe_right()
                else:
                    motor.strafe_left()

                time.sleep(STRAFE_STEP)
                motor.stop()
                time.sleep(0.1)

            # Side avoidance
            elif FL < TH_SIDE_CAUTION:
                log("Left side too close → strafe right")
                motor.strafe_right()
                time.sleep(STRAFE_STEP)
                motor.stop()

            elif FR < TH_SIDE_CAUTION:
                log("Right side too close → strafe left")
                motor.strafe_left()
                time.sleep(STRAFE_STEP)
                motor.stop()

            # Rear avoidance
            elif RE < TH_CENTER_STOP:
                log("Rear close → move forward slightly")
                motor.forward()
                time.sleep(FORWARD_STEP)
                motor.stop()

            # Clear path → move forward in small steps
            else:
                log("Path clear → forward step")
                motor.forward()
                time.sleep(FORWARD_STEP)
                motor.stop()

            # Show camera window
            cv2.imshow("TravaX Vision", display)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(LOOP_DELAY)

    except KeyboardInterrupt:
        log("Shutdown by user.")

    except Exception as e:
        log("Fatal error:", e)

    finally:
        motor.stop()
        cv2.destroyAllWindows()
        log("System stopped safely.")

# ------------------ ENTRY ------------------
if __name__ == "__main__":
    main()
