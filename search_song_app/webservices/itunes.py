import requests
import urllib.parse
from .song import SongWS

# Busca una canción en la API de iTunes
def search_itunes(song_name):
    try:
        # Se codifica el nombre de la canción para que pueda ser enviado en la URL
        song_name = urllib.parse.quote(song_name)
        # Se realiza la petición a la API de iTunes
        response = requests.get('https://itunes.apple.com/search?term={}&limit=20'.format(song_name))
        # Se valida que la petición haya sido exitosa
        response.raise_for_status()
        # Se obtiene la respuesta en formato JSON
        json_response = response.json()
        # Se obtiene la lista de canciones
        songs = json_response.get('results', [])
        # Se crea una lista vacía para almacenar las canciones
        songs_list = []
        # Se recorre la lista de canciones
        for song in songs:
            try:
                # Se crea una instancia de la clase Song con los datos de la canción
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
                # Se agrega la canción a la lista
                songs_list.append(song_object)
            except KeyError:
                # Handle missing or invalid data in the song response
                continue
        # Se retorna la lista de canciones
        return songs_list
    except requests.exceptions.RequestException as e:
        raise Exception("Error while searching iTunes: " + str(e))