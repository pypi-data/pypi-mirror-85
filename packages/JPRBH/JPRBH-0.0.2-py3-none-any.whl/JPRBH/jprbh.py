import asyncio
from create_table import create_table
from readfile import read
from get_albums import get_albums
from add_albums import add_albums

async def main():
    create_table()
    lines = read()
    searches = [line.rstrip().split('|') for line in lines]
    searches = [{"data": {"term": i[0], "country": "US", "media": "music", "entity": "album", "attribute": "artistTerm"}, "filters": i[1:]} for i in searches]
    albums = await get_albums(searches)
    add_albums(albums)

if __name__ == "__main__":
	asyncio.run(main())


