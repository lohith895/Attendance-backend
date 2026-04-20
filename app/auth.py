# auth.py (JWT-secret-free)
from fastapi import Header, HTTPException
import os, requests
from dotenv import load_dotenv

load_dotenv() 

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.replace("Bearer ", "").strip()

    r = requests.get(
        f"{SUPABASE_URL}/auth/v1/user",
        headers={"Authorization": f"Bearer {token}", "apikey": SUPABASE_ANON_KEY},
        verify=False  # Skip SSL verification for local dev
    )

    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return r.json()  # contains user id etc.
