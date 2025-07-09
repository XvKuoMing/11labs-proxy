from elevenlabs import ElevenLabs
import os
from dotenv import load_dotenv

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

correct_voice = client.voices.get("21m00Tcm4TlvDq8ikWAM")
print("correct_voice: ", correct_voice)

print("--------------------------------")
wrong_voice = client.voices.get("nova")
print("wrong_voice: ", wrong_voice)




