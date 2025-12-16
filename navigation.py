import serial
import time

class RoverSerial:
    def __init__(self, port="/dev/ttyACM0", baud=115200):
        self.ser = serial.Serial(port, baud, timeout=0.1)
        time.sleep(2)  # wait for Arduino reset
        self.last_cmd = None

    def send(self, cmd):
        if cmd != self.last_cmd:
            self.ser.write((cmd + "\n").encode())
            self.last_cmd = cmd

    def close(self):
        self.ser.write(b"STOP\n")
        self.ser.close()
