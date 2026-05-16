import logging
from tkinter import messagebox, simpledialog

from core import state

def create_admin():
  app = state.active_app
  
  if not state.active_app:
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
  
  try:
    logging.info(f"Creazione admin: {username} ({email})")
    with app.app_context():
      result = app.create_admin_func(username, email, password)
      logging.info(f"Admin creato con successo: {username}")
      messagebox.showinfo("Risultato", result)
  except Exception as e:
    logging.error(f"Errore creazione admin: {e}")
    messagebox.showerror("Errore", f"Creazione admin fallita: {e}")

def create_week_days():
  app = state.active_app
  
  if not state.active_app:
    messagebox.showerror("Errore", "Server non avviato")
    return
  
  try:
    logging.info("Creazione giorni della settimana...")
    with app.app_context():
      result = app.create_week_days_func()
      logging.info(f"Giorni della settimana creati con successo.")
      messagebox.showinfo("Risultato", result)
  except Exception as e:
    logging.error(f"Errore creazione giorni della settimana: {e}")
    messagebox.showerror("Errore", f"Creazione giorni fallita: {e}")

def sync_libemax_clients():
  app = state.active_app

  if not app:
    messagebox.showerror("Errore", "Server non avviato")
    return

  try:
    logging.info("Avvio sincronizzazione clienti da Libemax...")
    with app.app_context():
      from app.services.client_service import ClientService
      synced = ClientService.sync_from_libemax()
      logging.info(f"Sincronizzazione completata: {synced} clienti sincronizzati.")
      messagebox.showinfo("Successo", f"Clienti sincronizzati: {synced}")
  except Exception as e:
    logging.error(f"Errore sincronizzazione clienti Libemax: {e}")
    messagebox.showerror("Errore", f"Sincronizzazione fallita: {e}")
