import requests
import base64
import urllib.parse
from .song import SongWS  # Make sure you import the SongWS class
from .globals import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Obtiene el token de acceso de Spotify
def get_token_spotify():
    try:
        # Se obtienen las credenciales de la aplicacion de spotify
        client_id = SPOTIFY_CLIENT_ID
        client_secret = SPOTIFY_CLIENT_SECRET

        # Se codifican las credenciales en base64
        client_credentials = base64.b64encode((client_id + ":" + client_secret).encode("utf-8")).decode("utf-8")
        # Se realiza la peticion a la API de spotify para obtener el token de acceso
        response = requests.post("https://accounts.spotify.com/api/token", 
                                 data={"grant_type": "client_credentials"}, 
                                 headers={"Authorization": "Basic " + client_credentials})
        # Se valida que la peticion haya sido exitosa
        response.raise_for_status()  

        # Se obtiene el token de acceso
        response_json = response.json()
        token = response_json.get("access_token")
        if token is None:
            raise ValueError("Access token not found in the response")
        
        return token
    except requests.exceptions.RequestException as e:
        raise Exception("Error getting Spotify token: " + str(e))

# Busca una cancion en spotify
def search_spotify(song_name):
    try:
        # Se obtiene el token de acceso
        token = get_token_spotify()
        # Se codifica el nombre de la cancion para que pueda ser utilizado en la URL
        song_name = urllib.parse.quote(song_name)
        # Se realiza la peticion a la API de spotify
        search_response = requests.get("https://api.spotify.com/v1/search?q=" + song_name + "&type=track&limit=20", headers={"Authorization": "Bearer " + token})
        # Se valida que la peticion haya sido exitosa
        search_response.raise_for_status()
        # Se obtiene el JSON de la respuesta
        search_response_json = search_response.json()
        # Se obtiene la lista de canciones de la respuesta
        songs = search_response_json.get("tracks", {}).get("items", [])
        # Se crea una lista con los nombres de las canciones
        songs_list = []
        # Se recorre la lista de canciones
        for song in songs:
            try:
                # Se realiza una peticion a la API de spotify para obtener el genero de la cancion
                artist_id = song["artists"][0]["id"]
                album_response = requests.get("https://api.spotify.com/v1/artists/" + artist_id, headers={"Authorization": "Bearer " + token})
                # **Nota** Se obtiene el genero del artista, no de la cancion, ya que la API de spotify todavia no lo implementa
                # Se valida que la peticion haya sido exitosa
                album_response.raise_for_status()
                # Se obtiene el JSON de la respuesta
                album_response_json = album_response.json()
                # Se obtiene el genero del album de la cancion
                genre = album_response_json.get("genres", ["N/A"])
                # Se crea el objeto de la cancion
                song_object = SongWS(
                    song.get("name", "N/A"),
                    song.get("id", "N/A"),
                    (song.get('album', {}) or {}).get('name', 'N/A') or 'N/A',
                    ", ".join([artist["name"] for artist in song["artists"]]) if len(song["artists"]) > 0 else "N/A",
                    song["album"]["images"][0]["url"] if len(song["album"]["images"]) > 0 else "N/A",
                    ((song.get('album', {}) or {}).get('release_date', 'N/A') or 'N/A')[:4] or 'N/A',
                    genre,
                    song.get("duration_ms", "N/A"),
                    "Spotify"
                )
                songs_list.append(song_object)
            except KeyError:
                # Handle missing or invalid data in the song response
                continue
        
        return songs_list
    except requests.exceptions.RequestException as e:
        raise Exception("Error while searching Spotify: " + str(e))