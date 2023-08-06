import sqlite3
from contextlib import closing

default = {
	'artistId':0,
	'collectionId':0,
	'amgArtistId':0,
	'artistName':'',
	'collectionName':'',
	'collectionCensoredName':'',
	'artistViewUrl':'',
	'collectionViewUrl':'',
	'artworkUrl60':'',
	'artworkUrl100':'',
	'collectionPrice':0.00,
	'collectionExplicitness':'',
	'trackCount':0,
	'copyright':'',
	'country':'US',
	'currency':'USD',
	'releaseDate':'',
	'primaryGenreName':''
}

def add_albums(albums):
	with closing(sqlite3.connect("itunes.db")) as connection:
		with closing(connection.cursor()) as cursor:
			for album in albums:
				missing_keys = list(set(default.keys()).difference(album.keys()))
				for missing_key in missing_keys:
					album[missing_key] = default[missing_key]
				sql = """INSERT INTO albums VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
				row = (album['artistId'],
					album['collectionId'],
					album['amgArtistId'],
					album['artistName'],
					album['collectionName'],
					album['collectionCensoredName'],
					album['artistViewUrl'],
					album['collectionViewUrl'],
					album['artworkUrl60'],
					album['artworkUrl100'],
					album['collectionPrice'],
					album['collectionExplicitness'],
					album['trackCount'],
					album['copyright'],
					album['country'],
					album['currency'],
					album['releaseDate'],
					album['primaryGenreName'])
				try:
					cursor.execute(sql,row)
				except Exception as err:
					print(err)
		connection.commit()