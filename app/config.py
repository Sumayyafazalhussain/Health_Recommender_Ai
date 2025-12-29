
# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Settings:
#     # API Keys
#     GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
#     GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
#     # MongoDB
#     MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
#     DB_NAME: str = os.getenv("DB_NAME", "recommendation_db")
    
#     # Server
#     HOST: str = os.getenv("HOST", "0.0.0.0")
#     PORT: int = int(os.getenv("PORT", 8000))
#     DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
#     # Gemini Configuration
#     GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
#     def validate(self):
#         """Validate required settings"""
#         missing = []
#         if not self.GOOGLE_API_KEY:
#             missing.append("GOOGLE_API_KEY")
#         if not self.GEMINI_API_KEY:
#             missing.append("GEMINI_API_KEY")
        
#         if missing:
#             raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

# settings = Settings()

# # Validate on import
# try:
#     settings.validate()
#     print("✅ All API keys configured")
# except ValueError as e:
#     print(f"❌ Configuration Error: {e}")
#     exit(1)





# # app/config.py
# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Settings:
#     # ========== NEON POSTGRESQL ==========
#     # DIRECT Neon URL - This will be used everywhere
#     NEON_URL = "postgresql://neondb_owner:npg_adJ8QvFxsD4H@ep-twilight-poetry-ad9esqb5-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
#     # For SQLAlchemy
#     DATABASE_URL = NEON_URL
#     DATABASE_TYPE = "neon"
    
#     # ========== API KEYS ==========
#     GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
#     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
#     # ========== SERVER ==========
#     HOST = os.getenv("HOST", "0.0.0.0")
#     PORT = int(os.getenv("PORT", 8000))
#     DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
#     # ========== GEMINI ==========
#     GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# settings = Settings()

# # Print debug info
# print(f"⚙️ Config loaded: Database={settings.DATABASE_TYPE}")



# # app/config.py
# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Settings:
#     # ========== NEON POSTGRESQL ==========
#     # DIRECT Neon URL - Use YOUR Neon URL here
#     NEON_URL = "postgresql://neondb_owner:npg_adJ8QvFxsD4H@ep-twilight-poetry-ad9esqb5-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
#     # For SQLAlchemy
#     DATABASE_URL = NEON_URL
#     DATABASE_TYPE = "neon"
    
#     # ========== API KEYS ==========
#     GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
#     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
#     # ========== SERVER ==========
#     HOST = os.getenv("HOST", "0.0.0.0")
#     PORT = int(os.getenv("PORT", 8000))
#     DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
#     # ========== GEMINI ==========
#     GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# settings = Settings()

# # Print debug info
# print(f"⚙️ Config loaded: Database={settings.DATABASE_TYPE}")







# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # ========== NEON POSTGRESQL ==========
    # Use YOUR Neon URL from .env or hardcode it
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_adJ8QvFxsD4H@ep-twilight-poetry-ad9esqb5-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require")
    
    # For backward compatibility
    POSTGRES_URL = DATABASE_URL
    DATABASE_TYPE = "neon"
    
    # ========== API KEYS ==========
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # ========== SERVER ==========
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # ========== GEMINI ==========
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

settings = Settings()

# Print debug info
print(f"⚙️ Config loaded")
print(f"🔗 Database URL set: {'Yes' if settings.DATABASE_URL else 'No'}")