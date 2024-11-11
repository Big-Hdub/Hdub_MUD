import asyncio
from app.app import create_app

async def main():
    global app
    app = await create_app('production')

asyncio.run(main())
