import hashlib
from fastapi.security import (
    HTTPAuthorizationCredentials, 
    HTTPBearer,
)
from datetime import (
    datetime, 
    timedelta,
)
from typing import Optional
from jose import (
    jwt, 
    JWTError,
)
from fastapi import (
    HTTPException, 
    Request, 
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
import logging
from core.config import settings


logger = logging.getLogger(__name__)

oauth2_scheme =HTTPBearer()

def hash_password(plain_password: str) -> str:
    return hashlib.sha256(plain_password.encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> str:
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> tuple:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
    return encoded_jwt, expire.isoformat()

async def get_access_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    logger.debug(f"Received Authorization header: {auth_header}")
    if not auth_header:
        logger.error("No Authorization header provided")
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.error(f"Invalid Authorization header format: {auth_header}")
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    
    token = parts[1].strip()
    logger.debug(f"Extracted token: {token[:20]}...")
    return token

async def validate_access_token(access_token: str) -> str:
    try:
        if not isinstance(access_token, str) or not access_token.strip():
            logger.error("Token is empty or not a string")
            raise HTTPException(status_code=401, detail="Invalid token: empty or not a string")
        
        logger.debug(f"Received token: {access_token[:20]}...")
        
        parts = access_token.split(".")
        if len(parts) != 3:
            logger.error(f"Invalid JWT structure: {len(parts)} parts")
            raise HTTPException(status_code=401, detail="Invalid token: incorrect structure")

        payload = jwt.decode(
            access_token,
            settings.TOKEN_SECRET_KEY,
            algorithms=[settings.TOKEN_ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            logger.error("No user_id in token payload")
            raise HTTPException(status_code=401, detail="Invalid token: user_id missing")
        
        exp = payload.get("exp")
        if exp and exp < datetime.utcnow().timestamp():
            logger.error(f"Token expired for user_id: {user_id}")
            raise HTTPException(status_code=401, detail="Token has expired")
        
        return int(user_id)
    except UnicodeDecodeError as e:
        logger.error(f"Token decoding error: {str(e)}, token: {access_token[:20]}...")
        raise HTTPException(status_code=401, detail="Invalid token: malformed encoding")
    except JWTError as e:
        logger.error(f"JWT decode error: {str(e)}, token: {access_token[:20]}...")
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during token validation: {str(e)}, token: {access_token[:20]}...")
        raise HTTPException(status_code=401, detail="Invalid token")