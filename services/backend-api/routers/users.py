# services/backend-api/routers/users.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from services.service_user import forward_register_request


router = APIRouter()


@router.post("/register")
async def register(request: Request):
    try:
        body = await request.json()
        response = await forward_register_request(body)
        return JSONResponse(status_code=response.status_code, content=response.json())
    except Exception as e:
        raise HTTPException(status_code=500,  detail=str(e))
