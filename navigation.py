import time
from motor import MotorController
from sensor import UltrasonicSensors
from vision import HaarVision

RUN_TIME = 120   # 2 minutes

def main():
    print("TravaX Rover Ready (2-minute run mode enabled)")

    mc = MotorController()
    us = UltrasonicSensors()
    vision = HaarVision()

    start_time = time.time()

    while True:

        # ========================
        # AUTO STOP AFTER 2 MINUTES
        # ========================
        elapsed = time.time() - start_time
        if elapsed >= RUN_TIME:
            print("\n=== 2 MINUTES FINISHED — STOPPING ROVER ===")
            mc.stop()
            time.sleep(0.5)
            print("Rover stopped safely.\n")
            break

        try:
            # ----- ULTRASONIC -----
            dist = us.read_all()
            FL, FC, FR, RE = dist["FL"], dist["FC"], dist["FR"], dist["RE"]

            print(f"US: FL={FL} FC={FC} FR={FR} RE={RE}")

            rear_blocked  = RE < 15
            front_blocked = (FC < 25) or (FL < 20)

            # ----- CAMERA -----
            face = vision.detect()

            # ===== LOGIC =====
            if rear_blocked:
                print("Obstacle REAR → forward bump")
                mc.forward()
                time.sleep(0.15)
                mc.stop()
                continue

            if face is not None:
                print("Face detected → stopping")
                mc.stop()
                continue

            if front_blocked:
                print("Front obstacle → rotate left")
                mc.stop()
                time.sleep(0.2)
                mc.rotate_left()
                time.sleep(0.4)
                mc.stop()
                continue

            print("PATH CLEAR → forward step")
            mc.forward()
            time.sleep(0.15)
            mc.stop()

        except Exception as e:
            # DO NOT STOP THE PROGRAM
            print("[WARNING — continuing]", e)
            time.sleep(0.1)
            continue


if __name__ == "__main__":
    main()
