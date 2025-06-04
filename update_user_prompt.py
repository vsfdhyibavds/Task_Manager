import click
from commands.user_commands import update_user

@click.command()
@click.option('--user-id', prompt='User ID', type=int)
def update_user_prompt(user_id):
    username = click.prompt('New username', default='', show_default=False)
    email = click.prompt('New email', default='', show_default=False)
    password = click.prompt('New password', default='', hide_input=True, confirmation_prompt=True, show_default=False)

    updates = {}
    if username:
        updates['username'] = username
    if email:
        updates['email'] = email
    if password:
        updates['password'] = password

    if not updates:
        click.echo("No updates provided")
        return

    result = update_user(user_id, updates)
    if 'error' in result:
        click.echo(f"Error: {result['error']}")
    else:
        click.echo(result['message'])

if __name__ == '__main__':
    update_user_prompt()
