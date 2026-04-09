import os
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog
import webbrowser
import webview
from app import create_app
import shutil
from datetime import datetime
from tkinter import filedialog, scrolledtext, messagebox
import logging
from dotenv import load_dotenv
from app import decrypt_db
import subprocess
import tempfile
from app import encrypt_db

load_dotenv()

app = None
server_thread = None

status_var_text = None
log_display_text = None

APPDATA_DIR = os.path.join(os.environ.get('APPDATA'), "LucyManager")
if not os.path.exists(APPDATA_DIR):
    os.makedirs(APPDATA_DIR, exist_ok=True)
    
LOG_DIR = os.path.join(APPDATA_DIR, "logs")
DB_PATH = os.path.join(APPDATA_DIR, "lucy.db")
CURRENT_LOG_FILE = os.path.join(LOG_DIR, f"lucy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def configure_logging_to_file():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(CURRENT_LOG_FILE),
            logging.StreamHandler()
        ]
    )

def update_live_logs(text_widget):
    if os.path.exists(CURRENT_LOG_FILE):
        with open(CURRENT_LOG_FILE, "r") as f:
            lines = f.readlines()
            last_lines = "".join(lines[-50:]) # Prendi le ultime 5

            text_widget.config(state=tk.NORMAL)
            text_widget.delete('1.0', tk.END)
            text_widget.insert(tk.END, last_lines)
            text_widget.see(tk.END) # Scroll automatico alla fine
            text_widget.config(state=tk.DISABLED) # Torna in sola lettura
            
    # Riesegui tra 1000ms (1 secondo)
    root.after(1000, lambda: update_live_logs(text_widget))
    # root.after(1000, update_live_logs)
    
def open_data_folder():
    """Apre la cartella dati"""
    if os.name == 'nt':
        os.startfile(APPDATA_DIR)
    else:
        subprocess.run(['open' if os.name == 'posix' else 'xdg-open', LOG_DIR])

def open_temporary_folder():
    """Apre la cartella temporanea di sistema dove viene scompattato il DB"""
    temp_path = tempfile.gettempdir()
    
    # Se vuoi essere ancora più preciso e aprire direttamente la cartella 
    # dove Python mette i file temporanei (spesso una sottocartella specifica)
    if os.name == 'nt':
        os.startfile(temp_path)
    else:
        subprocess.run(['open' if os.name == 'posix' else 'xdg-open', temp_path])

def start_server():
    global app, server_thread, status_var_text
    
    if not os.path.exists(DB_PATH):
        messagebox.showwarning("Database Mancante", "Il database non esiste. Clicca su 'Inizializza DB' prima di avviare.")
        return

    password = simpledialog.askstring("Login", "Inserisci la password del database:", show='*')
    if not password: return

    try:
        normalized_db_path = os.path.abspath(DB_PATH).replace("\\", "/")
        messagebox.showinfo("normalized", f"normalized_db_path: {normalized_db_path}")
        app = create_app(db_path=normalized_db_path, db_password=password)
        # Qui il server parte ma NON tocca le tabelle (sono già state create)
        server_thread = threading.Thread(
            target=lambda: app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False),
            daemon=True
        )
        server_thread.start()
        status_var_text.set("Stato: ✅ Server Attivo")
    except Exception as e:
        logging.error(f"Errore durante l'avvio del server: {e}")
        messagebox.showerror("Errore di Avvio", f"Dettaglio: {e}")

def create_admin():
    if not app:
        messagebox.showerror("Errore", "Server non avviato")
        return
    username = simpledialog.askstring("Username", "Inserisci username:")
    if not username:
        return
    email = simpledialog.askstring("Email", "Inserisci email:")
    if not email:
        return
    password = simpledialog.askstring("Password", "Inserisci password:", show="*")
    if not password:
        return
    with app.app_context():
        result = app.create_admin_func(username, email, password)
        messagebox.showinfo("Risultato", result)

def create_week_days():
    if not app:
        messagebox.showerror("Errore", "Server non avviato")
        return
    with app.app_context():
        result = app.create_week_days_func()
        messagebox.showinfo("Risultato", result)
        
