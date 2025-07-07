from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
import json
import base64

load_dotenv()

host = os.getenv("HOST")
port = os.getenv("PORT")

client = OpenAI(
    base_url=f"http://{host}:{port}/v1",
    api_key=os.getenv("API_KEY")
)


# Test 1: Non-streaming (working)
print("Testing non-streaming audio generation...")
speech_file_path = Path(__file__).parent / "strea_speech_raw_audio.mp3"
with client.audio.speech.with_streaming_response.create(
  model=os.getenv("MODEL"),
  voice=os.getenv("VOICE"),
  input="Здравствуйте! Спасибо, что обратились в компанию Водовоз! Я ваш ассистент. Как я могу вам помочь?",
  response_format="mp3_44100_128"
) as response:
  # response.stream_to_file(speech_file_path)
  with open(speech_file_path, "wb") as f:
    for chunk in response.iter_bytes():
      f.write(chunk)

print(f"✓ Non-streaming audio saved to {speech_file_path}")


# Test 2: SSE streaming with proper parsing
print("\nTesting SSE streaming audio generation...")
speech_file_path = Path(__file__).parent / "stream_speech_sse.mp3"

with client.audio.speech.with_streaming_response.create(
  model=os.getenv("MODEL"),
  voice=os.getenv("VOICE"),
  input="Здравствуйте! Спасибо, что обратились в компанию Водовоз! Я ваш ассистент. Как я могу вам помочь?",
  response_format="mp3_44100_128",
  stream_format="sse"
) as response:
  # When using SSE, we need to parse the Server-Sent Events
  with open(speech_file_path, "wb") as f:
    buffer = b""
    for chunk in response.iter_bytes():
      buffer += chunk
      
      # Process complete lines
      while b'\n' in buffer:
        line, buffer = buffer.split(b'\n', 1)
        line = line.decode('utf-8').strip()
        
        # Parse SSE data lines
        if line.startswith('data: '):
          try:
            json_data = line[6:]  # Remove 'data: ' prefix
            event_data = json.loads(json_data)
            
            # Handle audio delta events
            if event_data.get("type") == "speech.audio.delta":
              audio_base64 = event_data.get("audio", "")
              if audio_base64:
                # Decode base64 audio data and write to file
                audio_bytes = base64.b64decode(audio_base64)
                f.write(audio_bytes)
                print(f"  Received audio chunk: {len(audio_bytes)} bytes")
            
            # Handle completion event
            elif event_data.get("type") == "speech.audio.done":
              print(f"  Audio generation completed!")
              usage = event_data.get("usage", {})
              print(f"  Usage: {usage}")
              break
              
            # Handle error events
            elif event_data.get("type") == "error":
              error = event_data.get("error", {})
              print(f"  Error: {error}")
              break
              
          except json.JSONDecodeError as e:
            print(f"  Failed to parse JSON: {e}")
            continue

print(f"✓ SSE streaming audio saved to {speech_file_path}")
print("\nBoth audio files should now be playable!")
