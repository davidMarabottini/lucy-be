# Come modificare il DB

Non ricreare mai il DB e non copiare dati a mano: si scrive una migration, si committa, e il Manager la applica da solo
(con backup) all'avvio del server.

## Procedura

1. Modifica `app/models.py`.
2. Avvia il Manager con `DEV_MODE=1` e premi **Generate Migration** (descrizione breve).
   Lavora su un DB vuoto di prova: non serve la password e non tocca dati reali.
3. Apri il file creato in `migrations/versions/` e controllalo (vedi sotto).
4. Premi **Avvia** (o **DB Migrate** a server fermo) col tuo DB: la migration viene applicata. Verifica che l'app funzioni.
5. Committa modelli + file di migration insieme, poi `python build.py`.
6. In produzione basta avviare il nuovo eseguibile: la migration si applica all'avvio.

Se la migration fallisce, `lucy.db` resta intatto. Prima di ogni migration viene salvato un backup in
`%APPDATA%\LucyManager\backups\`; per tornare indietro, a server fermo, copialo sopra `lucy.db`.

## Cosa controllare nel file generato

- **Colonna NOT NULL nuova su tabella con dati**: aggiungi `server_default=...` (oppure `nullable=True`, riempi, poi NOT NULL).
- **Rinomina**: Alembic genera drop + add e perdi i dati; sostituisci con `batch_op.alter_column('old', new_column_name='new')`
  o `op.rename_table(...)`.
- **Trasformazioni di dati**: falle nella migration con `op.execute(...)`.
- Mantieni le operazioni dentro `with op.batch_alter_table(...)` (SQLite ricrea la tabella).

## Regole

- `migrations/versions/` va sempre committata. Mai cancellare o modificare una migration già distribuita:
  se serve una correzione, se ne crea una nuova.
- Una sola migration per volta in sviluppo; se il Manager dice "DB a una revisione sconosciuta", manca un file in `versions/`
  (recuperalo da git con `git log --all -S <revisione>`).
