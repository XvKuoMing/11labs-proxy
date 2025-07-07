import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("HOST")
port = os.getenv("PORT")

client = ElevenLabs(
    base_url=f"https://{host}:{port}",
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

