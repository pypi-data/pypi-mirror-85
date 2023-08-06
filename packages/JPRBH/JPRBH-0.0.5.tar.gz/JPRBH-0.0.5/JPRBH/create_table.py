import sqlite3
from contextlib import closing

def create_table():
	with closing(sqlite3.connect("itunes.db")) as connection:
		with closing(connection.cursor()) as cursor:
			cursor.execute("""CREATE TABLE IF NOT EXISTS albums (
				artistId INTEGER,
				collectionId INTEGER PRIMARY KEY UNIQUE NOT NULL,
				amgArtistId INTEGER,
				artistName TEXT,
				collectionName TEXT,
				collectionCensoredName TEXT,
				artistViewUrl TEXT,
				collectionViewUrl TEXT,
				artworkUrl60 TEXT,
				artworkUrl100 TEXT,
				collectionPrice REAL DEFAULT 0,
				collectionExplicitness TEXT,
				trackCount INTEGER,
				copyright TEXT,
				country TEXT,
				currency TEXT,
				releaseDate TEXT,
				primaryGenreName TEXT
				)""")

def main():
	create_table()

if __name__ == "__main__":
	main()

