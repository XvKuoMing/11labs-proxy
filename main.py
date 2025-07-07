from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from elevenlabs import ElevenLabs
from pydantic import BaseModel
import base64
import json
from dotenv import load_dotenv
from typing import Dict, Any, Generator, Optional
import os
import logging

logger = logging.getLogger(__name__)

# Configure logging with handler
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

debug = os.getenv("DEBUG", "false").lower() == "true"
if debug:
    logger.setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
    logging.getLogger().setLevel(logging.INFO)

load_dotenv()

# Debug environment variables
logger.debug("Environment variables loaded:")
logger.debug(f"HOST: {os.getenv('HOST')}")
logger.debug(f"PORT: {os.getenv('PORT')}")
logger.debug(f"API_KEY: {'***' + str(os.getenv('API_KEY'))[-4:] if os.getenv('API_KEY') else 'None'}")
logger.debug(f"VOICE: {os.getenv('VOICE', 'Not set')}")
logger.debug(f"MODEL: {os.getenv('MODEL', 'Not set')}")

api_key = os.getenv("API_KEY")
client = ElevenLabs(
    api_key=api_key
)

app = FastAPI(title="ElevenLabs Proxy", description="Proxy server for ElevenLabs API")

# Authentication dependencies
security = HTTPBearer()

