import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Stati Globali
app = None
server_thread = None

# Percorsi di Sistema
APPDATA_DIR = os.path.join(os.environ.get('APPDATA'), "LucyManager")
LOG_DIR = os.path.join(APPDATA_DIR, "logs")
DB_PATH = os.path.join(APPDATA_DIR, "lucy.db")
CURRENT_LOG_FILE = os.path.join(LOG_DIR, f"lucy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Assicurati che le cartelle esistano
os.makedirs(LOG_DIR, exist_ok=True)