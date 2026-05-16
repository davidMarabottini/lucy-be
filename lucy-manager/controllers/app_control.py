import threading
import webbrowser
import webview
import logging
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from werkzeug.serving import make_server

from core.config import DB_PATH
from app import create_app
from core import state

def start_server(status_var_text):
    if state.active_app is not None:
        messagebox.showinfo("Info", "Il server è già attivo.")
        return
    
    if not os.path.exists(DB_PATH):
        messagebox.showwarning("Database Mancante", "Il database non esiste. Inizializzalo prima.")
        logging.error(f"DB mancante o non esistente in {DB_PATH}")
        return

    password = simpledialog.askstring("Login", "Password del database:", show='*')
    if not password: return

    try:
        logging.info(f'Avvio inizializzazione Flask..., db_path: {DB_PATH}')
        normalized_db_path = os.path.abspath(DB_PATH).replace("\\", "/")
        
        state.active_app = create_app(db_path=normalized_db_path, db_password=password)
        
        state.server_instance = make_server("127.0.0.1", 5000, state.active_app, threaded=True)
        state.server_thread = threading.Thread(
            target=state.server_instance.serve_forever,
            daemon=True
        )
        state.server_thread.start()
        
        logging.info('Server Flask avviato.')
        status_var_text.set("Stato: ✅ Server Attivo")
        
    except Exception as e:
        state.active_app = None # Reset in caso di errore
        logging.error(f"Errore avvio: {e}")
        messagebox.showerror("Errore di Avvio", str(e))

def stop_server(status_var_text):
    if not state.active_app:
        messagebox.showerror("Errore", "Server non avviato")
        return

    try:
        # Prima ferma il server HTTP (rilascia il lock sul file DB)
        if state.server_instance:
            state.server_instance.shutdown()
            state.server_thread.join(timeout=5)

        # Poi cifra il DB
        if hasattr(state.active_app, "shutdown_func"):
            state.active_app.shutdown_func()

        # Pulizia dello STATO GLOBALE
        state.active_app = None
        state.server_thread = None
        state.server_instance = None

        status_var_text.set("Stato: 🔴 Server Fermato (DB criptato)")
        messagebox.showinfo("OK", "Server fermato correttamente")
        logging.info("Server arrestato.")

    except Exception as e:
        logging.error(f"Errore stop: {e}")
        messagebox.showerror("Errore", str(e))

def open_web_app():
    if not state.server_thread or not state.server_thread.is_alive():
        messagebox.showerror("Errore", "Avvia prima il server")
        return
    webbrowser.open("http://127.0.0.1:5000/")
  
def open_app():
    if not state.server_thread or not state.server_thread.is_alive():
        messagebox.showerror("Errore", "Avvia prima il server")
        return

    logging.info("Apertura finestra WebView...")
    url = "http://127.0.0.1:5000/"
    webview.create_window("Lucy Desktop", url, width=1200, height=800)
    webview.start()
