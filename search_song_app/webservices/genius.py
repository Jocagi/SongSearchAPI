import requests
import urllib.parse
from .song import SongWS
from .globals import GENIUS_CLIENT_ID, GENIUS_CLIENT_SECRET

#Funcion para obtener token de genius
def get_token_genius():
        # Se obtienen las credenciales de la aplicacion de genius
        client_id = GENIUS_CLIENT_ID
        client_secret = GENIUS_CLIENT_SECRET
        
        # Se realiza la peticion a la API de genius para obtener el token de acceso
        response = requests.post('https://api.genius.com/oauth/token',
                                    data={'grant_type': 'client_credentials'},
                                    auth=(client_id, client_secret))
        # Se retorna el token de acceso
        response_json = response.json()
        token = response_json["access_token"]
        return token

#Funcion para buscar una cancion en la API de Genius
def search_genius(song_name):
        #Se obtiene el token de acceso
        token = get_token_genius()
        # Se codifica el nombre de la cancion para que pueda ser utilizado en la URL
        song_name = urllib.parse.quote(song_name)
        # Se realiza la peticion a la API de genius para obtener la cancion
        search_response = requests.get('https://api.genius.com/search?q={}'.format(song_name),
                                headers={'Authorization': 'Bearer ' + token})
        # Se obtiene la respuesta de la peticion
        search_response_json = search_response.json()
        # Se obtiene la lista de canciones
        songs = search_response_json["response"]["hits"]
        # Se crea una lista con los nombres de las canciones
        songs_list = []
        # Se recorre la lista de canciones
        for song in songs:
                # Se realiza la peticion a la API de genius para obtener la cancion
                song_response = requests.get('https://api.genius.com/songs/{}'.format(song["result"]["id"]),
                                        headers={'Authorization': 'Bearer ' + token})
                # Se obtiene la respuesta de la peticion
                song_response_json = song_response.json()
                songinfo = song_response_json["response"]["song"]
                # Se crea un objeto de tipo Song con la informacion de la cancion
                songObject = SongWS(
                    songinfo.get('title', 'N/A') or 'N/A',
                    songinfo.get('id', 'N/A') or 'N/A',
                    (songinfo.get('album', {}) or {}).get('name', 'N/A') or 'N/A',
                    (songinfo.get('primary_artist', {}) or {}).get('name', 'N/A') or 'N/A',
                    (songinfo.get('album', {}) or {}).get('cover_art_url', 'N/A') or 'N/A',
                    (songinfo.get('release_date', 'N/A') or 'N/A')[:4] or 'N/A',
                    ["N/A"],  # Genius no provee el género de la canción
                    "N/A",    # Genius no provee la duración de la canción
                    'Genius'
                )
                songs_list.append(songObject)
        return songs_list
