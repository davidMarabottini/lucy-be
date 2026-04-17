import click
from flask.cli import with_appcontext

from .seeders import create_admin as create_admin_internal
from .seeders import create_week_days as create_week_days_internal


def register_cli_commands(app):
    @app.cli.command("create-admin")
    @with_appcontext
    def create_admin():
        username = click.prompt("Username")
        email = click.prompt("Email")
        password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
        click.echo(create_admin_internal(username, email, password))

    @app.cli.command("create-week-days")
    @with_appcontext
    def create_week_days():
        click.echo(create_week_days_internal())

    app.create_admin_func = create_admin_internal
    app.create_week_days_func = create_week_days_internal