def open_web_app():
  if not server_thread or not server_thread.is_alive():
    messagebox.showerror("Errore", "Avvia prima il server")
    return print("Aprendo app...")
  
  webbrowser.open("http://127.0.0.1:5000/")
        
def open_app():
    if not server_thread or not server_thread.is_alive():
        messagebox.showerror("Errore", "Avvia prima il server")
        return

    print("Aprendo app in modalità desktop...")

    # URL del server Flask
    url = "http://127.0.0.1:5000/"

    # Crea una finestra WebView
    window = webview.create_window("Lucy Desktop", url, width=1200, height=800)

    # Avvia il loop della finestra (bloccante)
    webview.start()


def backup_database():
    # 1. Recupera il percorso del DB attuale (assicurati che DB_PATH sia definita)
    # Se non hai ancora definito DB_PATH, usa il percorso relativo o assoluto del tuo sqlite
    source_db = "lucy.db" 

    if not os.path.exists(DB_PATH):
        messagebox.showerror("Errore", f"File database non trovato in:\n{DB_PATH}")
        return

    # 2. Genera il nome file con giorno e ora
    # Formato: lucy_20231027_1530.db
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    default_filename = f"lucy_{timestamp}.db"

    # 3. Chiedi all'utente dove salvare
    destination_path = filedialog.asksaveasfilename(
        initialfile=default_filename,
        defaultextension=".db",
        title="Salva Backup Database",
        filetypes=[("SQLite Database", "*.db")]
    )

    if destination_path:
        try:
            # 4. Copia il file
            shutil.copy2(DB_PATH, destination_path)
            messagebox.showinfo("Successo", "Backup creato correttamente!")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante il salvataggio: {e}")

    if os.path.exists(DB_PATH):
        messagebox.showinfo("Info", "Il database esiste già. Usa 'Avvia Server' per accedere.")
        return

    # Chiediamo la password per la PRIMA creazione
    password = simpledialog.askstring("Setup Iniziale", "Scegli una password per CRIPTARE il nuovo database:", show='*')
    
    if not password:
        return

    try:
        # 1. Creiamo un'istanza temporanea dell'app per attivare il driver SQLCipher
        temp_app = create_app(db_path=DB_PATH, db_password=password)
        
        # 2. Chiamiamo la funzione di creazione tabelle
        with temp_app.app_context():
            result = temp_app.setup_database_func()
            
    except Exception as e:
        messagebox.showerror("Errore Critico", f"Impossibile creare il database: {e}")


def stop_server():
    global app, server_thread, status_var_text

    if not app:
        messagebox.showerror("Errore", "Server non avviato")
        return

    try:
        # 🔐 Chiude DB e lo ricripta
        if hasattr(app, "shutdown_func"):
            app.shutdown_func()

        app = None
        server_thread = None

        status_var_text.set("Stato: 🔴 Server Fermato (DB criptato)")
        messagebox.showinfo("OK", "Server fermato correttamente")

    except Exception as e:
        logging.error("Errore", f"Errore durante lo stop: {e}")
        messagebox.showerror("Errore", f"Errore durante lo stop: {e}")
    
def utility_decripta_db():
    """Utility per salvare una copia decriptata del DB"""
    password = simpledialog.askstring("Utility Decrittazione", "Inserisci la password del DB:", show='*')
    if not password: return

    # Seleziona il file .db.enc (default quello in APPDATA)
    file_origine = filedialog.askopenfilename(
        title="Seleziona il database criptato",
        initialdir=APPDATA_DIR,
        filetypes=[("Database Criptato", "*.db")]
    )
    if not file_origine: return

    # Chiedi dove salvare il file in chiaro
    file_destinazione = filedialog.asksaveasfilename(
        title="Salva DB decriptato come...",
        defaultextension=".db",
        filetypes=[("SQLite Database", "*.db")]
    )
    if not file_destinazione: return

    try:
        # CHIAMATA ALLA FUNZIONE ISOLATA
        decrypt_db(password, file_origine, file_destinazione)
        messagebox.showinfo("Successo", f"File decriptato correttamente in:\n{file_destinazione}")
    except Exception as e:
        messagebox.showerror("Errore", "Impossibile decrittare. Password errata o file corrotto.")

