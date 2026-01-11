import time
from enum import Enum

class State(Enum):
    IDLE = 0
    LANE_FOLLOW = 1
    STOP = 2
    EMERGENCY = 3

class FSM:
    def __init__(self, camera=None, logger=None):
        self.state = State.IDLE
        self.camera = camera
        self.logger = logger

    def run(self):
        while True:
            self.step()
            time.sleep(0.05)

    def step(self):
        if self.state == State.IDLE:
            self.handle_idle()
        elif self.state == State.LANE_FOLLOW:
            self.handle_lane_follow()
        elif self.state == State.STOP:
            self.handle_stop()
        elif self.state == State.EMERGENCY:
            self.handle_emergency()

    def handle_idle(self):
        # temporary: read frame to validate pipeline
        ok, _ = self.camera.read()
        if not ok and self.logger:
            self.logger.warning("Camera read failed in IDLE")

    def handle_lane_follow(self):
        pass

    def handle_stop(self):
        pass

    def handle_emergency(self):
        pass
