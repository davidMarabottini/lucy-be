import tkinter as tk

def create_sidebar_button(parent, text, command):
    return tk.Button(
      parent,
      text=text,
      command=command,
      anchor="w",
      relief="flat",
      bg="#34495e",
      fg="white",
      activebackground="#3d566e",
      padx=10,
      pady=6
    )


def create_section_label(parent, text):
    return tk.Label(
      parent,
      text=text,
      bg="#2c3e50",
      fg="#bdc3c7",
      font=("Segoe UI", 9, "bold")
    )
