import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.core.exceptions import CustomException

JWT_SECRET = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Decodes the JWT token and verifies its validity.
    Returns the decoded user payload or raises an HTTP 401 exception.
    """
    token = credentials.credentials
    try:
        # Decode and verify the token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Ensure the user identifier (e.g., 'sub') is present in the payload
        if "sub" not in payload:
               CustomException.call(
                message="Invalid token payload: Missing user ID",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        
        return payload 

    except jwt.ExpiredSignatureError:
         CustomException.call(
            message="Token has expired",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    except jwt.InvalidTokenError:
        CustomException.call(
             message="Invalid Authentication Token",
             status_code=status.HTTP_401_UNAUTHORIZED
        )
