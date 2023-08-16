import sys
from api.song import Song
from api.spotify import search_song_spotify
from api.itunes import search_song_itunes
from api.genius import search_song_genius

def main():
    # Se obtiene el nombre de la cancion a buscar
    if len(sys.argv) != 2:
        song_name = "Test"
    else:
        song_name = sys.argv[1]
    # Se realiza la busqueda de la cancion
    songs_list = search_song_genius(song_name)
    # Se imprime la lista de canciones
    if len(songs_list) == 0:
        print("No se encontraron canciones")
    else:
        for song in songs_list:
            print(song)
            print("------------------------------")

if __name__ == "__main__":
    main()