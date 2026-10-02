import os
import glob
import shutil
import logging
import tempfile
from contextlib import contextmanager, suppress
from datetime import datetime

from alembic import command
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from cryptography.fernet import InvalidToken
from flask import current_app
from sqlalchemy import inspect as sa_inspect

from ..extension import db

BACKUPS_TO_KEEP = 10


def _config(autogenerate=False):
    migrate_ext = current_app.extensions["migrate"].migrate
    return migrate_ext.get_config(opts=["autogenerate"] if autogenerate else None)


# Non usare i wrapper di flask_migrate: su errore fanno sys.exit(1) e chiuderebbero la GUI.
def upgrade(revision="head"):
    command.upgrade(_config(), revision)


def stamp(revision):
    command.stamp(_config(), revision)


def autogenerate_revision(message):
    command.revision(_config(autogenerate=True), message, autogenerate=True)


def _script_dir():
    return ScriptDirectory.from_config(_config())


def _db_state():
    """Ritorna (revisioni correnti, il DB contiene tabelle utente)."""
    with db.engine.connect() as conn:
        current = set(MigrationContext.configure(conn).get_current_heads())
        tables = set(sa_inspect(conn).get_table_names()) - {"alembic_version"}
    return current, bool(tables)


def _schema_signature(engine):
    insp = sa_inspect(engine)
    return {
        t: set(c["name"] for c in insp.get_columns(t))
        for t in insp.get_table_names()
        if t != "alembic_version"
    }


@contextmanager
def _scratch_app():
    """App Flask su un DB SQLite vuoto e usa-e-getta (non cifrato, nessun dato reale)."""
    from .. import create_app

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    app = create_app(db_path=path.replace("\\", "/"))
    try:
        with app.app_context():
            yield app
    finally:
        with app.app_context():
            db.engine.dispose()
        with suppress(OSError):
            os.remove(path)


def _verify_matches_baseline(base_rev):
    """Un DB senza versione può essere marcato come baseline solo se ha lo schema della baseline."""
    real = _schema_signature(db.engine)
    with _scratch_app():
        upgrade(revision=base_rev)
        expected = _schema_signature(db.engine)

    problems = [f"tabella mancante: {t}" for t in sorted(expected.keys() - real.keys())]
    for t in sorted(expected.keys() & real.keys()):
        if expected[t] != real[t]:
            missing = sorted(expected[t] - real[t])
            extra = sorted(real[t] - expected[t])
            problems.append(f"{t}: colonne mancanti={missing} colonne extra={extra}")

    if problems:
        raise RuntimeError(
            "Il DB non ha versione Alembic e il suo schema non coincide con la baseline "
            f"({base_rev}); non lo marco per evitare di saltare modifiche.\n- " + "\n- ".join(problems)
        )


def has_pending_migrations():
    heads = set(_script_dir().get_heads())
    if not heads:
        return False
    current, _ = _db_state()
    return current != heads


def stamp_head_if_available():
    """Dopo db.create_all() lo schema è già l'ultimo: lo marca per non rieseguire le migration."""
    if _script_dir().get_heads():
        stamp(revision="head")


def apply_migrations():
    """Porta il DB dell'app corrente all'ultima revisione. Solleva RuntimeError se non è sicuro procedere."""
    script = _script_dir()
    heads = script.get_heads()
    if not heads:
        return "Nessuna migration presente: nulla da applicare."
    if len(heads) > 1:
        raise RuntimeError(f"Più head Alembic ({', '.join(heads)}): serve una migration di merge.")
    head = heads[0]

    current, has_tables = _db_state()
    stamped_baseline = False

    if not current:
        if not has_tables:
            db.create_all()
            stamp(revision="head")
            return f"DB vuoto: schema creato e marcato alla revisione {head}."

        base = script.get_bases()[0]
        _verify_matches_baseline(base)
        stamp(revision=base)
        current = {base}
        stamped_baseline = True
        logging.info(f"DB esistente marcato come baseline {base}.")

    try:
        for rev in current:
            script.get_revision(rev)
    except Exception:
        raise RuntimeError(
            f"Il DB è alla revisione {sorted(current)}, sconosciuta a questa versione dell'applicazione "
            "(DB più recente del programma?)."
        )

    if current == {head}:
        return f"DB esistente marcato come baseline {head}." if stamped_baseline else "Schema già aggiornato."

    upgrade(revision="head")
    return f"Schema aggiornato alla revisione {head}."


def backup_encrypted_db(db_path):
    """Copia il DB cifrato in backups/ accanto ad esso e mantiene solo gli ultimi BACKUPS_TO_KEEP."""
    backups_dir = os.path.join(os.path.dirname(db_path), "backups")
    os.makedirs(backups_dir, exist_ok=True)

    dest = os.path.join(backups_dir, f"lucy_pre-migrate_{datetime.now():%Y%m%d_%H%M%S}.db")
    shutil.copy2(db_path, dest)

    for old in sorted(glob.glob(os.path.join(backups_dir, "lucy_pre-migrate_*.db")))[:-BACKUPS_TO_KEEP]:
        with suppress(OSError):
            os.remove(old)
    return dest


def migrate_encrypted_db(db_path, password):
    """Applica le migration pendenti al DB cifrato in modo sicuro.

    Lavora su una copia decriptata: se qualcosa fallisce il file cifrato originale
    resta intatto. Prima di salvare crea un backup in backups/.
    """
    from .. import create_app

    try:
        app = create_app(db_path=db_path, db_password=password)
    except InvalidToken:
        raise RuntimeError("Password errata o file DB corrotto.")

    saved = False
    try:
        with app.app_context():
            if not has_pending_migrations():
                return "Schema già aggiornato."
            backup = backup_encrypted_db(db_path)
            logging.info(f"Backup pre-migration: {backup}")
            message = apply_migrations()

        app.shutdown_func()
        saved = True
        return f"{message}\nBackup pre-migration:\n{backup}"
    finally:
        if not saved:
            app.discard_func()


def generate_revision(message):
    """Genera una nuova migration confrontando i modelli con lo schema prodotto dalle migration esistenti.

    Usa un DB vuoto usa-e-getta: non serve la password e non tocca dati reali.
    La migration generata viene subito applicata allo scratch DB per verificare che funzioni.
    """
    with _scratch_app():
        script = _script_dir()
        # Alembic non crea versions/ da solo: senza, la prima generazione fallisce.
        os.makedirs(script.versions, exist_ok=True)
        head_before = set(script.get_heads())
        if head_before:
            upgrade(revision="head")

        autogenerate_revision(message=message)

        script = _script_dir()
        head_after = set(script.get_heads())
        if head_after == head_before:
            return None

        new_rev = script.get_revision((head_after - head_before).pop())
        upgrade(revision="head")
        return new_rev.path
