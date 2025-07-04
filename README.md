# ElevenLabs Proxy Server

A FastAPI-based proxy server that mimics ElevenLabs API endpoints, allowing you to use your own server as a proxy for ElevenLabs text-to-speech conversion.

## Features

- ✅ **Complete ElevenLabs API Coverage**: All 4 text-to-speech endpoints
  - `/v1/text-to-speech/{voice_id}` - Basic conversion
  - `/v1/text-to-speech/{voice_id}/with-timestamps` - With character-level timing
  - `/v1/text-to-speech/{voice_id}/stream` - Streaming audio
  - `/v1/text-to-speech/{voice_id}/stream/with-timestamps` - Streaming with timing
- ✅ **All ElevenLabs Parameters**: Voice settings, pronunciation dictionaries, seeds, etc.
- ✅ **All Output Formats**: MP3, PCM, μ-law, A-law, Opus (19 total formats)
- ✅ **Advanced Features**: Latency optimization, text normalization, language enforcement
- ✅ **Server-side API Key**: Clients don't need API keys
- ✅ **FastAPI with OpenAPI**: Automatic documentation and validation
- ✅ **Comprehensive Testing**: Full test suite included

## Setup

1. **Install dependencies:**
   ```bash
   pip install -e .
   ```

2. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   API_KEY=your_elevenlabs_api_key_here
   VOICE=your_default_voice_id
   MODEL=eleven_multilingual_v2
   ```

3. **Run the server:**
   ```bash
   python run_server.py
   ```
   
   Or manually with uvicorn:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Usage

### Original ElevenLabs API call:
```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb?output_format=mp3_44100_128" \
     -H "xi-api-key: your_api_key" \
     -H "Content-Type: application/json" \
     -d '{
  "text": "The first move is what sets everything in motion.",
  "model_id": "eleven_multilingual_v2"
}'
```

### Using your proxy:
```bash
curl -X POST "http://localhost:8000/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb?output_format=mp3_44100_128" \
     -H "Content-Type: application/json" \
     -d '{
  "text": "The first move is what sets everything in motion.",
  "model_id": "eleven_multilingual_v2"
}' \
     --output speech.mp3
```

### Python client example:
```python
import requests

url = "http://localhost:8000/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb"
params = {"output_format": "mp3_44100_128"}
payload = {
    "text": "Hello, world!",
    "model_id": "eleven_multilingual_v2"
}

response = requests.post(url, json=payload, params=params)
with open("speech.mp3", "wb") as f:
    f.write(response.content)
```

### Test the proxy:
```bash
# Basic tests
python proxy_test.py

# Comprehensive test suite (all endpoints and features)
python enhanced_proxy_test.py
```

## API Endpoints

### Text-to-Speech Endpoints
- `POST /v1/text-to-speech/{voice_id}` - Basic text-to-speech conversion
- `POST /v1/text-to-speech/{voice_id}/with-timestamps` - TTS with character-level timing
- `POST /v1/text-to-speech/{voice_id}/stream` - Streaming audio generation
- `POST /v1/text-to-speech/{voice_id}/stream/with-timestamps` - Streaming with timestamps

### Utility Endpoints
- `GET /` - Root endpoint with server info
- `GET /health` - Health check
- `GET /docs` - API documentation (Swagger UI)
- `GET /v1/text-to-speech/endpoints` - List all supported endpoints and formats

## Parameters

### Path Parameters
- **voice_id**: ElevenLabs voice ID

### Query Parameters
- **output_format**: Audio format (default: mp3_44100_128)
- **enable_logging**: Enable/disable logging (optional)
- **optimize_streaming_latency**: Latency optimization level 0-4 (optional)

### Request Body Parameters
- **text**: Text to convert to speech (required)
- **model_id**: ElevenLabs model ID (default: eleven_multilingual_v2)
- **language_code**: ISO 639-1 language code (optional)
- **voice_settings**: Voice settings object (optional)
  - **stability**: 0.0-1.0 (optional)
  - **similarity_boost**: 0.0-1.0 (optional)  
  - **style**: 0.0-1.0 (optional)
  - **use_speaker_boost**: boolean (optional)
- **pronunciation_dictionary_locators**: Array of pronunciation dictionaries (optional)
- **seed**: Random seed 0-4294967295 for deterministic output (optional)
- **previous_text**: Context from previous generation (optional)
- **next_text**: Context for next generation (optional)
- **previous_request_ids**: Array of previous request IDs for continuity (optional)
- **next_request_ids**: Array of next request IDs for continuity (optional)
- **use_pvc_as_ivc**: Use IVC instead of PVC voice version (optional)
- **apply_text_normalization**: "auto", "on", or "off" (optional)
- **apply_language_text_normalization**: Enable language-specific normalization (optional)

## Supported Output Formats

All ElevenLabs supported formats are available:

### MP3 Formats
- `mp3_22050_32`, `mp3_44100_32`, `mp3_44100_64`, `mp3_44100_96`, `mp3_44100_128`, `mp3_44100_192`

### PCM Formats  
- `pcm_8000`, `pcm_16000`, `pcm_22050`, `pcm_24000`, `pcm_44100`, `pcm_48000`

### μ-law and A-law Formats (commonly used for telephony)
- `ulaw_8000`, `alaw_8000`

### Opus Formats
- `opus_48000_32`, `opus_48000_64`, `opus_48000_96`, `opus_48000_128`, `opus_48000_192`

**Note:** Some formats require specific ElevenLabs subscription tiers:
- MP3 192kbps: Creator tier or above
- PCM 44.1kHz: Pro tier or above

## Benefits of Using a Proxy

1. **API Key Security**: Your ElevenLabs API key stays on your server
2. **Rate Limiting**: Implement your own rate limiting logic
3. **Logging**: Track usage and requests
4. **Caching**: Cache frequently requested audio (future feature)
5. **Custom Logic**: Add preprocessing or postprocessing of text/audio

## Development

- The server runs with auto-reload enabled for development
- Visit `http://localhost:8000/docs` for interactive API documentation
- Check `http://localhost:8000/health` to verify the server is running
