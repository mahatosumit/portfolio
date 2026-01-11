import serial
import time
import threading

class SerialHandler:
    def __init__(self, port="/dev/ttyACM0", baud=115200):
        self.port = port
        self.baud = baud
        self.ser = None
        self.running = False
        self.thread = None
        
        # Shared State Variables (Thread-Safe)
        self.current_speed = 0.0
        self.current_steer = 0.0
        self.lock = threading.Lock()

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=0.1)
            time.sleep(2.0)  # Wait for STM32 reset
            print(f"[Serial] Connected to {self.port}")
            
            # Start the background heartbeat thread
            self.running = True
            self.thread = threading.Thread(target=self._worker, daemon=True)
            self.thread.start()
            
        except Exception as e:
            print(f"[Serial] Connection Error: {e}")
            self.running = False

    def _worker(self):
        """
        Background Loop: 
        Sends the latest speed/steer command every 50ms (20Hz).
        This keeps the STM32 Watchdog happy!
        """
        while self.running:
            if self.ser and self.ser.is_open:
                try:
                    # 1. Read the latest decisions from Main Thread
                    with self.lock:
                        speed = self.current_speed
                        steer = self.current_steer
                    
                    # 2. Format & Send Packet
                    # Format: #S:15.0;;#T:-5.0;;
                    cmd = f"#S:{speed:.2f};;#T:{steer:.2f};;\r\n"
                    self.ser.write(cmd.encode())
                    
                except Exception as e:
                    print(f"[Serial] Write Error: {e}")
            
            # 3. Wait 50ms (20Hz)
            time.sleep(0.05)

    def send_command(self, speed, steer):
        """
        Main thread calls this to UPDATE decisions.
        It is NON-BLOCKING (instant).
        """
        # Safety Clamping
        speed = max(-100.0, min(speed, 100.0))
        steer = max(-25.0, min(steer, 25.0))
        
        # Update shared variables
        with self.lock:
            self.current_speed = speed
            self.current_steer = steer

    def enable_ignition(self):
        """Helper to send the KL15 command once"""
        if self.ser and self.ser.is_open:
            self.ser.write(b"#kl:1;;\r\n")

    def stop(self):
        self.running = False
        # Stop the car before closing
        self.send_command(0, 0)
        time.sleep(0.1)
        
        if self.thread:
            self.thread.join(timeout=1.0)
            
        if self.ser:
            try:
                self.ser.close()
            except:
                pass
        print("[Serial] Disconnected")
