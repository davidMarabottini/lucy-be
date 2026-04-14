import os
import sys

def get_base_path():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS

    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

def get_db_path(base_path, db_path=None):
    return db_path or os.path.join(base_path, "lucy.db")


def get_static_path(base_path):
    return os.path.join(base_path, "app", "static")


def resolve_paths(db_path=None):
    base = get_base_path()
    return (
        base,
        get_db_path(base, db_path),
        get_static_path(base),
    )
# def resolve_paths(db_path):
#     base_path = get_base_path()

#     final_db_path = db_path or os.path.join(base_path, "lucy.db")

#     static_folder = os.path.join(base_path, "app", "static")

#     return base_path, os.path.abspath(final_db_path).replace("\\", "/"), static_folder