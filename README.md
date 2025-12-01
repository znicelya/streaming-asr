# Real-Time Voice Activity Detection & Speech Recognition

A lightweight client-server system for real-time audio processing with voice activity detection (VAD) and automatic speech recognition (ASR). This project demonstrates a complete pipeline from browser-based audio recording to real-time speech transcription.

## ✨ Features

- **Browser-based Audio Capture**: Record audio directly in the browser using Web Audio API
- **Real-time Streaming**: Efficient WebSocket communication for low-latency audio transmission
- **Voice Activity Detection**: Server-side VAD to detect speech segments and reduce unnecessary processing
- **Speech Recognition**: Integrated ASR for real-time transcription
- **Modular Architecture**: Clean separation between client and server components

## 🏗️ System Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Browser   │    │  WebSocket  │    │     VAD     │    │     ASR     │
│   Client    │───▶│   Server    │───▶│  Detection  │───▶│   Engine    │
│  (React)    │    │ (Node.js)   │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                  │
  JavaScript         Audio Frames       Speech/Noise        Transcription
  Recording          Transmission        Detection           Result
```

## 🚀 Quick Start

### Prerequisites
- Modern browser with Web Audio API support
- Python 3.8+ (for ASR engine, if using Python-based solution)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/znicelya/streaming-asr.git
cd streaming-asr
```

2. **Install server dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

1. **Start the WebSocket server**
```bash
cd streaming-asr
python main.py
# Server runs on http://localhost:9871
```

2. **Open your browser and navigate to `http://localhost:9871`**
3. **Allow microphone permissions and start speaking**

## 🛠️ Technology Stack

### Frontend
- **Web Audio API** - Audio capture and processing
- **WebSocket** - Real-time communication

### Backend
- **WebSocket** - Real-time bidirectional communication
- **webrtcvad** - Voice activity detection
- **SenseVoiceSmall** - ASR engine


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [webrtcvad](https://github.com/wiseman/py-webrtcvad.git)

---

**Note**: This is a demonstration project. For production use, consider additional optimizations for scalability, security, and reliability.