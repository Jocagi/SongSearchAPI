import requests
import urllib.parse
from .song import SongWS
from .globals import GENIUS_CLIENT_ID, GENIUS_CLIENT_SECRET

# Obtener token de Genius
def get_token_genius():
    try:
        # Se obtienen las credenciales de la aplicación de Genius
        client_id = GENIUS_CLIENT_ID
        client_secret = GENIUS_CLIENT_SECRET
        
        # Se realiza la petición a la API de Genius para obtener el token de acceso
        response = requests.post('https://api.genius.com/oauth/token',
                                 data={'grant_type': 'client_credentials'},
                                 auth=(client_id, client_secret))
        
        # Se verifica si la petición fue exitosa
        response.raise_for_status()
        
        # Se obtiene el token de acceso
        response_json = response.json()
        token = response_json.get("access_token")
        if token is None:
            raise ValueError("Access token not found in the response")
        
        return token
    except requests.exceptions.RequestException as e:
        raise Exception("Error getting Genius token: " + str(e))

# Buscar una canción en la API de Genius
def search_genius(song_name):
    try:
        # Se obtiene el token de acceso
        token = get_token_genius()
        
        # Se codifica el nombre de la canción para que pueda ser utilizado en la URL
        song_name = urllib.parse.quote(song_name)
        
        # Se realiza la petición a la API de Genius para obtener la canción
        search_response = requests.get('https://api.genius.com/search?q={}'.format(song_name),
                                       headers={'Authorization': 'Bearer ' + token})
        
        # Se verifica si la petición fue exitosa
        search_response.raise_for_status()
        
        # Se obtiene la respuesta de la petición
        search_response_json = search_response.json()
        
        # Se obtiene la lista de canciones
        songs = search_response_json.get("response", {}).get("hits", [])
        
        songs_list = []
        for song in songs:
            try:
                song_id = song["result"]["id"]
                song_response = requests.get('https://api.genius.com/songs/{}'.format(song_id),
                                             headers={'Authorization': 'Bearer ' + token})
                
                # Se verifica si la petición fue exitosa
                song_response.raise_for_status()
                
                song_response_json = song_response.json()
                songinfo = song_response_json.get("response", {}).get("song", {})
                
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
            except KeyError:
                # Maneja datos faltantes o inválidos en la respuesta de la canción
                continue
        
        return songs_list
    except requests.exceptions.RequestException as e:
        raise Exception("Error while searching Genius: " + str(e))