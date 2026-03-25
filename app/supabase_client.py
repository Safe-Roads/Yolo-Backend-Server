from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("❌ Supabase credentials not set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)