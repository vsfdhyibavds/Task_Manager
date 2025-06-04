import click
from commands.user_commands import register_user

@click.command()
@click.option('--username', prompt='Username', help='The username for the new user')
@click.option('--email', prompt='Email', help='The email address for the new user')
@click.option('--password', prompt='Password', hide_input=True, confirmation_prompt=True, help='The password for the new user')
def register_user_cli(username, email, password):
    result = register_user(username, email, password)
    if "error" in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo(result["message"])

if __name__ == '__main__':
    register_user_cli()
