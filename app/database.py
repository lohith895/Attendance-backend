import os
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_SERVICE_KEY  # 👈 changed

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY  # 👈 changed - bypasses RLS entirely
)