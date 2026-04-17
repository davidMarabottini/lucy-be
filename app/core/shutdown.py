import os
import logging
import atexit

from ..extension import db

_shutdown_executed = False


def create_shutdown_handler(app, fernet, tmp_db_path, abs_db_path):
    """Crea e registra la funzione di shutdown che cifra il DB temporaneo."""
    global _shutdown_executed
    _shutdown_executed = False

    def shutdown_and_encrypt():
        global _shutdown_executed

        if _shutdown_executed or app is None:
            return

        try:
            logging.info("Avvio procedura di chiusura sicura...")

            with app.app_context():
                db.session.remove()
                db.engine.dispose()

            logging.info("Connessioni DB chiuse.")

            import time
            time.sleep(0.5)

            if not os.path.exists(tmp_db_path):
                logging.warning("Shutdown: Il file temporaneo non esiste già più.")
                return

            if os.path.getsize(tmp_db_path) == 0:
                logging.error("Shutdown: File temporaneo vuoto. Abortisco per evitare perdita dati.")
                return

            with open(tmp_db_path, "rb") as f:
                data = f.read()

            encrypted_data = fernet.encrypt(data)
            with open(abs_db_path, "wb") as f:
                f.write(encrypted_data)

            os.remove(tmp_db_path)
            logging.info("Rimosso file temporaneo.")
            _shutdown_executed = True
            logging.info("🔒 Database protetto e allineato correttamente.")

        except Exception as e:
            logging.error(f"❌ Errore critico durante lo shutdown: {e}")
            raise e

    app.shutdown_func = shutdown_and_encrypt
    atexit.register(shutdown_and_encrypt)
