import requests
import urllib.parse
from .song import SongWS

# Busca una cancion en la API de itunes
def search_itunes(song_name):
    # Se codifica el nombre de la cancion para que pueda ser enviado en la url
    song_name = urllib.parse.quote(song_name)
    # Se realiza la peticion a la API de itunes
    response = requests.get('https://itunes.apple.com/search?term={}&limit=25'.format(song_name))
    # Se obtiene la respuesta en formato json
    json_response = response.json()
    # Se obtiene la lista de canciones
    songs = json_response['results']
    # Se crea una lista vacia para almacenar las canciones
    songs_list = []
    # Se recorre la lista de canciones
    for song in songs:
        # Se crea una instancia de la clase Song con los datos de la cancion
        song_object = SongWS(
            song.get('trackName', 'N/A'),
            song.get('trackId', 'N/A'),
            song.get('collectionName', 'N/A'),
            song.get('artistName', 'N/A'),
            song.get('artworkUrl100', 'N/A'),
            song.get('releaseDate', 'N/A')[:4],
            [song.get('primaryGenreName', 'N/A')],
            song.get('trackTimeMillis', 'N/A'),
            'iTunes'
        )
        # Se agrega la cancion a la lista
        songs_list.append(song_object)
    # Se retorna la lista de canciones
    return songs_list