# ElevenLabs Proxy Server

A high-performance FastAPI-based proxy server for the ElevenLabs text-to-speech API. This proxy provides a simple interface for converting text to speech with support for multiple audio formats and streaming capabilities.

## 🚀 Features

- **FastAPI Framework**: High-performance async API server
- **Multiple Audio Formats**: Support for MP3, PCM, ULAW, ALAW, and OPUS formats
- **Streaming Support**: Real-time audio streaming capabilities
- **Docker Ready**: Containerized deployment with Docker Compose
- **Health Checks**: Built-in health monitoring endpoints
- **Environment Configuration**: Flexible configuration via environment variables
- **Production Ready**: Non-root user execution and security best practices

## 📋 Supported Audio Formats

- **MP3**: `mp3_22050_32`, `mp3_44100_32`, `mp3_44100_64`, `mp3_44100_96`, `mp3_44100_128`, `mp3_44100_192`
- **PCM**: `pcm_8000`, `pcm_16000`, `pcm_22050`, `pcm_24000`, `pcm_44100`, `pcm_48000`
- **ULAW/ALAW**: `ulaw_8000`, `alaw_8000`
- **OPUS**: `opus_48000_32`, `opus_48000_64`, `opus_48000_96`, `opus_48000_128`, `opus_48000_192`

## 🛠️ Setup

### Prerequisites

- Python 3.11+
- ElevenLabs API key
- Docker (optional, for containerized deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd 11px
   ```

2. **Install dependencies with UV** (recommended)
   ```bash
   pip install uv
   uv sync
   ```

   Or with pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   API_KEY=your_elevenlabs_api_key
   HOST=0.0.0.0
   PORT=8000
   WORKERS=1
   DEBUG=false
   ```

4. **Run the server**
   ```bash
   python main.py
   ```

### Docker Deployment

1. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Check health**
   ```bash
   curl http://localhost:8000/ping
   ```

## 📚 API Usage

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Health Check
```bash
GET /ping
```
Returns: `{"ping": "pong"}`

#### Text to Speech
```bash
POST /v1/text-to-speech/{voice_id}
```

**Request Body:**
```json
{
  "text": "Hello, world!",
  "output_format": "mp3_44100_128",
  "model_id": "eleven_multilingual_v2"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/v1/text-to-speech/YOUR_VOICE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test message.",
    "output_format": "mp3_44100_128"
  }' \
  --output audio.mp3
```

#### Streaming Text to Speech
```bash
POST /v1/text-to-speech/{voice_id}/stream
```

Same request format as above, but returns a streaming response for real-time audio playback.

### Parameters

- `voice_id`: ElevenLabs voice ID
- `text`: Text to convert to speech
- `output_format`: Audio format (see supported formats above)
- `model_id`: ElevenLabs model ID (optional)

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | ElevenLabs API key | Required |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `WORKERS` | Number of worker processes | `1` |
| `DEBUG` | Enable debug logging | `false` |

## 🐳 Docker Configuration

The application includes:
- **Multi-stage build** for optimized image size
- **Non-root user** for security
- **Health checks** for monitoring
- **UV package manager** for faster dependency installation
- **Network host mode** for optimal performance

## 🧪 Testing

Run the test suite:
```bash
python test.py
```

## 📝 Logging

The application includes structured logging with configurable levels:
- Production: INFO level
- Development: DEBUG level (set `DEBUG=true`)

## 🔒 Security Features

- Non-root container execution
- Environment-based configuration
- Input validation for audio formats
- Error handling with appropriate HTTP status codes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🆘 Support

For issues and questions:
1. Check the [Issues](../../issues) page
2. Review the ElevenLabs API documentation
3. Ensure your API key is valid and has sufficient credits
