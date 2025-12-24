import cv2
import subprocess
import numpy as np

class LibCamera:
    def __init__(self, width=640, height=480, framerate=30):
        self.width = width
        self.height = height
        self.framerate = framerate
        self.process = None
        
        # Command to run rpicam-vid (formerly libcamera-vid)
        # -t 0: Run correctly forever
        # --inline: Embed header information for easier parsing
        # --codec mjpeg: MJPEG is fastest for Python to decode via cv2.imdecode
        # -o -: Output to stdout (pipe)
        self.cmd = [
            "rpicam-vid",
            "-t", "0",
            "--inline",
            "--width", str(self.width),
            "--height", str(self.height),
            "--framerate", str(self.framerate),
            "--codec", "mjpeg",
            "-o", "-"
        ]

    def start(self):
        # Launch the camera process
        self.process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
        print("Creating Camera Pipeline...")

    def get_frame(self):
        # We need to read the MJPEG stream from stdout
        # This is a simplified reader; for robust threading, you might want to run this in a separate thread
        
        # NOTE: In a real BFMC race loop, you should run this reading in a separate 
        # thread (threading.Thread) to ensure you always have the latest frame 
        # ready for your main loop.
        
        # Reading chunk by chunk (this logic effectively parses for JPEG start/end bytes)
        # For simplicity in testing, we rely on the fact that we can read chunks. 
        # A more robust implementation buffers bytes and looks for 0xFF 0xD8 (Start) and 0xFF 0xD9 (End).
        
        # Quick hack for testing (Not production grade for 100mph racing, but works to verify setup):
        # Real implementation requires a buffer reader.
        pass 
        # *Use the implementation below for the actual robust code*

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

# --- ROBUST IMPLEMENTATION ---
# Since reading MJPEG streams from a pipe can be tricky, 
# here is a ready-to-use threaded version which is BFMC-ready.

import threading

class BFMC_Camera:
    def __init__(self, width=640, height=480, framerate=30):
        self.cmd = [
            "rpicam-vid", "-t", "0", "--inline", 
            "--width", str(width), "--height", str(height), 
            "--framerate", str(framerate), 
            "--codec", "mjpeg", "--nopreview", "-o", "-"
        ]
        self.process = None
        self.running = False
        self.thread = None
        self.latest_frame = None
        self.lock = threading.Lock()

    def start(self):
        self.process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, bufsize=10**6)
        self.running = True
        self.thread = threading.Thread(target=self._update)
        self.thread.daemon = True
        self.thread.start()
        print(f"BFMC Camera started: {self.cmd}")

    def _update(self):
        # Reads the stream and updates self.latest_frame
        stream_bytes = b''
        while self.running:
            # Read a chunk of data
            chunk = self.process.stdout.read(4096)
            if not chunk:
                break
            stream_bytes += chunk
            
            # Look for JPEG Start (0xffd8) and End (0xffd9)
            a = stream_bytes.find(b'\xff\xd8')
            b = stream_bytes.find(b'\xff\xd9')
            
            if a != -1 and b != -1:
                jpg = stream_bytes[a:b+2]
                stream_bytes = stream_bytes[b+2:]
                
                # Decode the image
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                
                if frame is not None:
                    with self.lock:
                        self.latest_frame = frame

    def read(self):
        with self.lock:
            return self.latest_frame

    def stop(self):
        self.running = False
        if self.process:
            self.process.terminate()

# --- USAGE EXAMPLE ---
if __name__ == "__main__":
    cam = BFMC_Camera()
    cam.start()
    
    # Wait a moment for camera to warm up
    import time
    time.sleep(2)
    
    while True:
        frame = cam.read()
        if frame is not None:
            cv2.imshow("BFMC View", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cam.stop()
    cv2.destroyAllWindows()
