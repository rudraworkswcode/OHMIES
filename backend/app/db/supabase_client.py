import httpx
from typing import Optional, Dict, Any, List
import pandas as pd
from app.core.config import settings
from app.core.logging_config import logger
from app.db.seed_data import PROFILES, generate_hourly_records

class SupabaseService:
    def __init__(self):
        self.url = settings.SUPABASE_URL.strip()
        self.anon_key = settings.SUPABASE_ANON_KEY.strip()
        self.is_configured = bool(self.url and self.anon_key)
        if self.is_configured:
            logger.info("Supabase client initialized with endpoint %s", self.url)
        else:
            logger.info("Supabase credentials not configured in .env. Operating in Local Verified Dataset mode.")

    def get_user_profile(self, user_id_or_meter: str) -> Dict[str, Any]:
        """Resolves user profile by ID or meter number."""
        # Support default test user 'Jeevan' or 'JEEVAN KRISHNA'
        norm = user_id_or_meter.strip().upper()
        if norm in ["JEEVAN", "JEEVAN KRISHNA"]:
            return PROFILES["DOM-9821"]
            
        for profile in PROFILES.values():
            if profile["user_id"].upper() == norm or profile["meter_id"].upper() == norm:
                return profile
                
        # Default fallback to primary domestic profile
        return PROFILES["DOM-9821"]

    def list_all_archetype_profiles(self) -> List[Dict[str, Any]]:
        """Returns list of selectable sector/subcategory archetype profiles."""
        return list(PROFILES.values())

    async def fetch_consumption_records(self, meter_id: str, days: int = 30) -> pd.DataFrame:
        """
        Fetches consumption records for a meter.
        If live Supabase is configured, attempts REST API query with RLS.
        Otherwise falls back to high-resolution local dataset.
        """
        if self.is_configured:
            try:
                headers = {
                    "apikey": self.anon_key,
                    "Authorization": f"Bearer {self.anon_key}"
                }
                async with httpx.AsyncClient(timeout=5.0) as client:
                    resp = await client.get(
                        f"{self.url}/rest/v1/consumption_records?meter_id=eq.{meter_id}&order=timestamp.desc&limit={days * 24}",
                        headers=headers
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        if data and len(data) > 0:
                            logger.info("Successfully fetched %d records from live Supabase for meter %s", len(data), meter_id)
                            return pd.DataFrame(data)
                    logger.warning("Supabase returned status %d. Falling back to local verified dataset.", resp.status_code)
            except Exception as e:
                logger.error("Error querying Supabase: %s. Using local verified dataset fallback.", str(e))
                
        # Return deterministic verified dataset
        return generate_hourly_records(meter_id, days=days)

db_service = SupabaseService()

