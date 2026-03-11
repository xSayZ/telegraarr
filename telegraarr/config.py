import os

# Telegram
BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_TELEGRAM_ID = int(os.environ["ADMIN_TELEGRAM_ID"])

# Jellyseerr
JELLYSEERR_URL = os.environ.get("JELLYSEERR_URL", "http://jellyseerr:5055")
JELLYSEERR_API_KEY = os.environ["JELLYSEERR_API_KEY"]

# Sonarr
SONARR_URL = os.environ.get("SONARR_URL", "http://sonarr:8989")
SONARR_API_KEY = os.environ["SONARR_API_KEY"]

# Sonarr Anime (optional second instance)
SONARR_ANIME_URL = os.environ.get("SONARR_ANIME_URL", "")
SONARR_ANIME_API_KEY = os.environ.get("SONARR_ANIME_API_KEY", "")

# Radarr
RADARR_URL = os.environ.get("RADARR_URL", "http://radarr:7878")
RADARR_API_KEY = os.environ["RADARR_API_KEY"]

# Jellyfin
JELLYFIN_URL = os.environ.get("JELLYFIN_URL", "http://jellyfin:8096")
JELLYFIN_API_KEY = os.environ["JELLYFIN_API_KEY"]

# Database
DB_PATH = os.environ.get("DB_PATH", "/config/telegraarr.db")