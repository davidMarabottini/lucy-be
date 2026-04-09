import PyInstaller.__main__

PyInstaller.__main__.run([
    'desktop.py',
    '--onedir',
    '--windowed',
    '--name=LucyDesktop',
    '--add-data=app/static;app/static',
    '--add-data=models;models',
    '--add-data=migrations;migrations',
    # '--add-data=manager.html;.',
    '--hidden-import=app',
    '--hidden-import=flask',
    '--hidden-import=sqlalchemy',
    '--hidden-import=webview',
    '--hidden-import=sklearn',
    '--hidden-import=joblib',
    '--hidden-import=flask_sqlalchemy',
    '--hidden-import=flask_migrate',
    '--hidden-import=flask_cors',
])