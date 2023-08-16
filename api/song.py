#!/usr/bin/env python3

class Song:
    name = ''
    id = ''
    album = ''
    artist = ''
    album_cover = ''
    year_release_date = ''
    genres = []
    duration = ''
    origin = ''

    def __init__(self, name, id, album, artist, album_cover, year_release_date, genres, duration, origin):
        self.name = name
        self.id = id
        self.album = album
        self.artist = artist
        self.album_cover = album_cover
        self.year_release_date = year_release_date
        self.genres = genres
        self.duration = duration
        self.origin = origin
    
    def __str__(self):
        return f"Name: {self.name}\nID: {self.id}\nAlbum: {self.album}\nArtist: {self.artist}\nAlbum Cover: {self.album_cover}\nYear Release Date: {self.year_release_date}\nGenres: {', '.join(self.genres)}\nDuration: {self.duration}\nOrigin: {self.origin}"

    
