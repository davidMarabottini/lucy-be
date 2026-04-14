import os
import tempfile

from core.config import APPDATA_DIR
from app import create_app

flask_app = None
server_thread = None


def open_data_folder():
    """Apre la cartella dati"""
    if os.name == 'nt':
        os.startfile(APPDATA_DIR)
    else:
        subprocess.run(['open' if os.name == 'posix' else 'xdg-open', LOG_DIR])

def open_temporary_folder():
    """Apre la cartella temporanea di sistema dove viene scompattato il DB"""
    temp_path = tempfile.gettempdir()

    if os.name == 'nt':
        os.startfile(temp_path)
    else:
        subprocess.run(['open' if os.name == 'posix' else 'xdg-open', temp_path])

