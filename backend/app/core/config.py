import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

class Settings(BaseModel):
    PROJECT_NAME: str = "OHMies"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", 8000))
    FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    
    # JWT & Auth
    JWT_SECRET: str = os.getenv("JWT_SECRET", "ohmmies_dev_jwt_key_994827_2026_secured")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))
    
    # Development Credentials
    DEV_DEFAULT_USER: str = os.getenv("DEV_DEFAULT_USER", "JEEVAN KRISHNA")
    DEV_DEFAULT_PASSWORD: str = os.getenv("DEV_DEFAULT_PASSWORD", "JAI RNSIT")
    
    # Supabase (optional)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    
    # Documented Carbon Emission Factor
    # Source: CEA (Central Electricity Authority) India CO2 Baseline Database v19 (~0.716-0.72 kg CO2e / kWh)
    GRID_EMISSION_FACTOR_KG_PER_KWH: float = 0.72

settings = Settings()

