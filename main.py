import numpy as np
import sounddevice as sd
import signal
import threading
from concurrent.futures import ThreadPoolExecutor
from RealtimeSTT import AudioToTextRecorder
from agent_client import knowledge_agent_client
from kokoro_onnx import Kokoro
from misaki import en, espeak

# Configuration Constants
SAMPLE_RATE = 16000
MAX_THREADS = 2

# Global Variables
stt_recorder = None
executor = None
shutdown_event = threading.Event()
tts_lock = threading.Lock()
is_playing = threading.Event()

# Speech Processing Models
fallback = None
g2p = None
kokoro = None

def setup_signal_handler():
    signal.signal(signal.SIGINT, lambda s, f: shutdown_event.set())

def initialize_models():
    global fallback, g2p, kokoro, stt_recorder
    
    # Initialize TTS and STT Models
    fallback = espeak.EspeakFallback(british=False)
    g2p = en.G2P(trf=False, british=False, fallback=fallback)
    kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
    print("🎙️ TTS and STT models initialized.")
    
    stt_recorder = AudioToTextRecorder(
        model="large-v1",
        language="en",
        use_microphone=True,
        on_recording_start=lambda: print(" - 🎤 Recording started"),
        on_recording_stop=lambda: print(" - 🛑 Recording stopped"),
        device="cuda",
        realtime_model_type="large-v1"
    )

def process_audio_stream():
    def audio_callback(indata, frames, time_info, status):
        if shutdown_event.is_set() or is_playing.is_set():
            return
        stt_recorder.feed_audio(indata)
    
    with sd.InputStream(
        callback=audio_callback,
        channels=1,
        samplerate=SAMPLE_RATE,
        dtype=np.int16
    ):
        print("🎧 Listening... Press Ctrl+C to exit")
        while not shutdown_event.is_set():
            if not is_playing.is_set():
                text = stt_recorder.text()
                if text:
                    print(f"📝 Transcribed: {text}")
                    executor.submit(create_and_play_response, text)
            sd.sleep(100)

def create_and_play_response(prompt):
    with tts_lock:
        if shutdown_event.is_set():
            return
        
        is_playing.set()  # Pause STT to prevent feedback loop
        try:
            agent_response = knowledge_agent_client(prompt)
            print(f"🤖 Response: {agent_response}")
            phonemes, _ = g2p(agent_response)
            samples, sample_rate = kokoro.create(phonemes, "af_heart", is_phonemes=True)
            audio_data = samples.astype(np.float32)
            if len(audio_data) > 0:
                sd.play(audio_data.reshape(-1, 1), sample_rate)
                sd.wait()
        except Exception as e:
            print(f"❌ Error in TTS: {str(e)}")
        finally:
            is_playing.clear()  # Resume STT after TTS playback

def main():
    global executor
    setup_signal_handler()
    initialize_models()
    executor = ThreadPoolExecutor(max_workers=MAX_THREADS)
    try:
        with stt_recorder:
            process_audio_stream()
    finally:
        shutdown_event.set()
        executor.shutdown(wait=True)
        print("👋 Exiting...")

if __name__ == "__main__":
    main()