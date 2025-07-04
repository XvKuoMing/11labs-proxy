from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
from typing import Dict, Any
import os
import logging

logger = logging.getLogger(__name__)

debug = os.getenv("DEBUG", "false").lower() == "true"
if debug:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

load_dotenv()


api_key = os.getenv("API_KEY")
client = ElevenLabs(
    api_key=api_key
)

app = FastAPI(title="ElevenLabs Proxy", description="Proxy server for ElevenLabs API")


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

@app.post("/v1/text-to-speech/{voice_id}")
async def text_to_speech(voice_id: str, request: Dict[str, Any]):
    try:
        audio = client.text_to_speech.convert(
            voice_id=voice_id,
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
            media_type=media_type
        )
    except Exception as e:
        logger.error(f"Error converting text to speech: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/text-to-speech/{voice_id}/stream")
async def text_to_speech_stream(voice_id: str, request: Dict[str, Any]):
    try:
        audio_stream = client.text_to_speech.stream(
            voice_id=voice_id,
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
            media_type=media_type
        )
    except Exception as e:
        logger.error(f"Error converting text to speech: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
        log_level="debug" if debug else "info",
        workers=workers
    ) 