def utility_cripta_db():
    """Utility per criptare un DB SQLite standard nel formato Lucy"""
    # 1. Chiede la password con cui criptare
    password = simpledialog.askstring("Utility Cifratura", "Scegli la password per criptare il DB:", show='*')
    if not password: return

    # 2. Seleziona il file .db decriptato (quello "in chiaro")
    file_origine = filedialog.askopenfilename(
        title="Seleziona il database DECRIPTATO",
        filetypes=[("SQLite Database", "*.db"), ("Tutti i file", "*.*")]
    )
    if not file_origine: return

    # 3. Chiede dove salvare il file finale criptato
    file_destinazione = filedialog.asksaveasfilename(
        title="Salva DB criptato come...",
        initialdir=APPDATA_DIR,
        initialfile="lucy.db",
        defaultextension=".db",
        filetypes=[("Database Criptato", "*.db")]
    )
    if not file_destinazione: return

    try:
        # Chiamata alla funzione atomica che usa Fernet
        encrypt_db(password, file_origine, file_destinazione)
        messagebox.showinfo("Successo", f"File criptato con successo!\nSalvato in: {file_destinazione}")
        logging.info(f"Manutenzione: DB criptato manualmente in {file_destinazione}")
    except Exception as e:
        logging.error(f"Errore utility criptazione: {e}")
        messagebox.showerror("Errore", f"Impossibile criptare il file: {e}")
         
def initialize_db():
    if os.path.exists(DB_PATH):
        messagebox.showinfo("Info", "Il database esiste già. Usa 'Avvia Server' per accedere.")
        return

    # Chiediamo la password per la PRIMA creazione
    password = simpledialog.askstring("Setup Iniziale", "Scegli una password per CRIPTARE il nuovo database:", show='*')
    
    if not password:
        return
    
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    try:
        normalized_path = DB_PATH.replace('\\', '/')
        
        # 1. Creiamo un'istanza temporanea dell'app per attivare il driver SQLCipher
        temp_app = create_app(db_path=normalized_path, db_password=password)
            
    except Exception as e:
        logging.error(f"Errore inizializzazione: {e}")
        messagebox.showerror("Errore Critico", f"Impossibile creare il database: {e}")

    try:
        # 2. Chiamiamo la funzione di creazione tabelle
        with temp_app.app_context():
            result = temp_app.setup_database_func()
            from app import db 
            
            db.session.remove()
            db.engine.dispose()
            
            if hasattr(temp_app, 'shutdown_func'):
                temp_app.shutdown_func()
                messagebox.showinfo("Successo", f"{result}\n\nDatabase sigillato correttamente!")
            
            else:
                messagebox.showerror("Errore", "Funzione shutdown_func non trovata.")
            
    
    except Exception as e:
        messagebox.showerror("Errore Cifratura", f"Tabelle create, ma errore nel salvataggio finale: {e}")
    
