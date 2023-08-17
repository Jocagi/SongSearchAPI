from django.db import models

class Song(models.Model):
    query = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    song_id = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album_cover = models.URLField()
    year_release_date = models.CharField(max_length=4)
    genres = models.JSONField()
    duration = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)

    def __str__(self):
        return self.name
