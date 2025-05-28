from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import decode_access_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        token = credentials.credentials
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=403, detail="Invalid or expired token")
        return payload["sub"] 