def main():
    global status_var_text, log_display_text, root
    # global root
    configure_logging_to_file()
    root = tk.Tk()
    root.title("Lucy Desktop Manager")
    root.geometry("600x500")
    root.configure(bg="#f0f0f0") # Sfondo grigio chiaro moderno

    status_var_text = tk.StringVar(value="Stato: 🔴 Server Spento")
    log_display_text = tk.StringVar(value="In attesa di log...")
    
    # --- TITOLO ---
    tk.Label(root, text="Lucy Desktop Manager", font=("Segoe UI", 18, "bold"), 
             bg="#f0f0f0", fg="#333").pack(pady=20)

    main_container = tk.Frame(root, bg="#f0f0f0")
    main_container.pack(fill="x", padx=20)
    
    # --- CONTENITORE PRINCIPALE (per affiancare le sezioni) ---
    main_container = tk.Frame(root, bg="#f0f0f0")
    main_container.pack(expand=True, fill="both", padx=10)

    # --- SEZIONE SINISTRA: AVVIO (Server e App) ---
    left_frame = tk.LabelFrame(main_container, text=" Controllo App ", padx=10, pady=10, bg="#ffffff", relief="flat")
    left_frame.pack(side=tk.LEFT, expand=True, fill="both", padx=10, pady=10)

    tk.Button(left_frame, text="🚀 Avvia Server", command=start_server, 
              width=20, bg="#4CAF50", fg="white", font=("Segoe UI", 10)).pack(pady=10)
    
    tk.Button(left_frame, text="🛑 Stop Server", command=stop_server,
              width=20, bg="#f44336", fg="white", font=("Segoe UI", 10)).pack(pady=5)
    
    tk.Button(left_frame, text="🖥️ Apri App Desktop", command=open_app, 
              width=20, bg="#2196F3", fg="white").pack(pady=5)
    
    tk.Button(left_frame, text="🌐 Apri nel Browser", command=open_web_app, 
              width=20).pack(pady=5)

    # --- SEZIONE DESTRA: SETUP & DATI ---
    right_frame = tk.LabelFrame(main_container, text=" Configurazione & Dati ", padx=10, pady=10, bg="#ffffff", relief="flat")
    right_frame.pack(side=tk.RIGHT, expand=True, fill="both", padx=10, pady=10)

    tk.Button(right_frame, text="🛠️ Inizializza DB", command=initialize_db, 
          width=20, bg="#FF9800", fg="white", font=("Segoe UI", 9, "bold")).pack(pady=10)
    
    tk.Button(right_frame, text="👤 Crea Admin", command=create_admin, width=20).pack(pady=5)
    
    tk.Button(right_frame, text="📅 Crea Giorni Settimana", command=create_week_days, width=20).pack(pady=5)
    
    # Spazio vuoto (separatore)
    tk.Label(right_frame, bg="#ffffff").pack(pady=5)
    
    tk.Button(right_frame, text="💾 Backup Database", command=backup_database, 
              width=20, bg="#d1e7dd").pack(pady=5)
    
    tk.Button(right_frame, text="🔓 Utility Decripta DB", command=utility_decripta_db, 
          width=20, bg="#673AB7", fg="white").pack(pady=5)
    tk.Button(right_frame, text="🔒 Utility Cripta DB", command=utility_cripta_db, 
          width=20, bg="#4527A0", fg="white").pack(pady=5)
    
    btn_frame = tk.Frame(root, bg="#f5f5f5")
    
    btn_frame.pack(expand=True, fill="both", padx=20)
    
    tk.Button(btn_frame, text="📂 Apri Cartella Dati", 
              command=open_data_folder, bg="#e0e0e0").pack(pady=5, fill="x")
    tk.Button(btn_frame, text="📂 Apri Cartella Temp", 
          command=open_temporary_folder, bg="#e0e0e0").pack(pady=5, fill="x")
    
    status_frame_base = tk.Frame(root, bd=1, relief=tk.SUNKEN, bg="#eeeeee")
    status_frame_base.pack(side=tk.BOTTOM, fill=tk.X)
    
    # --- SEZIONE LOG LIVE ---
    log_frame = tk.LabelFrame(root, text=" Live Logs (Ultime 50 righe) ", padx=10, pady=5, bg="#ffffff")
    log_frame.pack(fill="both", expand=True, padx=30, pady=10)


    # Label che mostra i log (Sfondo bianco, font monospaziato tipo terminale)
    log_area = scrolledtext.ScrolledText(
        log_frame, 
        height=10, 
        state=tk.DISABLED, 
        font=("Consolas", 9),
        bg="white", 
        fg="#333",
        padx=5, 
        pady=5
    )
    log_area.pack(fill="both", expand=True)

    # --- BARRA DI STATO ---
    status_frame = tk.Frame(status_frame_base, bd=1, relief=tk.SUNKEN, bg="#eeeeee")
    status_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # Notare: textvariable invece di text
    tk.Label(status_frame, textvariable=status_var_text, 
             anchor=tk.W, bg="#eeeeee", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=10, pady=2)

    tk.Label(status_frame, text=f"Sessione: {datetime.now().strftime('%H:%M')}", 
             bg="#eeeeee", font=("Segoe UI", 8), fg="#666").pack(side=tk.RIGHT, padx=10)

    # AVVIA IL CICLO DI AGGIORNAMENTO LOG
    update_live_logs(log_area)
    
    root.mainloop()

if __name__ == "__main__":
    main()
