import time
import threading
from threading import Thread
import speech_recognition as sr

from src.services.ai import ask_ai

# ---------- Speech Setup ----------
r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    print("🎤 Calibrating microphone...")
    r.adjust_for_ambient_noise(source, duration=1.0)
    r.dynamic_energy_threshold = True
    r.energy_threshold = 300
    r.pause_threshold = 2.0
    r.phrase_threshold = 0.15
    r.non_speaking_duration = 0.25

print("✅ Mic Ready!")

# ---------- Runtime State ----------
is_listening = False
is_processing = False
last_text = ""
listen_thread = None


def continuous_listen(callback):
    global is_listening, is_processing, last_text

    print("🎤 Continuous listening started")

    with mic as source:
        while True:
            try:
                if not is_listening:
                    time.sleep(0.10)
                    continue

                audio = r.listen(source, timeout=None, phrase_time_limit=15)
                raw = audio.get_raw_data()
                if len(raw) < 700:
                    continue

                text = r.recognize_google(audio).strip()
                if not text or text == last_text:
                    continue

                print(f"🗣 Heard: {text}")
                last_text = text

                def worker():
                    global is_processing
                    if is_processing:
                        return

                    is_processing = True
                    if callback:
                        callback(text, "⏳ Thinking...")
                    reply = ask_ai(text)
                    if callback:
                        callback(text, reply)
                    is_processing = False

                threading.Thread(target=worker, daemon=True).start()

            except sr.UnknownValueError:
                continue
            except Exception as e:
                print(f"⚠️ Mic Error: {e}")


def start_auto_listening(callback=None):
    global listen_thread, is_listening

    if listen_thread is None:
        listen_thread = Thread(
            target=continuous_listen,
            args=(callback,),
            daemon=True
        )
        listen_thread.start()

    is_listening = True
    print("🎤 Listening ON")


def stop_auto_listening():
    global is_listening
    is_listening = False
    print("🔇 Listening OFF")
