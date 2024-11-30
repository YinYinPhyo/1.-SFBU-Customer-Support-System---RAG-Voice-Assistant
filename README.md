# SFBU-Customer-Support-System---RAG-Voice-Assistant

A multimodal AI assistant that integrates document-based knowledge (RAG) with voice interaction capabilities. This application allows both text and voice interfaces to interact with documents.

## Features

- **Chat Interface**: Enables text-based interaction with your documents.
- **Voice Interface**: Supports speech-based interaction using wake word detection.
- **Document Management**: Provides options to manage various document sources, including:
  - PDF files
  - YouTube videos (with auto-transcription)
  - Web pages
- **RAG (Retrieval Augmented Generation)**: Facilitates smart querying of document content.
- **Text-to-Speech**: Generates natural voice responses.

## Prerequisites

- Python 3.9 or later
- FFmpeg (required for audio processing)
- Microphone and system audio support

## Installation

1. Clone the repository.

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
4. Edit the .env file to include your OpenAI API key:

    ```env
    OPENAI_API_KEY=your-api-key-here
    ```

## Usage

### Start the Application

1. Run the following command to start the application:

```bash
python3 run.py
```
2. Explore the application interfaces:

    - Chat: Interact via text.
    - Voice: Communicate using speech.
    - Sources: Manage and upload documents.

### Adding Documents
1. Navigate to the Sources page.
2. Upload documents using one of the supported methods:
    - Upload PDF files.
    - Provide YouTube URLs for transcription.
    - Enter web page URLs.

### Voice Interaction
1. Open the Voice page.
2. Use the configured wake word (default: "hey abc").
3. Speak your query.
4. Listen to the AI assistant's response.

### Chat Interaction
1. Open the Chat page.
2. Enter your question in the text input box.
3. View the AI’s response, generated based on your documents.

### Configuration

Adjust settings via environment variables or the settings interface:
- OPENAI_API_KEY: Your OpenAI API key.
- Wake word: Configurable (default is "hey abc").
- Voice settings: Includes energy threshold, pause duration, and more.
- Model settings: Configure Whisper model, text-to-speech voice, etc.

### Dependencies
- LangChain: For RAG implementation.
- OpenAI: For language models and embeddings.
- Whisper: For speech-to-text conversion.
- ChromaDB: For vector storage.
- Streamlit: For the web-based interface.
- PyAudio: For audio processing.
- FFmpeg: For handling media files.

### Sample Output
![alt text](<output1.png>)