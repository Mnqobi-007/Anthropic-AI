import os
from fastapi import Depends, HTTPException, status
import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-here")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

security = HTTPBearer()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token, 
            JWT_SECRET, 
            algorithms=["HS256"], 
            audience="authenticated",
            options={"verify_signature": True}
        )

        # Validate token by Supabase verification
        try:
            response = supabase.auth.get_user(token)
            if response.user:
                payload["email"] = response.user.email
                payload["created_at"] = response.user.created_at
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def create_user_jwt(email: str, password: str):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer",
            "user": {
                "id": response.user.id,
                "email": response.user.email
            }
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

def refresh_supabase_token(refresh_token: str):
    try:
        response = supabase.auth.refresh_session(refresh_token)
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer",
            "expires_in": getattr(response.session, 'expires_in', None)
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

def signup_user(email: str, password: str):
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Signup failed"
            )
        
        return {
            "message": "User created successfully",
            "user_id": response.user.id,
            "email": response.user.email,
            "confirmed_at": response.user.confirmed_at
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )