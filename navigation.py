from Brain.orchestrator import Orchestrator
from Brain.planner import plan_action
from Brain.safety import safety_filter
from Brain.vision_fast import detect_hazards
from Brain.camera import capture_frame
from Brain.voice import VoiceEngine
from Brain.voice_input import VoiceInput
from Brain.online_ai import ask_gemini, suggest_intent
from Brain.actions import Action

# ---------------- INIT ----------------
orchestrator = Orchestrator(mode="personal_care")
voice = VoiceEngine()

last_spoken = None
last_ai_reply = None
latest_user_command = None

# Wake-word state
awake = False
WAKE_WORD = "hey zuno"

# Short-term conversation memory
conversation_memory = []
MAX_MEMORY = 5

print("ZunoBot Brain Running (Vision + Voice + Gemini)\n")

# ----------- VOICE INPUT CALLBACK -----------

def on_voice_text(text: str):
    global latest_user_command, awake

    text = text.lower().strip()
    print("Heard:", text)

    # Wake-word detection
    if WAKE_WORD in text:
        awake = True
        voice.speak("Yes, I am listening.")
        return

    # Only accept commands after wake-word
    if awake:
        latest_user_command = text


voice_input = VoiceInput(
    model_path="/home/pi/zunobot/models/vosk-model-small-en-us-0.15"
)
voice_input.on_text = on_voice_text
voice_input.start()

# ---------------- MAIN LOOP ----------------
while True:
    # 1?? FAST VISION (always running)
    frame = capture_frame()
    if frame is None:
        continue

    hazards = detect_hazards(frame)

    perception = {
        "person": hazards.get("person", False),
        "obstacle": hazards.get("obstacle", False),
        "emergency": False
    }

    # 2?? USER INTENT FROM VOICE (after wake-word)
    user_action = None
    ai_action = None
    user_text = None

    if latest_user_command:
        user_text = latest_user_command
        latest_user_command = None
        awake = False  # reset wake state after one command

        # ---- Conversation memory (user side) ----
        conversation_memory.append(f"User: {user_text}")
        conversation_memory = conversation_memory[-MAX_MEMORY:]

        # ---- Gemini intent suggestion (non-binding) ----
        try:
            intent_text = suggest_intent(user_text)
            ai_action = Action[intent_text]
        except Exception:
            ai_action = None

        # ---- Deterministic planner ----
        user_action = plan_action(user_text)

    # 3?? ORCHESTRATOR (final motion decision)
    final_action, explanation = orchestrator.decide(
        perception,
        user_action=user_action,
        ai_action=ai_action
    )

    final_action = safety_filter(final_action)

    print("ACTION:", final_action.value)

    # 4?? CARE VOICE (deterministic explanation)
    if explanation and explanation != last_spoken:
        voice.speak(explanation)
        print("ZunoBot:", explanation)
        last_spoken = explanation

    # 5?? GEMINI (only for explanation / vision / help)
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
            last_ai_reply = ai_text

            # ---- Conversation memory (bot side) ----
            conversation_memory.append(f"ZunoBot: {ai_text}")
            conversation_memory = conversation_memory[-MAX_MEMORY:]
