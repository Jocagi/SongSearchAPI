from rest_framework import views, status
from rest_framework.response import Response
from .providers import search_spotify, search_itunes, search_genius
from .models import Song
from .serializers import SongSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import concurrent.futures

class SearchSongsView(views.APIView):

    # Valida que el usuario este autenticado
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Documentacion de la API
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Song Name', required=True),
            openapi.Parameter('genre', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Genre', required=False),
            openapi.Parameter('year', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Year', required=False),
            openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Bearer {token}', format='Bearer', required=True)
        ],
        operation_description='''Search songs by name, genre and year''',
        responses={200: 'OK', 401: 'Unauthorized'}
    )

    def get(self, request):
        try:
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

                # Busca en los proveedores de forma concurrente
                def run_search(provider_func):
                    try:
                        return provider_func(query)
                    except Exception as e:
                        print("Error in provider_func:", str(e))
                        return []

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    spotify_future = executor.submit(run_search, search_spotify)
                    itunes_future = executor.submit(run_search, search_itunes)
                    genius_future = executor.submit(run_search, search_genius)

                songs = spotify_future.result() + itunes_future.result() + genius_future.result()

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

        except Exception as e:
            return Response({'error': 'An error occurred: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
