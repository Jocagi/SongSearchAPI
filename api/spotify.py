import requests
import base64
import urllib.parse
from .song import Song

# Obtiene el token de acceso de spotify
def get_token_spotify():
    # Se obtienen las credenciales de la aplicacion de spotify
    #client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    #client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    client_id = ""
    client_secret = ""

    # Se codifican las credenciales en base64
    client_credentials = base64.b64encode((client_id + ":" + client_secret).encode("utf-8")).decode("utf-8")
    # Se realiza la peticion a la API de spotify para obtener el token de acceso
    response = requests.post("https://accounts.spotify.com/api/token", 
                              data={"grant_type": "client_credentials"}, 
                              headers={"Authorization": "Basic " + client_credentials})
    # Se obtiene el token de acceso
    response_json = response.json()
    token = response_json["access_token"]
    return token

# Busca una cancion en spotify
def search_song_spotify(song_name):
    # Se obtiene el token de acceso
    token = get_token_spotify()
    # Se codifica el nombre de la cancion para que pueda ser utilizado en la URL
    song_name = urllib.parse.quote(song_name)
    # Se realiza la peticion a la API de spotify
    search_response = requests.get("https://api.spotify.com/v1/search?q=" + song_name + "&type=track&limit=10", headers={"Authorization": "Bearer " + token})
    # Se obtiene el JSON de la respuesta
    search_response_json = search_response.json()
    # Se obtiene la lista de canciones de la respuesta
    songs = search_response_json["tracks"]["items"]
    # Se crea una lista con los nombres de las canciones
    songs_list = []
    # Se recorre la lista de canciones
    for song in songs:
        # Se realiza una peticion a la API de spotify para obtener el genero de la cancion
        # album_response = requests.get("https://api.spotify.com/v1/track/" + song["id"], headers={"Authorization": "Bearer " + token})
        album_response = requests.get("https://api.spotify.com/v1/artists/" + song["artists"][0]["id"], headers={"Authorization": "Bearer " + token})
        # **Nota** Se obtiene el genero del artista, no de la cancion, ya que la API de spotify todavia no lo implementa
    
        # Se obtiene el JSON de la respuesta
        album_response_json = album_response.json()
        # Se obtiene el genero del album de la cancion
        genre = album_response_json["genres"]
        # Se crea el objeto de la cancion
        songObject = Song(
        song["name"],
        song["id"],
        song["album"]["name"],
        ", ".join([artist["name"] for artist in song["artists"]]),
        song["album"]["images"][0]["url"],
        song["album"]["release_date"][:4],
        genre,
        song["duration_ms"],
        "Spotify"
        )
        songs_list.append(songObject)

    # Se devuelve la lista de canciones
    return songs_list