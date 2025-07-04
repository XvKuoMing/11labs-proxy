import httpx
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("HOST")
port = os.getenv("PORT")

client = httpx.Client(base_url=f"http://{host}:{port}")

async def ping():
    response = await client.get("/ping")
    print(response.json())

if __name__ == "__main__":
    import asyncio
    asyncio.run(ping())
