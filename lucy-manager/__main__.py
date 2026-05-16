import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

from core.config import *
from core.logger import configure_logging_to_file, update_live_logs
from controllers import app_control, folder_links, data_config, db_utils
from ui.components import create_sidebar_button, create_section_label

def main():
    configure_logging_to_file()

    root = tk.Tk()
    root.title("Lucy Desktop Manager")
    root.geometry("1000x650")
    root.configure(bg="#ecf0f1")

    status_var_text = tk.StringVar(value="🔴 Server Spento")

    # ===== ROOT LAYOUT =====
    container = tk.Frame(root, bg="#ecf0f1")
    container.pack(fill="both", expand=True)

    # ===== SIDEBAR =====
    sidebar = tk.Frame(container, bg="#2c3e50", width=230)
    sidebar.pack(side="left", fill="y")

    content = tk.Frame(container, bg="#ecf0f1")
    content.pack(side="right", fill="both", expand=True)

    # ===== SIDEBAR HEADER =====
    tk.Label(sidebar, text="Lucy Manager", bg="#2c3e50", fg="white",
      font=("Segoe UI", 14, "bold")).pack(pady=20)

    # ===== DATI =====
    create_section_label(sidebar, "DATI & DB").pack(anchor="w", padx=10, pady=(15, 0))

    create_sidebar_button(sidebar, "🛠️ Inizializza DB",
      db_utils.initialize_db).pack(fill="x", padx=10, pady=2)

    create_sidebar_button(sidebar, "👤 Crea Admin",
      data_config.create_admin).pack(fill="x", padx=10, pady=2)

    create_sidebar_button(sidebar, "📅 Crea Giorni",
      data_config.create_week_days).pack(fill="x", padx=10, pady=2)

    create_sidebar_button(sidebar, "🔗 Sync Clienti Libemax",
      data_config.sync_libemax_clients).pack(fill="x", padx=10, pady=2)

    if os.environ.get("DEV_MODE", "").lower() in ("1", "true"):
        create_sidebar_button(sidebar, "🔄 DB Migrate",
          db_utils.run_migrations).pack(fill="x", padx=10, pady=2)

    # ===== UTILITY =====
    create_section_label(sidebar, "UTILITY").pack(anchor="w", padx=10, pady=(15, 0))

    create_sidebar_button(sidebar, "💾 Backup DB",
      db_utils.backup_database).pack(fill="x", padx=10, pady=2)

    create_sidebar_button(sidebar, "🔓 Decripta DB",
      db_utils.utility_decripta_db).pack(fill="x", padx=10, pady=2)

    create_sidebar_button(sidebar, "🔒 Cripta DB",
      db_utils.utility_cripta_db).pack(fill="x", padx=10, pady=2)

    # ===== CARTELLE =====
    create_section_label(sidebar, "CARTELLE").pack(anchor="w", padx=10, pady=(15, 0))

    create_sidebar_button(sidebar, "📂 Cartella Dati",
      folder_links.open_data_folder).pack(fill="x", padx=10, pady=2)

    create_sidebar_button(sidebar, "📂 Cartella Temp",
      folder_links.open_temporary_folder).pack(fill="x", padx=10, pady=2)

    # ===== HEADER =====
    header = tk.Frame(content, bg="#ecf0f1")
    header.pack(fill="x", padx=20, pady=10)

    tk.Label(header, text="Dashboard", font=("Segoe UI", 20, "bold"),
      bg="#ecf0f1", fg="#2c3e50").pack(anchor="w")

    # ===== STATUS CARD =====
    status_card = tk.Frame(content, bg="white", bd=0)
    status_card.pack(fill="x", padx=20, pady=10)

    tk.Label(status_card, text="STATO SERVER", font=("Segoe UI", 9, "bold"),
      fg="#7f8c8d", bg="white").pack(anchor="w", padx=15, pady=(10, 0))

    tk.Label(
      status_card,
      textvariable=status_var_text,
      font=("Segoe UI", 18, "bold"),
      bg="white"
    ).pack(anchor="w", padx=15, pady=10)

    # ===== QUICK ACTIONS =====
    actions = tk.Frame(content, bg="#ecf0f1")
    actions.pack(fill="x", padx=20, pady=5)

    tk.Button(actions, text="🚀 Avvia",
      command=lambda: app_control.start_server(status_var_text),
      bg="#27ae60", fg="white").pack(side="left", padx=5)

    tk.Button(actions, text="🛑 Stop",
      command=lambda: app_control.stop_server(status_var_text),
      bg="#c0392b", fg="white").pack(side="left", padx=5)

    tk.Button(actions, text="🌐 Apri Web",
      command=app_control.open_web_app).pack(side="left", padx=5)
    tk.Button(actions, text="🖥️ Apri Desktop",
      command=app_control.open_app).pack(side="left", padx=5)


    # ===== LOG PANEL =====
    log_container = tk.Frame(content, bg="white")
    log_container.pack(fill="both", expand=True, padx=20, pady=10)

    tk.Label(
      log_container,
      text="Live Logs",
      font=("Segoe UI", 11, "bold"),
      bg="white"
    ).pack(anchor="w", padx=10, pady=8)

    log_area = scrolledtext.ScrolledText(log_container, state=tk.DISABLED,
      font=("Consolas", 9), bg="#fafafa", relief="flat")
    
    log_area.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # ===== STATUS BAR =====
    status_bar = tk.Frame(root, bg="#dfe6e9")
    status_bar.pack(fill="x")

    tk.Label(status_bar, textvariable=status_var_text, bg="#dfe6e9", font=("Segoe UI", 9)
      ).pack(side="left", padx=10, pady=4)

    tk.Label(status_bar, text=f"{datetime.now().strftime('%H:%M')}", bg="#dfe6e9", font=("Segoe UI", 8)
      ).pack(side="right", padx=10)

    update_live_logs(log_area, root)

    root.mainloop()


if __name__ == "__main__":
    main()
