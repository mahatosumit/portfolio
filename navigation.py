import time

from Brain.orchestrator import Orchestrator
from Brain.planner import plan_action
from Brain.safety import safety_filter
from Brain.vision_fast import detect_hazards
from Brain.camera import capture_frame
from Brain.voice import VoiceEngine
from Brain.voice_input import VoiceInput
from Brain.online_ai import ask_gemini, suggest_intent
from Brain.actions import Action


# ================= INIT =================
orchestrator = Orchestrator(mode="personal_care")
voice = VoiceEngine()

print("ZunoBot Brain Running (Vision + Voice + Gemini)\n")

# ---------- STATES ----------
latest_user_command = None
awake = False
WAKE_WORD = "hey zuno"

last_action = None
last_spoken = None
last_ai_reply = None

# Perception throttling
LAST_VISION_TIME = 0
VISION_INTERVAL = 2.5  # seconds

# Brain loop throttling
LOOP_DELAY = 0.15  # seconds (VERY IMPORTANT)

# Conversation memory
conversation_memory = []
MAX_MEMORY = 5


# ========== VOICE CALLBACK ==========
def on_voice_text(text: str):
    global latest_user_command, awake

    text = text.lower().strip()
    print("Heard:", text)

    if WAKE_WORD in text:
        awake = True
        voice.speak("Yes, I am listening.")
        return

    if awake:
        latest_user_command = text
        awake = False


voice_input = VoiceInput(
    model_path="/home/pi/zunobot/models/vosk-model-small-en-us-0.15"
)
voice_input.on_text = on_voice_text
voice_input.start()


# ================= MAIN LOOP =================
while True:
    now = time.time()

    # ---------- 1. FRAME ACQUIRE (NON-BLOCKING) ----------
    frame = capture_frame()
    if frame is None:
        time.sleep(LOOP_DELAY)
        continue

    # ---------- 2. VISION (TIME-GATED) ----------
    if now - LAST_VISION_TIME >= VISION_INTERVAL:
        hazards = detect_hazards(frame)
        LAST_VISION_TIME = now
    else:
        hazards = {}  # do not re-run perception

    perception = {
        "person": hazards.get("person", False),
        "obstacle": hazards.get("obstacle", False),
        "emergency": False
    }

    # ---------- 3. USER INTENT ----------
    user_action = None
    ai_action = None
    user_text = None

    if latest_user_command:
        user_text = latest_user_command
        latest_user_command = None

        conversation_memory.append(f"User: {user_text}")
        conversation_memory = conversation_memory[-MAX_MEMORY:]

        # AI intent hint (optional)
        try:
            intent = suggest_intent(user_text)
            ai_action = Action[intent]
        except Exception:
            ai_action = None

        user_action = plan_action(user_text)

    # ---------- 4. ORCHESTRATOR ----------
    final_action, explanation = orchestrator.decide(
        perception,
        user_action=user_action,
        ai_action=ai_action
    )

    final_action = safety_filter(final_action)

    # ---------- 5. ACTION CHANGE ONLY ----------
    if final_action != last_action:
        print("ACTION:", final_action.value)
        last_action = final_action

        if explanation:
            voice.speak(explanation)
            print("ZunoBot:", explanation)
            last_spoken = explanation

    # ---------- 6. GEMINI (ONLY IF ASKED) ----------
    if user_text and any(
        k in user_text
        for k in ["see", "why", "explain", "help", "what"]
    ):
        print("[Gemini] Thinking...")

        context = "\n".join(conversation_memory)

        ai_text = ask_gemini(
            frame,
            f"{context}\nUser: {user_text}",
            perception
        )

        if ai_text and ai_text != last_ai_reply:
            voice.speak(ai_text)
            print("ZunoBot (Gemini):", ai_text)

            conversation_memory.append(f"ZunoBot: {ai_text}")
            conversation_memory = conversation_memory[-MAX_MEMORY:]
            last_ai_reply = ai_text

    # ---------- 7. LOOP THROTTLE ----------
    time.sleep(LOOP_DELAY)
