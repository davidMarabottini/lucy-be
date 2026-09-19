import PyInstaller.__main__

PyInstaller.__main__.run([
    'lucy-manager/__main__.py',
    '--onedir',
    '--windowed',
    '--name=Lucy',
    '--paths=.',
    '--add-data=app/static;app/static',
    '--add-data=migrations;migrations',
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