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
  
  with app.app_context():
    result = app.create_admin_func(username, email, password)
    messagebox.showinfo("Risultato", result)

def create_week_days():
  app = state.active_app
  
  if not state.active_app:
    messagebox.showerror("Errore", "Server non avviato")
    return
  
  with app.app_context():
    result = app.create_week_days_func()
    messagebox.showinfo("Risultato", result)
