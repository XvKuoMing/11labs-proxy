import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from dotenv import load_dotenv

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("API_KEY")
)

text = "Здравствуйте! Спасибо, что обратились в компанию Водовоз! Я ваш ассистент. Как я могу вам помочь?"

audio = client.text_to_speech.convert(
    text=text,
    voice_id=os.getenv("VOICE"),
    model_id=os.getenv("MODEL"),
    output_format="mp3_44100_128"
)

play(audio)



# from elevenlabs import stream
# from elevenlabs.client import ElevenLabs

# client = ElevenLabs()

# audio_stream = client.text_to_speech.stream(
#     text="This is a test",
#     voice_id="JBFqnCBsd6RMkjVDRZzb",
#     model_id="eleven_multilingual_v2"
# )

# # option 1: play the streamed audio locally
# stream(audio_stream)

# # option 2: process the audio bytes manually
# for chunk in audio_stream:
#     if isinstance(chunk, bytes):
#         print(chunk)
