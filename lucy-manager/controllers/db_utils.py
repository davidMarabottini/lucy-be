import os
from tkinter import messagebox, simpledialog
from app import create_app
import shutil
from datetime import datetime
from tkinter import filedialog, messagebox
import logging
from app.utils.crypto import decrypt_db, encrypt_db
from app.core.migrations import generate_revision, migrate_encrypted_db
from core import state


APPDATA_DIR = os.path.join(os.environ.get('APPDATA'), "LucyManager")

DB_PATH = os.path.join(APPDATA_DIR, "lucy.db")


def backup_database():
  if not os.path.exists(DB_PATH):
      messagebox.showerror("Errore", f"File database non trovato in:\n{DB_PATH}")
      return

  timestamp = datetime.now().strftime("%Y%m%d_%H%M")
  default_filename = f"lucy_{timestamp}.db"

  destination_path = filedialog.asksaveasfilename(
      initialfile=default_filename,
      defaultextension=".db",
      title="Salva Backup Database",
      filetypes=[("SQLite Database", "*.db")]
  )

  if destination_path:
    try:
      shutil.copy2(DB_PATH, destination_path)
      messagebox.showinfo("Successo", "Backup creato correttamente!")
    except Exception as e:
      messagebox.showerror("Errore", f"Errore durante il salvataggio: {e}")

def utility_decripta_db():
    """Utility per salvare una copia decriptata del DB"""
    password = simpledialog.askstring("Utility Decrittazione", "Inserisci la password del DB:", show='*')
    if not password: return

    file_origine = filedialog.askopenfilename(
        title="Seleziona il database criptato",
        initialdir=APPDATA_DIR,
        filetypes=[("Database Criptato", "*.db")]
    )
    if not file_origine: return

    file_destinazione = filedialog.asksaveasfilename(
        title="Salva DB decriptato come...",
        defaultextension=".db",
        filetypes=[("SQLite Database", "*.db")]
    )
    if not file_destinazione: return

    try:
        decrypt_db(password, file_origine, file_destinazione)
        messagebox.showinfo("Successo", f"File decriptato correttamente in:\n{file_destinazione}")
    except Exception as e:
        messagebox.showerror("Errore", "Impossibile decrittare. Password errata o file corrotto.")

def utility_cripta_db():
    """Utility per criptare un DB SQLite standard nel formato Lucy"""
    password = simpledialog.askstring("Utility Cifratura", "Scegli la password per criptare il DB:", show='*')
    if not password: return

    file_origine = filedialog.askopenfilename(
        title="Seleziona il database DECRIPTATO",
        filetypes=[("SQLite Database", "*.db"), ("Tutti i file", "*.*")]
    )
    if not file_origine: return

    file_destinazione = filedialog.asksaveasfilename(
        title="Salva DB criptato come...",
        initialdir=APPDATA_DIR,
        initialfile="lucy.db",
        defaultextension=".db",
        filetypes=[("Database Criptato", "*.db")]
    )
    if not file_destinazione: return

    try:
        encrypt_db(password, file_origine, file_destinazione)
        messagebox.showinfo("Successo", f"File criptato con successo!\nSalvato in: {file_destinazione}")
        logging.info(f"Manutenzione: DB criptato manualmente in {file_destinazione}")
    except Exception as e:
        logging.error(f"Errore utility criptazione: {e}")
        messagebox.showerror("Errore", f"Impossibile criptare il file: {e}")

def generate_migration():
    """Genera una migration dai modelli (solo DEV_MODE). Non usa il DB reale né la password."""
    message = simpledialog.askstring("Generate Migration", "Descrizione della migration:")
    if not message:
        return

    try:
        path = generate_revision(message)
    except Exception as e:
        logging.error(f"Errore durante la generazione migration: {e}")
        messagebox.showerror("Errore", f"Impossibile generare la migration: {e}")
        return

    if path is None:
        messagebox.showinfo("Nessuna modifica", "I modelli coincidono con le migration esistenti: niente da generare.")
    else:
        logging.info(f"Migration generata: {path}")
        messagebox.showinfo("Successo", f"Migration generata e verificata:\n{path}\n\nControllala prima di committarla.")


def run_migrations():
    """Applica le migration pendenti al DB cifrato (backup automatico prima di salvare)."""
    if state.active_app is not None:
        messagebox.showwarning("Server attivo", "Ferma il server prima di applicare le migration.")
        return

    if not os.path.exists(DB_PATH):
        messagebox.showwarning("Database Mancante", "Il database non esiste. Inizializzalo prima.")
        return

    password = simpledialog.askstring("DB Migrate", "Password del database:", show='*')
    if not password:
        return

    try:
        result = migrate_encrypted_db(DB_PATH, password)
    except Exception as e:
        logging.error(f"Errore durante le migration: {e}")
        messagebox.showerror("Errore", f"Migration non applicata, il database non è stato modificato:\n{e}")
        return

    logging.info(result)
    messagebox.showinfo("Migration", result)


def initialize_db():
    if os.path.exists(DB_PATH):
        messagebox.showinfo("Info", "Il database esiste già. Usa 'Avvia Server' per accedere.")
        return

    # Chiediamo la password per la PRIMA creazione
    password = simpledialog.askstring("Setup Iniziale", "Scegli una password per CRIPTARE il nuovo database:", show='*')

    if not password:
        return

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    temp_app = None
    success = False
    result = None
    try:
        normalized_path = DB_PATH.replace('\\', '/')
        temp_app = create_app(db_path=normalized_path, db_password=password)

        with temp_app.app_context():
            result = temp_app.setup_database_func()

        success = True
    except Exception as e:
        logging.error(f"Errore inizializzazione: {e}")
        messagebox.showerror("Errore Critico", f"Impossibile creare il database: {e}")
    finally:
        if temp_app is not None:
            if hasattr(temp_app, 'shutdown_func'):
                try:
                    temp_app.shutdown_func()
                    if success:
                        messagebox.showinfo("Successo", f"{result}\n\nDatabase sigillato correttamente!")
                except Exception as e:
                    logging.error(f"Errore durante lo shutdown/cifratura: {e}")
                    messagebox.showerror("Errore Cifratura", f"Errore durante il salvataggio del database cifrato: {e}")
            else:
                messagebox.showerror("Errore", "Funzione shutdown_func non trovata.")