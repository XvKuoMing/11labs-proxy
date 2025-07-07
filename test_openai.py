from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

host = os.getenv("HOST")
port = os.getenv("PORT")

client = OpenAI(
    base_url=f"http://{host}:{port}/v1",
    api_key=os.getenv("API_KEY")
)


# audio = client.audio.speech.create(
#     model=os.getenv("MODEL"),
#     input="Здравствуйте! Спасибо, что обратились в компанию Водовоз! Я ваш ассистент. Как я могу вам помочь?",
#     voice=os.getenv("VOICE"),
#     response_format="mp3_44100_128"
# )

speech_file_path = Path(__file__).parent / "speech.mp3"
with client.audio.speech.with_streaming_response.create(
  model=os.getenv("MODEL"),
  voice=os.getenv("VOICE"),
  input="Здравствуйте! Спасибо, что обратились в компанию Водовоз! Я ваш ассистент. Как я могу вам помочь?"
) as response:
  response.stream_to_file(speech_file_path)

