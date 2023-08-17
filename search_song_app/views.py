from rest_framework import views, status
from rest_framework.response import Response
from .providers import search_spotify, search_itunes, search_genius
from .models import Song
from .serializers import SongSerializer

class SearchSongsView(views.APIView):
    def get(self, request):
        query = request.query_params.get('query')
        genre = request.query_params.get('genre')
        year = request.query_params.get('year')

        # Primero, intenta buscar en la base de datos (si hay un cache en la base de datos)
        songs = Song.objects.filter(query__iexact=query)
        if genre:
            songs = songs.filter(genres__icontains=genre)
        if year:
            songs = songs.filter(year_release_date=year)

        # Si no hay resultados en la base de datos, busca en los proveedores
        if not songs.exists():
            songs = search_spotify(query) + search_itunes(query) + search_genius(query)

            # Almacena los resultados en la base de datos
            for song_data in songs:
                song, created = Song.objects.get_or_create(
                    query=query,
                    name=song_data.name,
                    song_id=song_data.song_id,
                    album=song_data.album,
                    artist=song_data.artist,
                    album_cover=song_data.album_cover,
                    year_release_date=song_data.year_release_date,
                    genres=song_data.genres,
                    duration=song_data.duration,
                    origin=song_data.origin,
                )

            # Aplica filtros
            songs = Song.objects.filter(query__iexact=query)
            if genre:
                songs = songs.filter(genres__icontains=genre)
            if year:
                songs = songs.filter(year_release_date=year)
    
        # Quita parametro id de la respuesta
        for song in songs:
            del song.id
            del song.query

        # Ordena los resultados por nombre
        songs = sorted(songs, key=lambda song: song.name)

        # Serializa los resultados
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
