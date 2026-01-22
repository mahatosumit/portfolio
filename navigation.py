from enum import Enum
import time


class State(Enum):
    INIT = 0
    LANE_FOLLOW = 1
    CAUTION = 2
    BLIND = 3
    OBSTACLE = 4
    STOP = 5


class FSM:
    def __init__(self):
        self.state = State.INIT
        self.state_enter_time = time.time()

        # ==================================================
        # Phase-2 note:
        # Sign handling is architecturally present
        # but NOT behaviorally active in Phase-2
        # ==================================================
        self.sign_memory = 0.0
        self.ignore_stop_sign_until = 0.0

    # --------------------------------------------------
    def transition(self, new_state: State):
        if new_state != self.state:
            self.state = new_state
            self.state_enter_time = time.time()
            print(f"[FSM] -> {self.state.name}")

    # --------------------------------------------------
    def update(self, signals: dict) -> State:
        now = time.time()
        elapsed = now - self.state_enter_time

        lane_conf = signals.get("lane_confidence", 0.0)
        obstacle = signals.get("obstacle", False)

        # ================= INIT =================
        # Phase-2: INIT must NEVER block autonomy
        # Immediately enter lane-following
        if self.state == State.INIT:
            self.transition(State.LANE_FOLLOW)

        # ================= LANE FOLLOW =================
        elif self.state == State.LANE_FOLLOW:
            if obstacle:
                self.transition(State.OBSTACLE)
            elif lane_conf == 0.0:
                self.transition(State.BLIND)
            elif lane_conf < 0.6:
                self.transition(State.CAUTION)

        # ================= CAUTION =================
        elif self.state == State.CAUTION:
            if obstacle:
                self.transition(State.OBSTACLE)
            elif lane_conf == 0.0:
                self.transition(State.BLIND)
            elif lane_conf > 0.8:
                self.transition(State.LANE_FOLLOW)

        # ================= BLIND =================
        elif self.state == State.BLIND:
            if lane_conf > 0.6:
                self.transition(State.CAUTION)
            elif elapsed > 2.0:
                print("[FSM] SAFETY STOP: Lane lost too long")
                self.transition(State.STOP)

        # ================= OBSTACLE =================
        elif self.state == State.OBSTACLE:
            if not obstacle and elapsed > 0.5:
                self.transition(State.CAUTION)

        # ================= STOP =================
        elif self.state == State.STOP:
            # Phase-2: basic safety stop only
            if elapsed > 3.0:
                self.transition(State.CAUTION)

        return self.state
