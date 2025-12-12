import time
from motor import MotorController
from sensor import UltrasonicSensors
from vision import Vision   # <-- FIXED IMPORT

RUN_TIME = 120  # 2 minutes

def main():
    print("TravaX Rover Ready (2-minute run mode)")

    mc = MotorController()
    us = UltrasonicSensors()
    vision = Vision()   # <-- FIXED CLASS NAME

    start = time.time()

    while True:

        # ===== AUTO STOP AFTER 2 MINUTES =====
        if time.time() - start >= RUN_TIME:
            print("\n=== 2 MINUTES COMPLETE — STOPPING ROVER ===")
            mc.stop()
            time.sleep(0.5)
            print("Rover stopped safely.")
            break

        try:
            # --- READ ULTRASONIC ---
            dist = us.read_all()
            FL, FC, FR, RE = dist["FL"], dist["FC"], dist["FR"], dist["RE"]

            print(f"US: FL={FL} FC={FC} FR={FR} RE={RE}")

            rear_blocked  = RE < 15
            front_blocked = (FC < 25) or (FL < 20)

            # --- CAMERA FRAME ---
            frame = vision.capture() if hasattr(vision, "capture") else None

            bodies = []
            if frame is not None:
                bodies = vision.detect(frame)

            # ===== DECISION LOGIC =====
            if rear_blocked:
                print("Rear obstacle → forward bump")
                mc.forward()
                time.sleep(0.15)
                mc.stop()
                continue

            if len(bodies) > 0:
                print("Human detected → STOP")
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
            print("[WARNING — continuing loop]", e)
            time.sleep(0.1)
            continue


if __name__ == "__main__":
    main()
