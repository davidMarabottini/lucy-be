import os
import time
import logging
import atexit

from ..extension import db


def create_shutdown_handler(app, fernet, tmp_db_path, abs_db_path):
    """Registra shutdown_func (cifra il DB temporaneo) e discard_func (lo elimina senza salvare)."""
    done = False

    def _release_connections():
        with app.app_context():
            db.session.remove()
            db.engine.dispose()
        time.sleep(0.5)

    def shutdown_and_encrypt():
        nonlocal done

        if done or app is None or fernet is None:
            return

        try:
            logging.info("Avvio procedura di chiusura sicura...")
            _release_connections()
            logging.info("Connessioni DB chiuse.")

            if not os.path.exists(tmp_db_path):
                logging.warning("Shutdown: Il file temporaneo non esiste già più.")
                return

            if os.path.getsize(tmp_db_path) == 0:
                logging.error("Shutdown: File temporaneo vuoto. Abortisco per evitare perdita dati.")
                return

            with open(tmp_db_path, "rb") as f:
                encrypted_data = fernet.encrypt(f.read())

            # Scrittura atomica: un crash a metà non deve corrompere l'unico DB cifrato.
            partial_path = abs_db_path + ".partial"
            with open(partial_path, "wb") as f:
                f.write(encrypted_data)
                f.flush()
                os.fsync(f.fileno())
            os.replace(partial_path, abs_db_path)

            os.remove(tmp_db_path)
            logging.info("Rimosso file temporaneo.")
            done = True
            logging.info("🔒 Database protetto e allineato correttamente.")

        except Exception as e:
            logging.error(f"❌ Errore critico durante lo shutdown: {e}")
            raise

    def discard_temp_db():
        """Elimina la copia decriptata senza toccare il DB cifrato originale."""
        nonlocal done

        if done or app is None or fernet is None:
            return

        try:
            _release_connections()
        finally:
            if os.path.exists(tmp_db_path):
                os.remove(tmp_db_path)
            done = True
            logging.info("Copia temporanea del DB scartata (DB cifrato originale non modificato).")

    app.shutdown_func = shutdown_and_encrypt
    app.discard_func = discard_temp_db
    atexit.register(shutdown_and_encrypt)
