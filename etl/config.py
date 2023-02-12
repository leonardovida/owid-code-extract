from os import environ as env

from dotenv import load_dotenv

ENV_FILE = env.get("ENV", ".env")

load_dotenv(ENV_FILE)

DEBUG = env.get("DEBUG") == "True"

# Publishing to Postgres
POSTGRES_USER_ID = env.get("POSTGRES_USER_ID")
DB_PORT = int(env.get("DB_PORT", "3306"))
DB_USER = env.get("DB_USER", "root")
DB_PASS = env.get("DB_PASS", "")
DB_NAME = env.get("DB_NAME", "nearit")
DB_HOST = env.get("DB_HOST", "localhost")

# Maps
CITIES_MAPPING = env.get("CITIES_MAPPING", "data/cities_mapping.csv")

# Amigo Specific
AMIGO_URL = env.get("URL_AMIGO", "https://api.amigo.app")
AMIGO_PORT = env.get("PORT_AMIGO", "443")
AMIGO_TOKEN = env.get("AMIGO_TOKEN")
AMIGO_UUID = env.get("AMIGO_UUID")
AMIGO_BEARER_TOKEN = env.get("AMIGO_BEARER_TOKEN")
AMIGO_PLACES_DF = env.get("AMIGO_PLACES_DF")

# Mapstr Specific
# MAPSTR_URL = env.get("MAPSTR_URL", "https://server.mapstr.com/")
# MAPSTR_PORT = env.get("MAPSTR_PORT", "443")
# MAPSTR_TOKEN = env.get("MAPSTR_MAPKIT_TOKEN")
# MAPSTR_UUID = env.get("MAPSTR_UUID")
# MAPSTR_PLACES_DF = env.get("MAPSTR_PLACES_DF")

# Google specific
# GOOGLE_KEY = env.get("GOOGLE_KEY")
