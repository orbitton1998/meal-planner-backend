import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Falls back to the anon key so the app still runs before SUPABASE_SERVICE_ROLE_KEY
# is filled in; saving/history will only work once the real service role key is set.
_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
_key = _service_key or os.getenv("SUPABASE_KEY").strip()

supabase: Client = create_client(os.getenv("SUPABASE_URL").strip(), _key)
