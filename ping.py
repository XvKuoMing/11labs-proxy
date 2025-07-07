import httpx
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("HOST")
port = os.getenv("PORT")

async def ping():
    async with httpx.AsyncClient(base_url=f"http://{host}:{port}") as client:
        response = await client.get("/ping")
        print(response.json())

if __name__ == "__main__":
    import asyncio
    asyncio.run(ping())
