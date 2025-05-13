# services/backend-pi/services/services_users.py
import httpx
from config import USER_SERVICE_URL


async def forward_register_request(payload: dict):
    try:
        async with httpx.AsyncClient() as client:
            return await client.post(f"{USER_SERVICE_URL}/api/users/",
                                     json=payload)
    except httpx.RequestError as exc:
        raise Exception(f"Error: {exc}")
