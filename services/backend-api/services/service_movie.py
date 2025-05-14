# services/backend-pi/services/service_movie.py
import httpx
from config import MOVIE_SERVICE_URL


async def get_popular_movie(lang_code: str, pageNum: int):
    try:
        async with httpx.AsyncClient() as client:
            return await client.get(f"{MOVIE_SERVICE_URL}/{lang_code}/fetchPopularMovies/{pageNum}/")
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
        raise Exception(f"Error: {exc}")