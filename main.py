import numpy as np
import sounddevice as sd
import soundfile as sf
import signal
from threading import Event
from concurrent.futures import ThreadPoolExecutor
from RealtimeSTT import AudioToTextRecorder
from agent_client import knowledge_agent_client
from kokoro_onnx import Kokoro
from misaki import en, espeak

# Configuration constants
SAMPLE_RATE = 16000  # Matches RealtimeSTT's expected input
MAX_PHONEME_LENGTH = 500
SPEED = 1.2
MAX_THREADS = 2

# Global variables
stt_recorder = None
executor = None
shutdown_event = Event()
fallback = None
g2p = None
kokoro = None

def setup_signal_handler():
    signal.signal(signal.SIGINT, lambda signum, frame: shutdown_event.set())

def initialize_models():
    global fallback, g2p, kokoro, stt_recorder
    
    # Initialize TTS
    fallback = espeak.EspeakFallback(british=False)
    g2p = en.G2P(trf=False, british=False, fallback=fallback)
    kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
    
    print("TTS and voice models initialized.")
    
    # Initialize RealtimeSTT with proper configuration
    stt_recorder = AudioToTextRecorder(
        model="large-v1",
        language="en",
        use_microphone=True,
        on_recording_start=lambda: print(" - Recording started"),
        on_recording_stop=lambda: print(" - Recording stopped"),
        device="cpu",
        realtime_model_type="large-v1",
    )

def process_audio_stream():
    def audio_callback(indata, frames, time_info, status):
        if shutdown_event.is_set():
            raise sd.CallbackStop()
        stt_recorder.feed_audio(indata)  # Feed audio to recorder

    with sd.InputStream(
        callback=audio_callback,
        channels=1,
        samplerate=SAMPLE_RATE,
        dtype=np.int16  # Matches RealtimeSTT's requirements
    ):
        print("Listening... Press Ctrl+C to exit")
        while not shutdown_event.is_set():
            # Get transcription result
            text = stt_recorder.text()
            if text:
                print(f"Transcribed: {text}")
                create_and_play_response(text)
            sd.sleep(100)

def create_and_play_response(prompt: str):
    if shutdown_event.is_set():
        return

    try:
        agent_response = knowledge_agent_client(prompt)
        print(f"Response from the knowldege agent: {agent_response}")
        phonemes, _ = g2p(agent_response)
        samples, sample_rate = kokoro.create(phonemes, "af_heart", is_phonemes=True)
        
        # Play audio using OutputStream
        if not shutdown_event.is_set():
            with sd.OutputStream(
                samplerate=sample_rate,
                channels=1,
                dtype=np.float32
            ) as out_stream:
                # Reshape samples for output stream format
                audio_data = samples.astype(np.float32)
                if len(audio_data) > 0:
                    out_stream.write(audio_data.reshape(-1, 1))
                    # Wait for playback to complete
                    sd.sleep(int(1000 * len(audio_data) / sample_rate))
    except Exception as e:
        print(f"Error in create_and_play_response: {str(e)}")
        return

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
        print("Exiting...")

if __name__ == "__main__":
    main()