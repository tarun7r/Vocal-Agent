# Real-Time Cascading Speech-to-Speech Chatbot 🤖

A real-time cascading speech-to-speech chatbot that combines advanced speech recognition, AI reasoning, and neural text-to-speech capabilities. Built for seamless voice interactions with web integration and extensible tool system.

## ✨ Features

- 🎙️ **Real-time Speech Recognition** - Powered by Whisper + Silero VAD for accurate voice input
- 🤖 **Intelligent AI Reasoning** - Multimodal reasoning with Llama 3.1 8B through Agno agent
- 🌐 **Web Integration** - Access to Google Search, Wikipedia, and Arxiv for real-time information
- 🗣️ **Natural Voice Synthesis** - High-quality voice output using Kokoro-82M ONNX
- ⚡ **Low-latency Processing** - Optimized audio pipeline for responsive interactions
- 🔧 **Extensible Tool System** - Easy to add new capabilities to the agent
- 🛠️ **Cross-platform Support** - Works on macOS, Linux, and Windows

## 🛠️ Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| **Speech-to-Text** | Whisper (large-v1) + Silero VAD | Real-time transcription with voice activity detection |
| **Language Model** | Llama 3.1 8B via Ollama | Local AI reasoning and conversation |
| **Text-to-Speech** | Kokoro-82M ONNX | Natural voice synthesis |
| **Agent Framework** | Agno LLM Agent | Extensible tool-calling capabilities |
| **Audio Processing** | SoundDevice + SoundFile | Real-time audio I/O |

## 📋 Prerequisites

- **Python 3.9+**
- **Ollama** - Local LLM server
- **espeak-ng** - Text-to-speech engine
- **Microphone and Speakers** - For voice interaction

## 🚀 Quick Start

### 1. Install Ollama

**macOS:**
```bash
# Download from https://ollama.com/download/mac
# Or use Homebrew
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
- Download from [Ollama Windows download page](https://ollama.com/download/windows)

### 2. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/tarun7r/Vocal-Agent.git
cd Vocal-Agent

# Install Python dependencies
pip install -r requirements.txt

# Install Kokoro TTS (separate installation)
pip install --no-deps kokoro-onnx==0.4.7
```

### 3. Install System Dependencies

**macOS:**
```bash
brew install espeak-ng
```

**Linux:**
```bash
sudo apt-get install espeak-ng
```

**Windows:**
1. Visit [eSpeak NG Releases](https://github.com/espeak-ng/espeak-ng/releases)
2. Download the latest `.msi` file (e.g., `espeak-ng-20191129-b702b03-x64.msi`)
3. Run the installer
4. Add to PATH if needed

### 4. Download Models

**Llama 3.1 8B:**
```bash
ollama pull llama3.1:8b
```

**Kokoro TTS Models:**
- Download `kokoro-v1.0.onnx` and `voices-v1.0.bin` from [kokoro-onnx releases](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0)
- Place them in the project root directory

### 5. Run the Application

**Start Ollama:**
```bash
ollama serve
```

**In a new terminal, run the agent:**
```bash
python main.py
```

## 🎯 Usage

1. **Start the application** - Run `python main.py`
2. **Wait for initialization** - The system will load models and start listening
3. **Speak naturally** - Ask questions, request information, or have conversations
4. **Listen to responses** - The AI will respond with synthesized speech

### Example Interaction Flow:

```
Listening... Press Ctrl+C to exit ⠋
speak now - Recording started ⠸
recording - Recording stopped

Transcribed: Who won the 2022 FIFA World Cup?
LLM Tool calls...

Response from the knowledge agent: The 2022 FIFA World Cup was won by Argentina, led by Lionel Messi. They defeated France in the final on December 18, 2022.

[Audio starts playing]
```

![Vocal Agent Demo](demo.png)

## ⚙️ Configuration

Key settings in `main.py`:

```python
# Audio processing
SAMPLE_RATE = 16000
MAX_PHONEME_LENGTH = 500

# Voice synthesis
SPEED = 1.2  # Adjust speech rate (0.5-2.0)
VOICE_PROFILE = "af_heart"  # Choose from voices-v1.0.bin

# Agent settings
MAX_THREADS = 2  # Parallel processing threads
```

### Available Voice Profiles

The `voices-v1.0.bin` file contains multiple voice profiles. You can change the `VOICE_PROFILE` setting to use different voices.

## 📁 Project Structure

```
Vocal-Agent/
├── main.py                 # Core application logic
├── agent_client.py         # LLM agent integration
├── kokoro-v1.0.onnx       # TTS model file
├── voices-v1.0.bin        # Voice profiles
├── requirements.txt        # Python dependencies
├── vocal_agent_mac.sh     # macOS setup script
├── demo.png               # Demo screenshot
└── README.md              # This file
```

## macOS Setup Script

For macOS users, we provide an automated setup script:

```bash
# Make the script executable
chmod +x vocal_agent_mac.sh

# Run the setup script
./vocal_agent_mac.sh
```

The script will:
- Install Homebrew dependencies
- Download Kokoro models
- Set up the environment
- Start Ollama service
- Launch the application


### Performance Tips

- Use a GPU for faster LLM inference
- Adjust `MAX_THREADS` based on your CPU cores
- Modify `SPEED` setting for preferred speech rate
- Close other audio applications to avoid conflicts


### Adding New Tools

The agent uses the Agno framework, which supports extensible tool calling. To add new capabilities:

1. Check the [Agno Toolkits documentation](https://docs.agno.com/tools/toolkits/toolkits)
2. Implement your tool following the Agno framework
3. Register the tool with the agent in `agent_client.py`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **[RealtimeSTT](https://github.com/KoljaB/RealtimeSTT)** - Real-time speech recognition and VAD
- **[Kokoro-ONNX](https://github.com/thewh1teagle/kokoro-onnx)** - Efficient text-to-speech synthesis
- **[Agno](https://docs.agno.com/introduction)** - LLM agent framework
- **[Ollama](https://ollama.ai/)** - Local LLM serving
- **[Weebo](https://github.com/amanvirparhar/weebo)** - Project inspiration


---

**Made with ❤️ for the open-source community**

