import asyncio
from JPRBH.initialize import initialize
from JPRBH.functions import oldest_album, average_price

async def main():
    await initialize()

if __name__ == "__main__":
	asyncio.run(main())