async def verify_openai_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify OpenAI Bearer token authentication"""
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    if credentials.credentials != api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return credentials.credentials

async def verify_elevenlabs_auth(xi_api_key: Optional[str] = Header(None, alias="xi-api-key")):
    """Verify ElevenLabs xi-api-key header authentication"""
    if not api_key:
        raise HTTPException(status_code=500, detail="ElevenLabs API key not configured")
    
    if not xi_api_key or xi_api_key != api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return xi_api_key

AUDIO_FORMATS = [
    "mp3_22050_32",
    "mp3_44100_32",
    "mp3_44100_64",
    "mp3_44100_96",
    "mp3_44100_128",
    "mp3_44100_192",
    "pcm_8000",
    "pcm_16000",
    "pcm_22050",
    "pcm_24000",
    "pcm_44100",
    "pcm_48000",
    "ulaw_8000",
    "alaw_8000",
    "opus_48000_32",
    "opus_48000_64",
    "opus_48000_96",
    "opus_48000_128",
    "opus_48000_192",
]
def get_media_type_and_extension(output_format: str) -> tuple[str, str]:
    """Map output format to media type and file extension"""
    if output_format.startswith("mp3_"):
        return "audio/mpeg", "mp3"
    elif output_format.startswith("pcm_"):
        return "audio/wav", "wav"
    elif output_format.startswith("ulaw_") or output_format.startswith("alaw_"):
        return "audio/basic", "au"
    elif output_format.startswith("opus_"):
        return "audio/opus", "opus"
    else:
        raise ValueError(f"Invalid output format: {output_format}")

# ElevenLabs API

@app.post("/v1/text-to-speech/{voice_id}")
async def text_to_speech(voice_id: str, request: Dict[str, Any], auth: str = Depends(verify_elevenlabs_auth)):
    try:
        audio = client.text_to_speech.convert(
            voice_id=voice_id.strip("'\""),
            **request
        )
        
        # Get output format from request, default to mp3_44100_128
        output_format = request.get("output_format", "mp3_44100_128")
        try:
            media_type, extension = get_media_type_and_extension(output_format)
            logger.info(f"Output format: {output_format}, Media type: {media_type}, Extension: {extension}")
        except Exception as e:
            logger.error(f"Error getting media type and extension: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid output format: {output_format}")
        
        return StreamingResponse(
            audio,
            media_type=media_type,
            headers={
                "Connection": "close",  # Ensure connection closes after response
                "Cache-Control": "no-cache",
            }
        )
    except Exception as e:
        logger.error(f"Error converting text to speech: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/text-to-speech/{voice_id}/stream")
async def text_to_speech_stream(voice_id: str, request: Dict[str, Any], auth: str = Depends(verify_elevenlabs_auth)):
    try:
        logger.debug(f"Received TTS request - Voice: '{voice_id}', Request: {request}")
        audio_stream = client.text_to_speech.stream(
            voice_id=voice_id.strip("'\""),
            **request
        )
        
        # Get output format from request, default to mp3_44100_128
        output_format = request.get("output_format", "mp3_44100_128")
        try:
            media_type, extension = get_media_type_and_extension(output_format)
            logger.info(f"Output format: {output_format}, Media type: {media_type}, Extension: {extension}")
        except Exception as e:
            logger.error(f"Error getting media type and extension: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid output format: {output_format}")
        
        return StreamingResponse(
            audio_stream,
            media_type=media_type,
            headers={
                "Connection": "close",  # Ensure connection closes after response
                "Cache-Control": "no-cache",
            }
        )
    except Exception as e:
        logger.error(f"Error converting text to speech: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# OpenAI API
class OpenaiT2SRequest(BaseModel):
    model: str
    input: str
    voice: str
    response_format: str
    instructions: str = None
    speed: float = 1.0
    stream_format: str = "audio" # or sse for streaming


@app.post("/v1/audio/speech")
async def audio_speech(request: OpenaiT2SRequest, auth: str = Depends(verify_openai_auth)):
    try:
        # Debug logging for voice parameter
        logger.debug(f"Received TTS request - Voice: '{request.voice}', Model: '{request.model}', Input length: {len(request.input)}")
        logger.debug(f"Response format: '{request.response_format}', Stream format: '{request.stream_format}'")
        
        if request.instructions:
            # ignore it for 11labs
            pass
        if request.stream_format == "audio": #
            voice_id = request.voice.strip("\"'")
            logger.info(f"Converting TTS with voice_id: '{voice_id}'")
            audio = client.text_to_speech.convert(
                voice_id=voice_id,
                text=request.input,
                model_id=request.model,
                output_format=request.response_format,
                voice_settings={
                    "speed": request.speed
                }
            )
            media_type, extension = get_media_type_and_extension(request.response_format)
            logger.info(f"Output format: {request.response_format}, Media type: {media_type}, Extension: {extension}")
            return StreamingResponse(
                audio,
                media_type=media_type,
                headers={
                    "Content-Disposition": f"attachment; filename=audio.{extension}",
                    "Connection": "close",  # Ensure connection closes after response
                    "Cache-Control": "no-cache",
                }
            )
        elif request.stream_format == "sse":
            def generate_sse_stream() -> Generator[str, None, None]:
                try:
                    voice_id = request.voice.strip("\"'")
                    logger.info(f"Streaming TTS with voice_id: '{voice_id}'")
                    audio_stream = client.text_to_speech.stream(
                        voice_id=voice_id,
                        text=request.input,
                        model_id=request.model,
                        output_format=request.response_format,
                        voice_settings={
                            "speed": request.speed
                        }
                    )
                    
                    # Stream audio chunks
                    for audio_chunk in audio_stream:
                        sse_chunk = {
                            "type": "speech.audio.delta",
                            "audio": base64.b64encode(audio_chunk).decode("utf-8")
                        }
                        yield f"data: {json.dumps(sse_chunk)}\n\n"
                    
                    # Send completion event
                    audio_done = {
                        "type": "speech.audio.done",
                        "usage": {
                            "input_tokens": 0,
                            "output_tokens": 0,
                            "total_tokens": 0
                        }
                    }
                    yield f"data: {json.dumps(audio_done)}\n\n"
                    
                except Exception as e:
                    error_event = {
                        "type": "error",
                        "error": {
                            "message": str(e),
                            "type": "server_error"
                        }
                    }
                    yield f"data: {json.dumps(error_event)}\n\n"
            
            return StreamingResponse(
                generate_sse_stream(), 
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no"  # Disable nginx buffering
                })
        else:
            raise HTTPException(status_code=400, detail=f"Invalid stream format: {request.stream_format}")
    except Exception as e:
        logger.error(f"Error converting text to speech: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Proxy API

@app.get("/")
async def root():
    return {"message": "ElevenLabs Proxy Server", "status": "running"}

@app.get("/ping")
async def ping():
    return {"ping": "pong"}


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))
    workers = int(os.getenv("WORKERS", "1"))
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Auto-reload on code changes
        # log_level="debug" if debug else "info",
        workers=workers
    ) 
