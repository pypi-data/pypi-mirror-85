import sqlite3
from contextlib import closing

def oldest_album(artist_name):
    """
    oldest_album(artist_name): Return the name of the oldest album
    that the given artist has produced, and the release date.
    """
    with closing(sqlite3.connect("itunes.db")) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("""SELECT collectionName, releaseDate FROM albums WHERE artistName = ?""", (artist_name)).fetchall()
            return rows


def average_price(artist_name):
    """
    average_price(artist_name): Return the average price in USD for
    the artist's albums
    """
    with closing(sqlite3.connect("itunes.db")) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT collectionPrice FROM albums WHERE artistName = ?", (artist_name)).fetchall()
            return rows