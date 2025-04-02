# Real-Time Speech-to-Speech Chatbot 🤖

A cutting-edge voice assistant combining state-of-the-art speech recognition, AI reasoning, and neural text-to-speech capabilities. Built with real-time interaction in mind.

## Features ✨

- 🎙️ Real-time speech recognition using Whisper + Silero VAD
- 🤖 Multimodal reasoning with Llama 3.1 8B through Agno agent
- 🌐 Web integration (Google Search, Wikipedia, Arxiv)
- 🗣️ Natural voice synthesis with Kokoro-82M ONNX
- ⚡ Low-latency audio processing pipeline
- 🔧 Extensible tool system for agent capabilities

## Tech Stack 🛠️

| Component              | Technology                          |
|------------------------|-------------------------------------|
| Speech-to-Text         | Whisper (large-v1) + Silero VAD     |
| Language Model         | Llama 3.1 8B via Ollama             |
| Text-to-Speech         | Kokoro-82M ONNX                     |
| Agent Framework        | Agno LLM Agent                      |


## Installation 📦

### Prerequisites
- Python 3.9+
- [Ollama](https://ollama.com/) running locally

```bash
# Clone repository
git clone https://github.com/tarun7r/Vocal-Agent.git

# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies 
sudo apt-get install espeak-ng

# For Mac users
brew install espeak-ng
```

## Models Setup 🧠

### Llama 3.1 8B:
```bash
ollama pull llama3.1:8b
```

### Kokoro Models:
Download from [kokoro-onnx releases](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0):
- kokoro-v1.0.onnx
- voices-v1.0.bin

Place in project root directory

## Usage 🚀

Start Ollama service:
```bash
ollama serve

ollama run llama3.1:8b
```

In a separate terminal:
```bash
python3 main.py
```

### Flow after running `main.py`:
```plaintext
Listening... Press Ctrl+C to exit ⠋
speak now - Recording started ⠸
recording - Recording stopped

Transcribed: Who won the 2022 FIFA World Cup?
LLM Tool calls...

Response from the knowledge agent: The 2022 FIFA World Cup was won by Argentina, led by Lionel Messi. They defeated France in the final on December 18, 2022.

[Audio starts playing]
```

## Configuration ⚙️

Key settings in main.py:
```python
# Audio processing
SAMPLE_RATE = 16000
MAX_PHONEME_LENGTH = 500

# Voice synthesis
SPEED = 1.2  # Adjust speech rate
VOICE_PROFILE = "af_heart"  # Choose from voices-v1.0.bin

# Agent settings
MAX_THREADS = 2  # Parallel processing threads
```


## Project Structure 📂
```
.
├── main.py               # Core application logic
├── agent_client.py       # LLM agent integration
├── kokoro-v1.0.onnx      # TTS model
├── voices-v1.0.bin       # Voice profiles
├── requirements.txt      # Python dependencies
└── README.md
```


## License 📄

MIT License - See [LICENSE](https://github.com/tarun7r/Vocal-Agent/blob/main/LICENSE) for details

## Acknowledgements 

- [RealtimeSTT](https://github.com/KoljaB/RealtimeSTT) for STS + VAD integration
- [Kokoro-ONNX](https://github.com/thewh1teagle/kokoro-onnx) for efficient TTS
- [Agno](https://docs.agno.com/introduction) for agent framework
- [Ollama](https://ollama.ai/) for local LLM serving
- Project inspiration from - [Weebo](https://github.com/amanvirparhar/weebo)
- You can add more tools to the agent - [Agno Toolkits](https://docs.agno.com/tools/toolkits/toolkits)
