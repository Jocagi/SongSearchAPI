# Song Search API - Cuadra

## Descripción

El proyecto SongSearchAPI es una API que centraliza la búsqueda de canciones por nombre en diferentes proveedores (Spotify, iTunes y Genius). Este servicio permite a los usuarios buscar canciones fácilmente, permitiendo aplicar filtros por género y año de lanzamiento.

## Prerrequisitos
Para ejecutar el proyecto es necesario tener Docker instalado en tu sistema. Puedes descargarlo e instalarlo desde [aquí](https://www.docker.com/products/docker-desktop/).

## Instrucciones de ejecución

Para ejecutar el presente proyecto con Docker, sigue los siguientes pasos:

1. Clona el repositorio.

2. Modifica el archivo `.env` para agregar las claves de las API de los proveedores y una secret key:

   ```bash
   SECRET_KEY=<secret key>
   SPOTIFY_CLIENT_ID=<Spotify client id>
   SPOTIFY_CLIENT_SECRET=<Spotify client secret>
   GENIUS_CLIENT_ID=<Genius client id>
   GENIUS_CLIENT_SECRET=<Genius client secret>
   DEBUG=True
   ```

3. Construye el contenedor de Docker:

   ```bash
   docker build -t songsearchapi .
   ```

4. Ejecuta el contenedor Docker:

   ```bash
   docker run -p 8000:8000 songsearchapi
   ```

   Al seguir estos pasos, el servicio estará disponible en: http://localhost:8000

## Documentación de la API

La definición de los endpoints puede encontrarse en: http://localhost:8000/api/swagger/

## Uso

- **Autenticarse en la aplicación**
  - Utiliza el endpoint `/api/token` para autenticarse con usuario y contraseña y crear un token.
  - Realiza un POST con los siguientes datos:
    ```json
    {
      "username": "user",
      "password": "user"
    }
    ```
    ** Se ha definido un usuario por defecto en el Dockerfile, pueden crearse usuarios adicionales desde el panel de administración.

- **Buscar canciones**
  - Utiliza el endpoint `/api/search` para buscar canciones.
  - Realiza una petición GET con la siguiente estructura:
    ```bash
    http://{endpoint}/api/search?query={canción}
    ```
    Ejemplo:
    ```bash
    http://localhost:8000/api/search?query=Test
    ```
  - Es posible aplicar filtros agregando los parámetros "year" y "genre":
    ```bash
    http://{endpoint}/api/search/?query={canción}&year={año}&genre={género}
    ```
    Ejemplos:
    ```bash
    http://localhost:8000/api/search/?query=test&year=2018&genre=pop
    ```
    ```bash
    http://localhost:8000/api/search/?query=test&year=2018
    ```
    ```bash
    http://localhost:8000/api/search/?query=test&genre=pop
    ```

Recordar personalizar los valores de las claves de las API y la secret key en el archivo `.env`, y cambiar las contraseñas por defecto de los usuarios.
