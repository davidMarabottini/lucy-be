import os
import logging
import tkinter as tk
from core.config import CURRENT_LOG_FILE

def configure_logging_to_file():
    """Configura il sistema di logging standard di Python"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(CURRENT_LOG_FILE),
            logging.StreamHandler()
        ]
    )
    logging.info("Sistema di logging inizializzato.")

def update_live_logs(text_widget, root):
    """
    Legge le ultime righe dal file di log e le visualizza nel widget Tkinter.
    Viene eseguita ricorsivamente ogni secondo.
    """
    if os.path.exists(CURRENT_LOG_FILE):
        try:
            with open(CURRENT_LOG_FILE, "r") as f:
                lines = f.readlines()
                last_lines = "".join(lines[-150:]) 

                text_widget.config(state=tk.NORMAL)
                text_widget.delete('1.0', tk.END)
                text_widget.insert(tk.END, last_lines)
                text_widget.see(tk.END)
                text_widget.config(state=tk.DISABLED)
                
        except Exception as e:
            print(f"Errore lettura log: {e}")

    root.after(1000, lambda: update_live_logs(text_widget, root))
