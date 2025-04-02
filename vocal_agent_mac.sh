#!/bin/bash

# Vocal-Agent Setup and Run Script for macOS with Virtual Environment

# Function to display error messages
function error_exit {
    echo "$1" 1>&2
    exit 1
}

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    error_exit "Homebrew is not installed. Please install Homebrew first: https://brew.sh/"
fi

# Install espeak-ng if not installed
if ! brew list espeak-ng &> /dev/null; then
    echo "Installing espeak-ng..."
    brew install espeak-ng || error_exit "Failed to install espeak-ng."
fi

if ! command -v ollama &> /dev/null; then
    error_exit "Ollama is not installed. Please install Ollama first: https://ollama.com/download/mac"
fi

# Clone the repository if not already cloned
if [ ! -d "Vocal-Agent" ]; then
    echo "Cloning Vocal-Agent repository..."
    git clone https://github.com/tarun7r/Vocal-Agent.git || error_exit "Failed to clone repository."
fi

cd Vocal-Agent || error_exit "Failed to navigate to Vocal-Agent directory."

# Create a Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating a Python virtual environment..."
    python3 -m venv venv || error_exit "Failed to create virtual environment."
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate || error_exit "Failed to activate virtual environment."


# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install --upgrade --no-deps -r requirements.txt || error_exit "Failed to install Python dependencies."



# Download Kokoro models if not already downloaded
if [ ! -f "kokoro-v1.0.onnx" ] || [ ! -f "voices-v1.0.bin" ]; then
    echo "Downloading Kokoro models..."
    curl -L -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx || error_exit "Failed to download kokoro-v1.0.onnx."
    curl -L -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin || error_exit "Failed to download voices-v1.0.bin."
fi

# Open a new terminal for Ollama service
echo "Starting Ollama service in a new terminal..."
osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && source venv/bin/activate && ollama run llama3.1:8b"'

# Wait for Ollama service to start
sleep 5

# Open a new terminal for the main application
echo "Running Vocal-Agent in a new terminal..."
osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && source venv/bin/activate && python3 main.py"'

echo "Setup complete. Check the new terminal windows for the running services."