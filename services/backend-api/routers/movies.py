# services/backend-api/routers/users.py
from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.responses import JSONResponse
from services.service_movie import get_popular_movie
from typing import Literal

router = APIRouter()


import logging


@router.get("/{lang_code}/fetchPopularMovies/{pageNum}")
async def fetchPopularMovies(
    lang_code: Literal["en", "fr"],
    pageNum: int = Path(..., gt=0) 
):
    try:
        if lang_code not in ["en", "fr"]:
            raise HTTPException(status_code=400, detail="Invalid language code")
        resp = await get_popular_movie(lang_code, pageNum)
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except Exception as e:
        logging.error(f"Error fetching popular movies: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")