import asyncio
import httpx
import re
from aiomultiprocess import Pool

url = 'https://itunes.apple.com/search'
ops = {
	'<=': (lambda a,b: a<=float(b)), 
	'>=': (lambda a,b: a>=float(b)), 
	'!=': (lambda a,b: a!=b if isinstance(a, str) else a!=float(b)), 
	'~': (lambda a,b: re.search(b, a)), 
	'<': (lambda a,b: a<float(b)), 
	'>': (lambda a,b: a>float(b)), 
	'=': (lambda a,b: a==b if isinstance(a, str) else a==float(b))
}

async def get(search):
	async with httpx.AsyncClient(timeout=None) as client:
		r = await client.post(url, data=search["data"])
		if r.status_code == 200:
			results = r.json()['results']
			results = [r for r in results if(r['wrapperType'] == 'collection' and r['collectionType'] == 'Album')]
			for filter in search["filters"]:
				op = next(ele for ele in ops.keys() if ele in filter)
				inputs = [i.strip() for i in filter.split(op)]
				if inputs[0] == 'contentAdvisoryRating':
					inputs[0] = 'collectionExplicitness'
					inputs[1] = 'explicit'
				results = [r for r in results if(ops[op](r[inputs[0]], inputs[1]))]
			return results
		else:
			print('ERROR! Search: ' + str(search))


async def search(searches):
	albums = []
	async with Pool() as pool:
		async for result in pool.map(get, searches):
			albums.extend(result)
	return albums

async def get_albums(searches):
	albums = await search(searches)
	return albums
