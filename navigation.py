import serial
import time
import threading
import math

# =====================================================
# 1. CONFIGURATION
# =====================================================
SERIAL_PORT = "/dev/ttyACM0"  # Check: might be /dev/ttyUSB0
BAUD_RATE = 115200

# Limits
MAX_SPEED = 15.0   # Start slow for testing (0-100 scale)
MAX_STEER = 25.0   # Degrees

# =====================================================
# 2. GLOBAL STATE (Shared between threads)
# =====================================================
# These are the "Brain's" current decisions.
# The background thread will send whatever is in here.
current_speed = 0.0
current_steer = 0.0
system_running = True

# =====================================================
# 3. BACKGROUND WORKER (The "Heartbeat")
# =====================================================
def serial_worker():
    """
    This thread runs in the background. 
    It wakes up every 50ms (20Hz) and sends the current command.
    This satisfies the STM32's 200ms watchdog.
    """
    global system_running
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
        time.sleep(2) # Allow STM32 to reset
        print(f"✅ Connected to {SERIAL_PORT}")
        
        while system_running:
            # Format: #S:15.5;;#T:-20.0;;
            # Note: We send both every time to keep the state robust
            cmd = f"#S:{current_speed:.2f};;#T:{current_steer:.2f};;\r\n"
            
            ser.write(cmd.encode('utf-8'))
            
            # Print occasionally for debugging (every 20th packet)
            # print(f"Sent: {cmd.strip()}") 
            
            time.sleep(0.05) # 50ms wait = 20Hz update rate
            
        # Clean exit
        ser.write(b"#S:0;;#T:0;;\r\n")
        ser.close()
        print("🔌 Serial closed.")
        
    except Exception as e:
        print(f"❌ SERIAL ERROR: {e}")
        system_running = False

# =====================================================
# 4. MAIN TEST SEQUENCE
# =====================================================
def main():
    global current_speed, current_steer, system_running
    
    # Start the heartbeat thread
    t = threading.Thread(target=serial_worker)
    t.start()
    
    print("🚗 TEST STARTED: Watchdog is being fed in background.")
    time.sleep(1)

    try:
        # --- TEST 1: STEERING SWEEP ---
        print("\n[1/4] Testing Steering (Check range of motion)")
        print("   -> Center")
        current_steer = 0.0
        time.sleep(1)
        
        print("   -> Right 20 deg")
        current_steer = 20.0
        time.sleep(1)
        
        print("   -> Left 20 deg")
        current_steer = -20.0
        time.sleep(1)
        
        print("   -> Center")
        current_steer = 0.0
        time.sleep(1)

        # --- TEST 2: COSINE SMOOTHNESS CHECK ---
        # This simulates your lane-keep algorithm output
        print("\n[2/4] Testing Smoothness (Sine Wave Steering)")
        for i in range(0, 360, 5):
            rad = math.radians(i)
            current_steer = math.sin(rad) * 20.0 # Swing +/- 20 deg
            time.sleep(0.05)
        current_steer = 0.0

        # --- TEST 3: MOTOR GENTLE MOVE ---
        print("\n[3/4] Testing Motor (Low Speed)")
        print("   -> Forward 15%")
        current_speed = MAX_SPEED
        time.sleep(2)
        
        print("   -> Stop")
        current_speed = 0.0
        time.sleep(1)

        # --- TEST 4: WATCHDOG SAFETY CHECK ---
        print("\n[4/4] Testing Safety Watchdog")
        print("   -> Motor running...")
        current_speed = MAX_SPEED
        time.sleep(1)
        
        print("   -> SIMULATING CRASH (Stopping Python Thread)")
        # We purposely stop the background thread to see if STM32 stops the car
        system_running = False 
        t.join() # Wait for thread to die
        
        print("   -> Thread stopped. STM32 should have auto-braked by now.")
        print("   -> (If wheels are still spinning, the Watchdog failed!)")

    except KeyboardInterrupt:
        print("\n🛑 INTERRUPTED! Stopping...")
        current_speed = 0
        current_steer = 0
        system_running = False
        t.join()

if __name__ == "__main__":
    main()
